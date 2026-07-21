"""Compatibility facade for the application pipeline."""

from backend.domain.frameworks import get_available_frameworks, get_framework_languages
from backend.domain.models import TestCase
from backend.pipelines.genia_orchestrator import GenIAOrchestrator, map_extracted_data_to_steps, validate_llm_connection
from backend.pipelines.stages.confirmation import ConfirmationStage
from backend.pipelines.stages.execution import ExecutionStage
from backend.pipelines.stages.extraction import ExtractionStage
from backend.pipelines.stages.finalization import FinalizationStage
from backend.pipelines.stages.generation import GenerationStage
from backend.pipelines.stages.homologation import HomologationStage
from backend.pipelines.stages.refactoring import RefactoringStage
from backend.pipelines.stages.refinement import RefinementStage
from backend.pipelines.stages.structuring import StructuringStage
from backend.pipelines.stages.validation import ValidationStage

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
