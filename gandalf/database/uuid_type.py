from sqlalchemy import TypeDecorator
from sqlalchemy.types import CHAR
from sqlalchemy import dialects
from sqlalchemy.dialects import postgresql
from typing import Union, Optional
import uuid

DialectType = Union[postgresql.UUID, CHAR]
ValueType = Optional[Union[uuid.UUID, str]]


class UUID(TypeDecorator):
    impl = CHAR

    def load_dialect_impl(self, dialect: dialects) -> DialectType:
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(postgresql.UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value: ValueType, dialect: dialects) -> Optional[str]:
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            return str(value).replace('-', '')

    def process_result_value(self, value, dialect) -> Optional[uuid.UUID]:
        if value is None:
            return value
        else:
            return uuid.UUID(value)

    def copy(self, *args, **kwargs) -> 'UUID':
        return UUID(*args, **kwargs)
