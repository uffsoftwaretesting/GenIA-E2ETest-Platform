"""Validation stage."""

from __future__ import annotations

from typing import Any, Dict

from backend.domain.models import TestCase

from .base import PipelineStageRunner
from ..shared import _append_context_block, _render_prompt


class ValidationStage(PipelineStageRunner):
    async def run(
        self,
        current_api_key: str,
        current_model: str,
        current_provider: str,
        current_temperature: float,
        script: str,
        test_case: TestCase,
        temperature: float | None = None,
        prompt_override: str | None = None,
        llm_override: dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        provider, model, api_key, resolved_temperature = self.resolve_stage_llm(
            current_provider,
            current_model,
            current_api_key,
            current_temperature,
            "validation",
            {"validation": llm_override} if llm_override else None,
        )
        return await self.execute(
            script,
            test_case,
            api_key,
            model,
            provider,
            temperature=temperature if temperature is not None else resolved_temperature,
            prompt_override=prompt_override,
        )

    async def execute(
        self,
        script: str,
        test_case: TestCase,
        api_key: str,
        model: str,
        provider: str,
        temperature: float = 0.0,
        prompt_override: str | None = None,
    ) -> Dict[str, Any]:
        del provider
        prompt = prompt_override or self.prompt_manager.load_prompt("validation")
        final_prompt = _append_context_block(
            _render_prompt(
                prompt,
                generated_script=script,
                script=script,
                refined_test_case=test_case,
                structured_test_case=test_case,
                validation_context={
                    "script": script,
                    "test_case": test_case,
                },
            ),
            {
                "generated_script": script,
                "refined_test_case": test_case,
                "structured_test_case": test_case,
                "validation_context": {
                    "script": script,
                    "test_case": test_case,
                },
            },
        )
        variables_raw = self.llm.generate_json(api_key, model, final_prompt, temperature=temperature)
        return self._normalize_variables(variables_raw)

    def _normalize_variables(self, raw_variables: Any) -> Dict[str, Any]:
        if not raw_variables:
            return {"detected_inputs": [], "editable_fields": []}

        if isinstance(raw_variables, dict):
            inputs = raw_variables.get("detected_inputs", raw_variables.get("variables", []))
            editable_fields = raw_variables.get("editable_fields", [])
            if not isinstance(inputs, list):
                inputs = [inputs] if inputs else []
            if not isinstance(editable_fields, list):
                editable_fields = [editable_fields] if editable_fields else []
        elif isinstance(raw_variables, list):
            inputs = raw_variables
            editable_fields = raw_variables
        else:
            inputs = []
            editable_fields = []

        normalized_inputs = []
        normalized_editable_fields = []

        for i, var in enumerate(inputs):
            if isinstance(var, dict):
                name = var.get("variable_name") or var.get("name") or var.get("variable") or f"variable_{i + 1}"
                current_value = var.get("current_value", var.get("value", var.get("suggestedValue", var.get("suggested_value", ""))))
                normalized_inputs.append(
                    {
                        "variable_name": name,
                        "current_value": current_value,
                        "description": var.get("description", "Detectada automaticamente"),
                        "type": var.get("type", "string"),
                        "required": bool(var.get("required", True)),
                        "related_steps": var.get("related_steps", []),
                    }
                )
                normalized_editable_fields.append(
                    {
                        "name": name,
                        "value": current_value,
                        "description": var.get("description", "Detectada automaticamente"),
                        "editable": True,
                    }
                )
            else:
                normalized_inputs.append(
                    {
                        "variable_name": f"variable_{i + 1}",
                        "current_value": str(var),
                        "description": "Detectada automaticamente",
                        "type": "string",
                        "required": True,
                        "related_steps": [],
                    }
                )
                normalized_editable_fields.append(
                    {
                        "name": f"variable_{i + 1}",
                        "value": str(var),
                        "description": "Detectada automaticamente",
                        "editable": True,
                    }
                )

        return {"detected_inputs": normalized_inputs, "editable_fields": normalized_editable_fields}


__all__ = ["ValidationStage"]
