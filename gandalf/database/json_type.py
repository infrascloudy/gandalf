from sqlalchemy import TypeDecorator
from sqlalchemy.types import VARCHAR
from sqlalchemy import dialects
from sqlalchemy.dialects import postgresql, mysql
import json
from typing import Union, Optional

DialectType = Union[postgresql.UUID, VARCHAR]
ValueType = Optional[Union[dict, str]]


class JSON(TypeDecorator):
    impl = VARCHAR
    _MAX_VARCHAR_LIMIT = 100000

    def load_dialect_impl(self, dialect: dialects) -> DialectType:
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(postgresql.JSON())
        elif dialect.name == 'mysql':
            if 'JSON' in dialect.ischema_names:
                return dialect.type_descriptor(mysql.JSON())
            else:
                return dialect.type_descriptor(
                    VARCHAR(self._MAX_VARCHAR_LIMIT)
                )
        else:
            return dialect.type_descriptor(VARCHAR(self._MAX_VARCHAR_LIMIT))

    def process_bind_param(self, value: ValueType, dialect: dialects) -> Optional[str]:
        if value is None:
            return value
        else:
            return json.dumps(value)

    def process_result_value(self, value: Optional[str], dialect: dialects) -> Optional[dict]:
        if value is None:
            return value
        else:
            return json.loads(value)

    def copy(self, *args, **kwargs) -> 'JSON':
        return JSON(*args, **kwargs)

