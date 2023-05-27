from typing import Any, Dict, List, Protocol, Tuple

from sugaru import check_callable_signature


class LoaderStub(Protocol):
    def __call__(self, *, param1: List[float], param2: Dict[str, int]) -> Tuple:
        ...


def test_object_signature_not_strict_ok() -> None:
    class LoaderOk:
        def __call__(self, param1: Any, param2: Any) -> Any:
            ...

    class LoaderOk2:
        def __call__(self, param1: Any, param2: Any, **kwargs: Any) -> Any:
            ...

    assert check_callable_signature(LoaderOk, LoaderStub)
    assert check_callable_signature(LoaderOk2, LoaderStub)


def test_object_signature_not_strict_error() -> None:
    class NotCallable:
        ...

    class BadLoader1:
        def __call__(self, param11: Any, param22: Any) -> Any:
            ...

    class BadLoader2:
        def __call__(self, param1: Any) -> Any:
            ...

    assert not check_callable_signature(NotCallable, LoaderStub)
    assert not check_callable_signature(BadLoader1, LoaderStub)
    assert not check_callable_signature(BadLoader2, LoaderStub)
