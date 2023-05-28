from sugaru import create_object


def test_create_objects() -> None:
    class OK:
        ...

    class Bad:
        def __init__(self, x: int) -> None:
            ...

    def ok_func() -> None:
        ...

    class StaticClass:
        @staticmethod
        def static() -> None:
            ...

    class BadClass:
        @property
        def bad_method(self) -> None:
            ...

    assert isinstance(create_object(OK), OK)  # type: ignore
    assert create_object(Bad) is None  # type: ignore
    assert create_object(ok_func) is ok_func  # type: ignore
    assert create_object(BadClass.bad_method) is None  # type: ignore
    assert create_object(StaticClass.static) is StaticClass.static  # type: ignore
