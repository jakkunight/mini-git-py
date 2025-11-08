from abc import ABC, abstractmethod

from .repository import Repository
from .commit import Commit
from .references import Ref
from .tag import Tag


class VersionControlSystem(ABC):
    """
    Una interfaz que representa un Sistema de Control de Versiones.
    """

    @abstractmethod
    def init(self, repository: Repository) -> str | None:
        """
        Inicializa la carpeta del proyecto y toma un repositorio como entrada para almacenar los cambios de versiones de esa carpeta. Es responsabilidad de la aplicación inicializar correctamente el repositorio, y proteger su contenido en caso de que el mismo se encuentre en la carpeta de trabajo.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def stage_file(self, repository: Repository, path: str) -> str | None:
        """
        Añade un archivo al staging area del repositorio dado. Actualiza el tree

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def stage_directory(self, repository: Repository, path: str) -> str | None:
        """
        Añade un archivo al staging area del repositorio dado. Actualiza el index del repositorio con las entradas de un directorio. Devuelve SHA-256 del `Tree` creado.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def commit(
        self, repository: Repository, author: str, email: str, message: str
    ) -> str | None:
        """
        Crea un `Commit` a partir del `Tree` almacenado en el índice.

        Devuelve el SHA-256 del `Commit` creado. La operación limpia el índice del repositorio.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def checkout_commit(self, repository: Repository, commit: str) -> str | None:
        """
        Toma como entrada un repositorio y el SHA-256 de un `Commit` para restaurar el working directory al estado indicado en el `Commit`.

        Devuelve el SHA-256 del `Commit` restaurado.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def checkout_ref(self, repository: Repository, name: str) -> str | None:
        """
        Toma como entrada un `Repository` y el nombre de un `Ref` para restaurar el working directory al estado indicado en el `Commit` referenciado por la `Ref`.

        Devuelve el SHA-256 del `Commit` restaurado.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def checkout_tag(self, repository: Repository, name: str) -> str | None:
        """
        Toma como entrada un `Repository` y el nombre de un `Tag` para restaurar el working directory al estado indicado en el `Commit` referenciado por el `Tag`.

        Devuelve el SHA-256 del `Commit` restaurado.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def log(self, repository: Repository, ref: Ref | None) -> Commit | None:
        """
        Toma como entrada un `Repository` y una `Ref`. Devuelve una lista con los `Commit` correspondientes a esa referencia. Si no se especifica una referencia, se devuelven los `Commit` correspondientes a la `Ref` activa.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def create_branch(
        self, repository: Repository, name: str, commit: str | None
    ) -> Ref | None:
        """
        Toma como entrada un `Repository`, el nombre de la nueva rama, y el SHA-256 del `Commit` al que hace referencia.

        Devuelve la `Ref` de la rama creada. Si la rama ya existía, se devuelve el `Ref` de dicha rama.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def delete_branch(self, repository: Repository, name: str) -> str | None:
        """
        Toma como argumentos un `Repository` y el nombre de una `Ref` para eliminarla del repositorio.

        Devuelve el SHA-256 del último commit referenciado de la rama.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def list_branches(self, repository: Repository) -> list[Ref] | None:
        """
        Toma como entrada un `Repository`. devuelve una lista con todas las`Ref` a `Commit` del repositorio.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def create_tag(
        self, repository: Repository, name: str, commit: str | None
    ) -> Tag | None:
        """
        Toma como entrada un `Repository`, el nombre de la nueva rama, y el SHA-256 del `Commit` al que hace referencia.

        Devuelve la `Tag` de la rama creada. Si la rama ya existía, se devuelve el `Tag` de dicha rama.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def delete_tag(self, repository: Repository, name: str) -> str | None:
        """
        Toma como argumentos un `Repository` y el nombre de una `Tag` para eliminarla del repositorio.

        Devuelve el SHA-256 del último commit referenciado de la rama.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    @abstractmethod
    def list_tags(self, repository: Repository) -> list[Tag] | None:
        """
        Toma como entrada un `Repository`. devuelve una lista con todas los `Tag` a `Commit` del repositorio.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass

    # TODO:
    # Definir un tipo de datos que modele las diferencias entre dos conjuntos de líneas.
    @abstractmethod
    def diff_commits(
        self, repository: Repository, base: str | None, target: str
    ) -> list[str] | None:
        """
        Toma como entrada un `Repository`, el SHA-256 de un `Commit` base y el SHA-256 de un `Commit` objetivo a comparar contra la base.

        Devuelve una lista de `Diff` entre los `Commit`.

        Si la operación falla, se devuelve `None` (nil-as-error), o se plantea una excepción `AssertionError` con un mensaje explicando el error.
        """
        pass
