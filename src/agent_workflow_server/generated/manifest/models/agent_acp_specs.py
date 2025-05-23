# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

# coding: utf-8

"""
    Agent Manifest Definition

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json




from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from agent_workflow_server.generated.manifest.models.agent_acp_specs_interrupts_inner import AgentACPSpecsInterruptsInner
from agent_workflow_server.generated.manifest.models.agent_capabilities import AgentCapabilities
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class AgentACPSpecs(BaseModel):
    """
    Specification of agent capabilities, config, input, output, and interrupts
    """ # noqa: E501
    capabilities: AgentCapabilities
    input: Dict[str, Any] = Field(description="This object contains an instance of an OpenAPI schema object, formatted as per the OpenAPI specs: https://spec.openapis.org/oas/v3.1.1.html#schema-object")
    output: Dict[str, Any] = Field(description="This object contains an instance of an OpenAPI schema object, formatted as per the OpenAPI specs: https://spec.openapis.org/oas/v3.1.1.html#schema-object")
    custom_streaming_update: Optional[Dict[str, Any]] = Field(default=None, description="This describes the format of an Update in the streaming.  Must be specified if `streaming.custom` capability is true and cannot be specified otherwise. Format follows: https://spec.openapis.org/oas/v3.1.1.html#schema-object")
    thread_state: Optional[Dict[str, Any]] = Field(default=None, description="This describes the format of ThreadState.  Cannot be specified if `threads` capability is false. If not specified, when `threads` capability is true, then the API to retrieve ThreadState from a Thread or a Run is not available. This object contains an instance of an OpenAPI schema object, formatted as per the OpenAPI specs: https://spec.openapis.org/oas/v3.1.1.html#schema-object")
    config: Dict[str, Any] = Field(description="This object contains an instance of an OpenAPI schema object, formatted as per the OpenAPI specs: https://spec.openapis.org/oas/v3.1.1.html#schema-object")
    interrupts: Optional[List[AgentACPSpecsInterruptsInner]] = Field(default=None, description="List of possible interrupts that can be provided by the agent. If `interrupts` capability is true, this needs to have at least one item.")
    __properties: ClassVar[List[str]] = ["capabilities", "input", "output", "custom_streaming_update", "thread_state", "config", "interrupts"]

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
        """Create an instance of AgentACPSpecs from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of capabilities
        if self.capabilities:
            _dict['capabilities'] = self.capabilities.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in interrupts (list)
        _items = []
        if self.interrupts:
            for _item in self.interrupts:
                if _item:
                    _items.append(_item.to_dict())
            _dict['interrupts'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of AgentACPSpecs from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "capabilities": AgentCapabilities.from_dict(obj.get("capabilities")) if obj.get("capabilities") is not None else None,
            "input": obj.get("input"),
            "output": obj.get("output"),
            "custom_streaming_update": obj.get("custom_streaming_update"),
            "thread_state": obj.get("thread_state"),
            "config": obj.get("config"),
            "interrupts": [AgentACPSpecsInterruptsInner.from_dict(_item) for _item in obj.get("interrupts")] if obj.get("interrupts") is not None else None
        })
        return _obj


