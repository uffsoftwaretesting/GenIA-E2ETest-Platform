"""Extraction stage."""

from __future__ import annotations

import json
from typing import Any, List

from backend.domain.models import ExtractedElement, Module

from .base import PipelineStageRunner
from ..shared import _append_context_block, _compact_html_snapshot, _extract_html_snapshot, _render_prompt


class ExtractionStage(PipelineStageRunner):
    async def run(
        self,
        current_api_key: str,
        current_model: str,
        current_provider: str,
        current_temperature: float,
        module: Module,
        headless: bool = True,
        temperature: float | None = None,
        prompt_override: str | None = None,
        llm_override: dict[str, Any] | None = None,
        crawler: Any | None = None,
    ) -> List[ExtractedElement]:
        from backend.pipelines.shared import _create_browser_config, _require_crawl4ai
        try:
            from crawl4ai import AsyncWebCrawler
        except ImportError:  # pragma: no cover - optional runtime dependency
            AsyncWebCrawler = None

        provider, model, api_key, resolved_temperature = self.resolve_stage_llm(
            current_provider,
            current_model,
            current_api_key,
            current_temperature,
            "extraction",
            {"extraction": llm_override} if llm_override else None,
        )

        _require_crawl4ai()
        owns_crawler = crawler is None
        if owns_crawler:
            browser_config = _create_browser_config(headless)
            crawler = AsyncWebCrawler(config=browser_config)
        try:
            if owns_crawler:
                await crawler.start()
            return await self.execute(
                crawler,
                module,
                api_key,
                model,
                provider,
                temperature=temperature if temperature is not None else resolved_temperature,
                headless=headless,
                prompt_override=prompt_override,
            )
        finally:
            if owns_crawler:
                try:
                    await crawler.close()
                except Exception:
                    pass

    async def execute(
        self,
        crawler: Any,
        module: Module,
        api_key: str,
        model: str,
        provider: str,
        temperature: float = 0.0,
        headless: bool = True,
        prompt_override: str | None = None,
    ) -> List[ExtractedElement]:
        del headless
        from crawl4ai import CacheMode, CrawlerRunConfig, LLMConfig
        from crawl4ai.extraction_strategy import LLMExtractionStrategy

        prompt = prompt_override or self.prompt_manager.load_prompt("extraction")
        final_prompt = _append_context_block(
            _render_prompt(
                prompt,
                Test_Case_Structured=module,
                structured_test_case=module,
                module_context=module,
            ),
            {"structured_test_case": module, "module": module},
        )

        llm_strategy = LLMExtractionStrategy(
            llm_config=LLMConfig(provider=f"{provider}/{model}", api_token=api_key),
            schema=ExtractedElement.model_json_schema(),
            extraction_type="schema",
            input_format="html",
            extra_args={"temperature": temperature},
            instruction=final_prompt,
        )

        crawl_config = CrawlerRunConfig(
            verbose=True,
            word_count_threshold=1,
            extraction_strategy=llm_strategy,
            cache_mode=CacheMode.BYPASS,
            wait_until="domcontentloaded",
            page_timeout=120000,
            delay_before_return_html=0.5,
            screenshot=False,
        )

        result = await crawler.arun(url=module.url, config=crawl_config)
        if not result.success:
            error_message = getattr(result, "error_message", None) or f"Crawling failed for {module.url}"
            raise RuntimeError(error_message)

        html_snapshot = _extract_html_snapshot(result)
        if html_snapshot:
            module.source_html = _compact_html_snapshot(html_snapshot)

        extracted_items = json.loads(result.extracted_content)
        return [ExtractedElement(**item) for item in extracted_items]


__all__ = ["ExtractionStage"]
