from typing import Mapping, Callable

from google.cloud import firestore


class FirestoreSessionFactory:
    """
    Generates and caches sessions of google firestore database
    """

    def __init__(
        self,
        *,
        session_cache: Mapping[int, firestore.AsyncClient],
        session_context_getter: Callable[..., int],
        gcp_project_id: str,
        gcp_credentials_path: str,
        database_name: str,
    ) -> None:
        self._session_cache = session_cache
        self._session_context_getter = session_context_getter
        self._gcp_project_id = gcp_project_id
        self._gcp_credentials_path = gcp_credentials_path
        self._database_name = database_name

    def __call__(self) -> firestore.AsyncClient:
        curr_session_context = self._session_context_getter()

        if curr_session_context not in self._session_cache:
            self._session_cache[curr_session_context] = firestore.AsyncClient(
                project=self._gcp_project_id,
                credentials=self._gcp_credentials_path,
                database=self._database_name,
            )

        return self._session_cache[curr_session_context]

    def remove_current_session(self) -> None:
        curr_session_context = self._session_context_getter()

        if curr_session_context in self._session_cache:
            del self._session_cache[curr_session_context]
