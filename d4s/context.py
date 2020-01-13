import threading
from typing import Any, MutableMapping, Iterator


class DotDict(MutableMapping):
    """
    A `dict` that also supports attribute ("dot") access. Think of this as an extension
    to the standard python `dict` object.  **Note**: while any hashable object can be added to
    a `DotDict`, _only_ valid Python identifiers can be accessed with the dot syntax; this excludes
    strings which begin in numbers, special characters, or double underscores.
    Example:
        ```python
        dotdict = DotDict({'a': 34}, b=56, c=set())
        dotdict.a # 34
        dotdict['b'] # 56
        dotdict.c # set()
        ```
    """

    def __init__(self, **kwargs: Any):
        super().update(kwargs)

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __setattr__(self, attr: str, value: Any) -> None:
        self[attr] = value

    def __iter__(self) -> Iterator[str]:
        return iter(self.__dict__.keys())

    def __delitem__(self, key: str) -> None:
        del self.__dict__[key]

    def __len__(self) -> int:
        return len(self.__dict__)

    def __repr__(self) -> str:
        if len(self) > 0:
            return "<{}: {}>".format(
                type(self).__name__, ", ".join(sorted(repr(k) for k in self.keys()))
            )
        else:
            return "<{}>".format(type(self).__name__)


class Context(DotDict, threading.local):
    """ A thread safe context store for D4S data.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def __getstate__(self) -> None:
        """
        Because we dynamically update context during runs, we don't ever want to pickle
        or "freeze" the contents of context.  Consequently it should always be accessed
        as an attribute of the prefect module.
        """
        raise TypeError(
            "\n".join(
                [
                    "Pickling context objects is explicitly not supported.",
                    "You should always access context as an attribute of the `prefect` module, as in `prefect.context`",
                ]
            )
        )

    def __repr__(self) -> str:
        return '<Context>'


context = Context()
