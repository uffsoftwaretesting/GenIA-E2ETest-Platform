from __future__ import annotations

import unittest

from backend.infrastructure.frameworks_languages.java_native import (
    extract_java_package_name,
    extract_java_primary_class_name,
)
from backend.infrastructure.frameworks_languages.junit import JUnitJavaExecutionStrategy


class JUnitJavaNativeStrategyTest(unittest.TestCase):
    def test_determine_filename_uses_public_class_name(self) -> None:
        strategy = JUnitJavaExecutionStrategy()
        script = """
        import org.junit.jupiter.api.Test;

        public class LoginFlowTest {
            @Test
            void should_run() {}
        }
        """

        self.assertEqual(strategy.determine_filename("junit", script, "java"), "LoginFlowTest.java")

    def test_java_helpers_extract_package_and_class(self) -> None:
        script = """
        package com.example.tests;

        public class CheckoutTest {
        }
        """

        self.assertEqual(extract_java_package_name(script), "com.example.tests")
        self.assertEqual(extract_java_primary_class_name(script), "CheckoutTest")

    def test_normalize_script_strips_markdown_fences(self) -> None:
        strategy = JUnitJavaExecutionStrategy()
        script = "```java\npublic class SampleTest {}\n```"

        normalized = strategy.normalize_script(script, "java")

        self.assertNotIn("```", normalized)
        self.assertIn("public class SampleTest {}", normalized)

    def test_normalize_script_converts_integer_waits_to_duration(self) -> None:
        strategy = JUnitJavaExecutionStrategy()
        script = """
        import org.openqa.selenium.WebDriver;
        import org.openqa.selenium.support.ui.WebDriverWait;

        public class SampleTest {
            private WebDriverWait wait;

            public void setup(WebDriver driver) {
                wait = new WebDriverWait(driver, 10);
            }
        }
        """

        normalized = strategy.normalize_script(script, "java")

        self.assertIn("new WebDriverWait(driver, Duration.ofSeconds(10))", normalized)
        self.assertIn("import java.time.Duration;", normalized)


if __name__ == "__main__":
    unittest.main()
