from __future__ import annotations

import unittest

from backend.application.pipeline import GenIAOrchestrator
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


class BackendRefactorSmokeTest(unittest.TestCase):
    def test_orchestrator_is_available_from_compatibility_facade(self) -> None:
        self.assertEqual(GenIAOrchestrator.__name__, "GenIAOrchestrator")

    def test_stage_modules_resolve_to_expected_classes(self) -> None:
        expected = {
            StructuringStage.__name__,
            ExtractionStage.__name__,
            RefinementStage.__name__,
            GenerationStage.__name__,
            ValidationStage.__name__,
            ConfirmationStage.__name__,
            ExecutionStage.__name__,
            HomologationStage.__name__,
            FinalizationStage.__name__,
            RefactoringStage.__name__,
        }
        self.assertEqual(
            expected,
            {
                "StructuringStage",
                "ExtractionStage",
                "RefinementStage",
                "GenerationStage",
                "ValidationStage",
                "ConfirmationStage",
                "ExecutionStage",
                "HomologationStage",
                "FinalizationStage",
                "RefactoringStage",
            },
        )


if __name__ == "__main__":
    unittest.main()
