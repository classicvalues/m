from typing import Callable, Generic, Iterator, TypeVar, Union, cast

A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name
G = TypeVar('G')  # pylint: disable=invalid-name
LazyArg = Union[A, Callable[[], A]]


def lazy_arg(param: LazyArg[A]) -> A:
    """Return the result of evaluating `param` if it is function.

    Otherwise param is returned.
    """
    return param if not callable(param) else param()


class StopBadIteration(Exception):
    """Store a `Bad` instance."""

    def __init__(self, bad):
        Exception.__init__(self)
        self.bad = bad


class OneOf(Generic[B, G]):
    """An instance of `OneOf` is an instance of either `Bad` or `Good`."""

    def __init__(self, bad: bool, val: Union[B, G]):
        self.is_bad = bad
        self.value = val

    def __iter__(self) -> Iterator[G]:
        if self.is_bad:
            raise StopBadIteration(self)
        yield cast(G, self.value)

    def iter(self):
        """Shortcut to transform to a list: list(x.iter()).

        It will either contain a value or be an empty list.
        """
        if not self.is_bad:
            yield self.value

    def map(self, fct):
        """The given function is applied if this is a `Good` value."""
        return self if self.is_bad else Good(fct(self.value))

    def flat_map_bad(self, fct: Callable[[B], 'OneOf']) -> 'OneOf':
        """The given function is applied if this is a `Bad` value."""
        return fct(cast(B, self.value)) if self.is_bad else self

    def get_or_else(self, or_: LazyArg[G]) -> G:
        """Returns the value if its Good or the given argument if its a Bad."""
        return lazy_arg(or_) if self.is_bad else cast(G, self.value)


class Bad(OneOf[B, G]):
    """The bad side of the disjoint union."""

    def __init__(self, val):
        OneOf.__init__(self, True, val)


class Good(OneOf[B, G]):
    """The good side of the disjoint union."""

    def __init__(self, val):
        OneOf.__init__(self, False, val)
