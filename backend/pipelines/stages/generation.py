"""Generation stage."""

from __future__ import annotations

from backend.domain.models import TestCase

from .base import PipelineStageRunner
from ..shared import _append_context_block, _render_prompt, _safe_json_dumps


class GenerationStage(PipelineStageRunner):
    async def run(
        self,
        current_api_key: str,
        current_model: str,
        current_provider: str,
        current_temperature: float,
        test_case: TestCase,
        framework: str,
        language: str,
        temperature: float | None = None,
        prompt_override: str | None = None,
        llm_override: dict[str, Any] | None = None,
    ) -> str:
        provider, model, api_key, resolved_temperature = self.resolve_stage_llm(
            current_provider,
            current_model,
            current_api_key,
            current_temperature,
            "generation",
            {"generation": llm_override} if llm_override else None,
        )
        return await self.execute(
            test_case,
            framework,
            language,
            api_key,
            model,
            provider,
            temperature=temperature if temperature is not None else resolved_temperature,
            prompt_override=prompt_override,
        )

    async def execute(
        self,
        test_case: TestCase,
        framework: str,
        language: str,
        api_key: str,
        model: str,
        provider: str,
        temperature: float = 0.0,
        prompt_override: str | None = None,
    ) -> str:
        del provider
        prompt_template = prompt_override or self.prompt_manager.load_generation_prompt(framework)
        final_prompt = _append_context_block(
            _render_prompt(
                prompt_template,
                language=language,
                framework=framework,
                test_case=test_case,
            )
            + f"\n\nLanguage: {language}\n\nTest Case Data:\n{_safe_json_dumps(test_case)}",
            {
                "framework": framework,
                "language": language,
                "test_case": test_case,
            },
        )
        return self.llm.generate_text(api_key, model, final_prompt, temperature=temperature)


__all__ = ["GenerationStage"]
