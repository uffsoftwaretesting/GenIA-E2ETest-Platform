"""Shared base for pipeline stage classes."""

from __future__ import annotations

import logging
from typing import Any, Dict, Tuple


logger = logging.getLogger(__name__)


class PipelineStageRunner:
    def __init__(self, llm_provider, prompt_manager) -> None:
        self.llm = llm_provider
        self.prompt_manager = prompt_manager

    def log(self, message: str, level: str = "info", stage: str = "") -> None:
        stage_prefix = f"[{stage}] " if stage else ""
        getattr(logger, level, logger.info)(f"{stage_prefix}{message}")
        print(f"[GenIA Pipeline] {stage_prefix}{message}", flush=True)

    @staticmethod
    def resolve_stage_llm(
        current_provider: str,
        current_model: str,
        current_api_key: str,
        current_temperature: float,
        stage: str,
        llm_overrides: Dict[str, Any] | None = None,
    ) -> Tuple[str, str, str, float]:
        override = (llm_overrides or {}).get(stage) or {}
        provider = override.get("provider") or current_provider
        model = override.get("model") or current_model
        api_key = override.get("apiKey") or override.get("api_key") or current_api_key
        temperature = override.get("temperature")
        if temperature is None:
            temperature = current_temperature
        try:
            temperature = float(temperature)
        except (TypeError, ValueError):
            temperature = float(current_temperature or 0.0)
        return provider, model, api_key, temperature
