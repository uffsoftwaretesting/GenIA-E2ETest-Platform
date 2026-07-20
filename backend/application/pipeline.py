"""Compatibility facade for the application pipeline."""

from backend.pipelines.genia_orchestrator import (
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

__all__ = [
    "ConfirmationStage",
    "ExecutionStage",
    "ExtractionStage",
    "FinalizationStage",
    "GenIAOrchestrator",
    "GenerationStage",
    "HomologationStage",
    "RefactoringStage",
    "RefinementStage",
    "StructuringStage",
    "TestCase",
    "ValidationStage",
    "validate_llm_connection",
    "get_available_frameworks",
    "get_framework_languages",
    "map_extracted_data_to_steps",
]
