import re
from datetime import datetime
from typing import Type, TypeVar, Union, Any, Optional

from sqlmodel import SQLModel, Field, text
from sqlmodel.sql.expression import Select, SelectOfScalar

from pydantic import BaseModel, create_model

ModelType = TypeVar("ModelType", bound=SQLModel)


class QueryParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    skip: int = Field(0, ge=0)
    event: int | None = Field(None, ge=1, nullable=True)
    order_by: str = Field("timestamp", schema_extra={'pattern': r"^\w+( (asc|desc))?$"})

    def build_query_params_model(
        base_model: Type[SQLModel],
        *,
        model_name_suffix: str = "QueryParams",
        base_query_params: dict[str, tuple[Any, Any]] = {
            "limit": (int, Field(100, gt=0, le=100)),
            "skip": (int, Field(0, ge=0)),
            "event": (int | None, Field(None, ge=1, nullable=True)),
            "order_by": (str, Field("timestamp", schema_extra={'pattern': r"^\w+( (asc|desc))?$"})),
        },
        base_class: Type[SQLModel] = SQLModel,
    ) -> Type[SQLModel]:
        fields = {}

        for name, model_field in base_model.model_fields.items():
            field_type = Optional[model_field.annotation]
            default = None
            metadata = model_field.json_schema_extra or {}
            fields[name] = (field_type, Field(default, **metadata))

        fields.update(base_query_params)
        return create_model(
            f"{base_model.__name__}{model_name_suffix}",
            **fields,
            __base__=base_class,
        )

    def apply_to_query(
        self, query: Select | SelectOfScalar, model: Type[ModelType]
    ) -> Union[Select, SelectOfScalar]:
        """
        Apply filters from this params object to a SQLModel select query.
        Supports implicit equality and suffix-based operators (e.g., _ge, _le, _contains).
        """
        operator_map = {
            "eq": lambda f, v: f == v,
            "ne": lambda f, v: f != v,
            "gt": lambda f, v: f > v,
            "lt": lambda f, v: f < v,
            "ge": lambda f, v: f >= v,
            "le": lambda f, v: f <= v,
            "contains": lambda f, v: f.contains(v),
            "startswith": lambda f, v: f.startswith(v),
            "endswith": lambda f, v: f.endswith(v),
            "in_": lambda f, v: f.in_(v),
        }

        suffix_pattern = re.compile(r"(.+?)_(" + "|".join(operator_map.keys()) + r")$")

        for field_name, field_value in self.model_dump(
            exclude={"skip", "limit", "order_by"}
        ).items():
            if field_value is None:
                continue

            match = suffix_pattern.match(field_name)
            if match:
                base_field, op = match.groups()
                try:
                    model_field = getattr(model, base_field)
                    query = query.where(operator_map[op](model_field, field_value))
                except AttributeError:
                    continue
            else:
                try:
                    model_field = getattr(model, field_name)
                    query = query.where(model_field == field_value)
                except AttributeError:
                    continue

        return query.offset(self.skip).limit(self.limit).order_by(text(self.order_by))


class SessionMappingParams(QueryParams):
    vrf_id: str | None = None
    protocol: int | None = None
    x_ip: str | None = None
    x_port: int | None = None
    dst_ip: str | None = None
    dst_port: int | None = None
    src_ip: str | None = None
    src_port: int | None = None
    timestamp_le: datetime | None = None
    timestamp_ge: datetime | None = None
    hook: str | None = None


class AddressMappingParams(QueryParams):
    vrf_id: str | None = None
    src_ip: str | None = None
    x_ip: str | None = None
    timestamp_le: datetime | None = None
    timestamp_ge: datetime | None = None
    hook: str | None = None


class PortMappingParams(QueryParams):
    vrf_id: str | None = None
    protocol: int | None = None
    x_ip: str | None = None
    x_port: int | None = None
    src_ip: str | None = None
    src_port: int | None = None
    timestamp_le: datetime | None = None
    timestamp_ge: datetime | None = None
    hook: str | None = None


class PortBlockMappingParams(QueryParams):
    vrf_id: str | None = None
    src_ip: str | None = None
    x_ip: str | None = None
    start_port: int | None = None
    end_port: int | None = None
    timestamp_le: datetime | None = None
    timestamp_ge: datetime | None = None
    hook: str | None = None
