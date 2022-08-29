from typing import Generic, TypeVar

from pydantic.generics import GenericModel

T = TypeVar('T')


class Range(GenericModel, Generic[T]):
    start: T
    end: T
