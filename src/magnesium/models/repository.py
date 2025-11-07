from abc import ABC, abstractmethod
from .blob import Blob
from .commit import Commit
from .references import Ref
from .tag import Tag
from .tree import Tree


class Repository(ABC):
    """
    Una interfaz que representa un repositorio.

    Permite abstraer las operaciones realizadas sobre los objetos que puede guardar y recuperar.

    La clase que implementa esta interfaz es reponsable de la validación y el formato de archivo y compresión de los datos.

    La clase que haga uso de esta interfaz, es responsable de proveer los tipos de datos validados y de hacer el manejo de errores correspondiente en casos de fallos.
    """

    @abstractmethod
    def init(self, path: str | None) -> str | None:
        """
        Inicializa un repositorio en la carpeta provista. Si la capeta es `None`, entonces se usa la carpeta actual como repositorio.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def save_commit(self, commit: Commit) -> str | None:
        """
        Toma como entrada un `Commit` y lo almacena en el repositorio.

        Si la operación tuvo éxito, entonces retorna el SHA-256 del objeto creado.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def load_commit(self, sha: str) -> Commit | None:
        """
        Toma como entrada un SHA-256 y recupera un `Commit` del repositorio.

        Si la operación tuvo éxito, entonces retorna el `Commit`.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def save_tree(self, tree: Tree) -> str | None:
        """
        Toma como entrada un `Tree` y lo almacena en el repositorio.

        Si la operación tuvo éxito, entonces retorna el SHA-256 del objeto creado.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def load_tree(self, sha: str) -> Tree | None:
        """
        Toma como entrada un SHA-256 y recupera un `Tree` del repositorio.

        Si la operación tuvo éxito, entonces retorna el `tree`.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def save_blob(self, blob: Blob) -> str | None:
        """
        Toma como entrada un `Blob` y lo almacena en el repositorio.

        Si la operación tuvo éxito, entonces retorna el SHA-256 del objeto creado.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def load_blob(self, sha: str) -> Blob | None:
        """
        Toma como entrada un SHA-256 y recupera un `Blob` del repositorio.

        Si la operación tuvo éxito, entonces retorna el `Blob`.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def save_tag(self, tag: Tag) -> str | None:
        """
        Toma como entrada un `Tag` y lo almacena en el repositorio.

        Si la operación tuvo éxito, entonces retorna el SHA-256 del objeto creado.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def load_tag(self, name: str) -> Tag | None:
        """
        Toma como entrada el nombre de una `Ref` y recupera el `Tag` del repositorio.

        Si la operación tuvo éxito, entonces retorna el `Tag`.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def save_ref(self, ref: Ref) -> str | None:
        """
        Toma como entrada un `Ref` y lo almacena en el repositorio.

        Si la operación tuvo éxito, entonces retorna el SHA-256 del `Commit` referenciado.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def load_ref(self, name: str) -> Ref | None:
        """
        Toma como entrada el nombre de una `Ref` y recupera el SHA-256 del `Commit` referenciado del repositorio.

        Si la operación tuvo éxito, entonces retorna el `Ref`.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def update_ref(self, ref: Ref) -> str | None:
        """
        Toma como entrada una `Ref` existente y la actualiza en el repositorio. También actualiza el log de la referencia, permitiendo reconstruir el historial de cambios de esa referencia.

        Si la operación tuvo éxito, entonces retorna el SHA-256 del antiguo `Commit` referenciado.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def delete_ref(self, name: str) -> str | None:
        """
        Toma como entrada el nombre de una `Ref` y la elimina del repositorio.

        Si la operación tuvo éxito, entonces retorna el SHA-256 del último `Commit` referenciado.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def list_refs(self) -> list[Ref] | None:
        """
        Recupera todas las `Ref` del repositorio.

        Si la operación tuvo éxito, entonces retorna una `list[Ref]`.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def log_ref(self, name: str) -> list[Commit] | None:
        """
        Reconstruye el historial de cambios de una `Ref`.

        Si la operación tuvo éxito, entonces retorna una `list[Commit]`.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def log_refs(self) -> list[Commit] | None:
        """
        Reconstruye el historial de cambios de todas las `Ref` del repositorio. Garantiza que los `Commit` sean únicos, pero no reconstruye las ramificaciones. Es responsabilidad de quien invoque a este método realizar tal formato

        Si la operación tuvo éxito, entonces retorna una `list[Commit]`.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """

    @abstractmethod
    def update_head_ref(self, ref: Ref) -> str | None:
        """
        Actualiza la referencia HEAD.

        Si la operación tuvo éxito, entonces devuelve el SHA-256 del `Commit` actualmente referenciado.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def update_index(self, working_tree: Tree) -> str | None:
        """
        Toma como entrada el working tree (`Tree`) y lo almacena en el index para luego referenciarlo y hacer un `Commit`. Esto es el "staging area" del repositorio.

        Si la operación tuvo éxito, entonces retorna el SHA-256 del working tree actual.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def load_index(self) -> Tree | None:
        """
        Devuelve el `Tree` almacenado en el index que representa el working directory.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass
