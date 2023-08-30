from typing import Callable
from typing import TypeVar
from typing import overload

from . import _ConverterType

_T = TypeVar('_T')

def pipe(*validators: _ConverterType) -> _ConverterType: ...
def optional(converter: _ConverterType) -> _ConverterType: ...
@overload
def default_if_none(default: _T) -> _ConverterType: ...
@overload
def default_if_none(*, factory: Callable[[], _T]) -> _ConverterType: ...
def to_bool(val: str) -> bool: ...
