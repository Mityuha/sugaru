from sugaru.utils import callable_name


def test_callable_name() -> None:
    class Foo:
        def baz(self) -> None:
            ...

    def bar() -> None:
        ...

    assert callable_name(Foo) == "Foo"
    assert callable_name(Foo()) == "Foo"
    assert callable_name(bar) == "bar"
    assert callable_name(Foo.baz) == "baz"
    assert callable_name(Foo().baz) == "baz"
    assert callable_name(lambda: 1) == "<lambda>"
