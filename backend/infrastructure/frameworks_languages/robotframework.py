"""Robot Framework execution strategy."""

from __future__ import annotations

import re
import shutil
import uuid

from .base import BaseExecutionStrategy


class RobotFrameworkPythonExecutionStrategy(BaseExecutionStrategy):
    framework_name = "robotframework"
    supported_languages = ("python",)
    default_language = "python"

    def determine_filename(self, framework: str, script: str, language: str | None = None) -> str:
        return f"test_{uuid.uuid4().hex}.robot"

    def normalize_script(self, script: str, language: str | None = None) -> str:
        normalized = script.replace("\r\n", "\n")
        normalized = re.sub(
            r"(?m)^(\s*\$\{chrome_bin\}\s+)\$\{CHROME_BIN\}\s*$",
            r"\1%{CHROME_BIN}",
            normalized,
        )
        normalized = re.sub(
            r"(?m)^(\s*Run Keyword If\s+'\\$\\{chrome_bin\\}' != ''\s+Set Suite Variable\s+)\$\{chrome_options\.binary_location\}\s+\$\{chrome_bin\}\s*$",
            r"\1Evaluate    setattr($chrome_options, 'binary_location', $chrome_bin)",
            normalized,
        )
        normalized = re.sub(
            r"(?m)^(\s*Set Suite Variable\s+)\$\{chrome_options\.binary_location\}\s+\$\{chrome_bin\}\s*$",
            r"\1Evaluate    setattr($chrome_options, 'binary_location', $chrome_bin)",
            normalized,
        )
        return normalized

    def build_command(self, file_path: str, language: str | None = None, temp_dir: str | None = None) -> list[str]:
        python_cmd = self._python_command()
        listener_path = self._write_robot_listener(temp_dir or ".")
        robot_command = [python_cmd, "-m", "robot", "--listener", listener_path, file_path]
        if self._is_unix_like() and shutil.which("xvfb-run"):
            return ["xvfb-run", "-a", *robot_command]
        return robot_command
