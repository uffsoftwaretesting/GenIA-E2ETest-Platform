"""Execution strategies for each framework/language combination."""

from .base import BaseExecutionStrategy, GenericPythonExecutionStrategy
from .cypress import CypressJavaScriptExecutionStrategy, CypressTypeScriptExecutionStrategy
from .junit import JUnitJavaExecutionStrategy
from .playwright import PlaywrightJavaScriptExecutionStrategy, PlaywrightTypeScriptExecutionStrategy
from .pytest import PytestPythonExecutionStrategy
from .registry import ExecutionStrategyRegistry
from .robotframework import RobotFrameworkPythonExecutionStrategy
from .selenium import (
    SeleniumJavaExecutionStrategy,
    SeleniumJavaScriptExecutionStrategy,
    SeleniumPythonExecutionStrategy,
    SeleniumTypeScriptExecutionStrategy,
)

__all__ = [
    "BaseExecutionStrategy",
    "GenericPythonExecutionStrategy",
    "ExecutionStrategyRegistry",
    "RobotFrameworkPythonExecutionStrategy",
    "PlaywrightJavaScriptExecutionStrategy",
    "PlaywrightTypeScriptExecutionStrategy",
    "CypressJavaScriptExecutionStrategy",
    "CypressTypeScriptExecutionStrategy",
    "PytestPythonExecutionStrategy",
    "JUnitJavaExecutionStrategy",
    "SeleniumPythonExecutionStrategy",
    "SeleniumJavaScriptExecutionStrategy",
    "SeleniumTypeScriptExecutionStrategy",
    "SeleniumJavaExecutionStrategy",
]
