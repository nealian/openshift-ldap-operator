from dataclasses import MISSING, dataclass, field
from datetime import datetime
from typing import Any, Optional, Pattern, Sequence, Type, TypeVar, Union

from apischema import schema
from apischema.schemas import ContentEncoding, Deprecated, Extra
from apischema.types import Number, Undefined
from kubernetes.client.models.v1_condition import V1Condition
from kubernetes.client.models.v1_local_object_reference import V1LocalObjectReference
from kubernetes.client.models.v1_object_meta import V1ObjectMeta
from kubernetes.client.models.v1_object_reference import V1ObjectReference


# Many lines, simple action.
def _field_schema(
    *,
    # field
    default=MISSING,
    default_factory=MISSING,
    init: bool = True,
    repr: bool = True,
    hash: Optional[bool] = None,
    compare: bool = True,
    kw_only=MISSING,
    # schema
    # annotations
    title: Optional[str] = None,
    description: Optional[str] = None,
    schema_default: Any = Undefined,
    examples: Optional[Sequence[Any]] = None,
    deprecated: Optional[Deprecated] = None,
    # number
    min: Optional[Number] = None,
    max: Optional[Number] = None,
    exc_min: Optional[Number] = None,
    exc_max: Optional[Number] = None,
    mult_of: Optional[Number] = None,
    # string
    format: Optional[str] = None,
    media_type: Optional[str] = None,
    encoding: Optional[ContentEncoding] = None,  # type: ignore
    min_len: Optional[int] = None,
    max_len: Optional[int] = None,
    pattern: Optional[Union[str, Pattern]] = None,
    # array
    min_items: Optional[int] = None,
    max_items: Optional[int] = None,
    unique: Optional[bool] = None,
    # objects
    min_props: Optional[int] = None,
    max_props: Optional[int] = None,
    # extra
    extra: Optional[Extra] = None,
    override: bool = False,
):
    if default is not MISSING and default_factory is not MISSING:
        raise ValueError("Only one of default and default_factory may be set.")
    if default is not MISSING:
        return field(
            default=default,
            init=init,
            repr=repr,
            hash=hash,
            compare=compare,
            metadata=schema(
                title=title,
                description=description,
                default=schema_default,
                examples=examples,
                deprecated=deprecated,
                min=min,
                max=max,
                exc_min=exc_min,
                exc_max=exc_max,
                mult_of=mult_of,
                format=format,
                media_type=media_type,
                encoding=encoding,
                min_len=min_len,
                max_len=max_len,
                pattern=pattern,
                min_items=min_items,
                max_items=max_items,
                unique=unique,
                min_props=min_props,
                max_props=max_props,
                extra=extra,
                override=override,
            ),
            kw_only=kw_only,  # type: ignore
        )
    elif default_factory is not MISSING:
        return field(
            default_factory=default_factory,
            init=init,
            repr=repr,
            hash=hash,
            compare=compare,
            metadata=schema(
                title=title,
                description=description,
                default=schema_default,
                examples=examples,
                deprecated=deprecated,
                min=min,
                max=max,
                exc_min=exc_min,
                exc_max=exc_max,
                mult_of=mult_of,
                format=format,
                media_type=media_type,
                encoding=encoding,
                min_len=min_len,
                max_len=max_len,
                pattern=pattern,
                min_items=min_items,
                max_items=max_items,
                unique=unique,
                min_props=min_props,
                max_props=max_props,
                extra=extra,
                override=override,
            ),
            kw_only=kw_only,  # type: ignore
        )
    else:
        return field(
            init=init,
            repr=repr,
            hash=hash,
            compare=compare,
            metadata=schema(
                title=title,
                description=description,
                default=schema_default,
                examples=examples,
                deprecated=deprecated,
                min=min,
                max=max,
                exc_min=exc_min,
                exc_max=exc_max,
                mult_of=mult_of,
                format=format,
                media_type=media_type,
                encoding=encoding,
                min_len=min_len,
                max_len=max_len,
                pattern=pattern,
                min_items=min_items,
                max_items=max_items,
                unique=unique,
                min_props=min_props,
                max_props=max_props,
                extra=extra,
                override=override,
            ),
            kw_only=kw_only,  # type: ignore
        )


class KubeResourceBase:
    api_version: str
    kind: str
    metadata: V1ObjectMeta | dict[str, Any]
    # TODO: init / metadata?
    # TODO: to_json?
    # TODO: from_json??
    # TODO: yaml file???
    # TODO: Use type reference somehow? If even necessary?
    pass


# See V1LocalObjectReference; TODO: maybe we can use that as the type in the thing?
@dataclass
class KubeLocalResourceRef:
    name: str = _field_schema(
        description="Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names",
    )
    __type_reference__: Type = field(
        default=V1LocalObjectReference,
        init=False,
        repr=False,
    )


@dataclass
class KubeTypedResourceRef:
    api_version: str = _field_schema(
        description="",
    )
    kind: str = _field_schema(
        description="",
    )
    name: str = _field_schema(
        description="",
    )
    namespace: Optional[str] = _field_schema(
        description="",
    )
    __type_reference__: Type = field(default=V1ObjectReference, init=False, repr=False)


@dataclass
class KubeLocalResourceRefWithDataKey(KubeLocalResourceRef):
    key: str = _field_schema(
        description="name of field within referent's data section. Must be a valid key.",
    )


# See V1Condition; TODO: maybe we can use that as the type in the thing?
@dataclass
class KubeCondition:
    last_transition_time: datetime = _field_schema(
        description="lastTransitionTime is the last time the condition transitioned from one status to another. This should be when the underlying condition changed.  If that is not known, then using the time when the API field changed is acceptable.",
    )
    message: str = _field_schema(
        description="message is a human readable message indicating details about the transition. This may be an empty string.",
    )
    observed_generation: Optional[int] = _field_schema(
        description="observedGeneration represents the .metadata.generation that the condition was set based upon. For instance, if .metadata.generation is currently 12, but the .status.conditions[x].observedGeneration is 9, the condition is out of date with respect to the current state of the instance.",
    )
    reason: str = _field_schema(
        description="reason contains a programmatic identifier indicating the reason for the condition's last transition. Producers of specific condition types may define expected values and meanings for this field, and whether the values are considered a guaranteed API. The value should be a CamelCase string. This field may not be empty.",
    )
    status: str = _field_schema(
        description="status of the condition, one of True, False, Unknown.",
    )
    type: str = _field_schema(
        description="type of condition in CamelCase or in foo.example.com/CamelCase.",
    )

    __type_reference__: Type = field(
        default=V1Condition,
        init=False,
        repr=False,
    )


@dataclass(frozen=True)
class PrintColumn:
    name: str
    type: str
    json_path: str
    priority: int = 0
    description: str = ''