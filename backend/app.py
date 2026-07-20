"""Compatibility facade for the application layer."""

from pathlib import Path
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout, force=True)

CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
sys.path = [entry for entry in sys.path if entry not in {"", str(CURRENT_DIR)}]
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from backend.application.pipeline import (
    ConfirmationStage,
    ExecutionStage,
    ExtractionStage,
    FinalizationStage,
    GenIAOrchestrator,
    GenerationStage,
    HomologationStage,
    RefactoringStage,
    RefinementStage,
    StructuringStage,
    TestCase,
    ValidationStage,
    validate_llm_connection,
    get_available_frameworks,
    get_framework_languages,
    map_extracted_data_to_steps,
)
from backend.domain.models import (
    ExecutionResult,
    ExecutionStep,
    ExtractedElement,
    Module,
    PipelineSessionState,
    PipelineStage,
)

__all__ = [
    "ConfirmationStage",
    "ExecutionResult",
    "ExecutionStage",
    "ExecutionStep",
    "ExtractionStage",
    "ExtractedElement",
    "FinalizationStage",
    "GenIAOrchestrator",
    "GenerationStage",
    "HomologationStage",
    "Module",
    "PipelineSessionState",
    "PipelineStage",
    "RefactoringStage",
    "RefinementStage",
    "StructuringStage",
    "TestCase",
    "ValidationStage",
    "get_available_frameworks",
    "get_framework_languages",
    "map_extracted_data_to_steps",
    "validate_llm_connection",
]

logging.getLogger("genia.api").info("GenIA application facade imported")
