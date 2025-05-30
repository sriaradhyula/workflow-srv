# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

# coding: utf-8

"""
    Agent Connect Protocol

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.2.2
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json




from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from agent_workflow_server.generated.models.run_status import RunStatus
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class ValueRunInterruptUpdate(BaseModel):
    """
    Partial result provided as value through streaming.
    """ # noqa: E501
    type: StrictStr
    interrupt: Optional[Any] = Field(description="This schema describes the interrupt payload. Actual schema describes a polimorphic object, which means a schema structured with `oneOf` and `discriminator`. The discriminator is the `interrupt_type`, while the schemas will be the ones defined in the agent spec under `interrupts`/`interrupt_payload` For example:          oneOf:   - $ref: '#/components/schemas/ApprovalInterruptPayload'   - $ref: '#/components/schemas/QuestionInterruptPayload' discriminator:   propertyName: interruput_type   mapping:     approval: '#/components/schemas/ApprovalInterruptPayload'     question: '#/components/schemas/QuestionInterruptPayload'")
    run_id: StrictStr = Field(description="The ID of the run.")
    status: RunStatus = Field(description="Status of the Run when this result was generated. This is particularly useful when this data structure is used for streaming results. As the server can indicate an interrupt or an error condition while streaming the result.")
    __properties: ClassVar[List[str]] = ["type", "interrupt", "run_id", "status"]

    @field_validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('interrupt',):
            raise ValueError("must be one of enum values ('interrupt')")
        return value

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of ValueRunInterruptUpdate from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        # set to None if interrupt (nullable) is None
        # and model_fields_set contains the field
        if self.interrupt is None and "interrupt" in self.model_fields_set:
            _dict['interrupt'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of ValueRunInterruptUpdate from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "interrupt": obj.get("interrupt"),
            "run_id": obj.get("run_id"),
            "status": obj.get("status")
        })
        return _obj


