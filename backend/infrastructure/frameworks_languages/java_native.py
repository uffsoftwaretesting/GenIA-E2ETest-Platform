"""Helpers to compile and execute native Java test sources."""

from __future__ import annotations

import os
import re
import shutil
from functools import lru_cache
from pathlib import Path


def discover_java_executable() -> str | None:
    candidate = shutil.which("java")
    if candidate:
        return candidate
    return None


def discover_javac_executable() -> str | None:
    candidate = shutil.which("javac")
    if candidate:
        return candidate
    return None


def discover_chromedriver_executable() -> str | None:
    candidates = [
        shutil.which("chromedriver"),
        shutil.which("msedgedriver"),
        os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"), "Google", "Chrome", "Application", "chromedriver.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"), "Google", "Chrome", "Application", "chromedriver.exe"),
        os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"), "Google", "Chrome", "Application", "Chrome for Testing", "chromedriver.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"), "Google", "Chrome", "Application", "Chrome for Testing", "chromedriver.exe"),
    ]
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate
    return None


def extract_java_package_name(source: str) -> str | None:
    match = re.search(r"^\s*package\s+([A-Za-z_][\w.]*)\s*;", source, flags=re.M)
    if match:
        return match.group(1).strip()
    return None


def extract_java_primary_class_name(source: str) -> str | None:
    cleaned = source.replace("\r\n", "\n")
    patterns = [
        r"^\s*public\s+(?:final\s+)?(?:class|record|interface|enum)\s+([A-Za-z_][\w]*)\b",
        r"^\s*(?:final\s+)?(?:class|record|interface|enum)\s+([A-Za-z_][\w]*)\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, cleaned, flags=re.M)
        if match:
            return match.group(1)
    return None


@lru_cache(maxsize=1)
def discover_java_classpath_entries() -> list[str]:
    roots = [
        Path.home() / ".m2" / "repository",
        Path.home() / ".m2" / ".lemminx-maven",
    ]

    desired_artifacts = [
        ("org/junit/jupiter", "junit-jupiter-api"),
        ("org/apiguardian", "apiguardian-api"),
        ("org/opentest4j", "opentest4j"),
        ("com/google/guava", "guava"),
        ("com/google/auto/service", "auto-service-annotations"),
        ("net/bytebuddy", "byte-buddy"),
        ("io/opentelemetry", "opentelemetry-api"),
        ("io/opentelemetry", "opentelemetry-context"),
        ("io/opentelemetry", "opentelemetry-exporter-logging"),
        ("io/opentelemetry", "opentelemetry-sdk-common"),
        ("io/opentelemetry", "opentelemetry-sdk-extension-autoconfigure-spi"),
        ("io/opentelemetry", "opentelemetry-sdk-extension-autoconfigure"),
        ("io/opentelemetry", "opentelemetry-sdk-trace"),
        ("io/opentelemetry", "opentelemetry-sdk"),
        ("io/opentelemetry", "opentelemetry-semconv"),
        ("org/seleniumhq/selenium", "selenium-api"),
        ("org/seleniumhq/selenium", "selenium-http"),
        ("org/seleniumhq/selenium", "selenium-chrome-driver"),
        ("org/seleniumhq/selenium", "selenium-remote-driver"),
        ("org/seleniumhq/selenium", "selenium-support"),
        ("org/seleniumhq/selenium", "selenium-json"),
        ("org/seleniumhq/selenium", "selenium-chromium-driver"),
        ("org/seleniumhq/selenium", "selenium-manager"),
        ("org/seleniumhq/selenium", "selenium-os"),
    ]

    def version_key(version: str) -> tuple:
        parts = re.findall(r"\d+|[A-Za-z]+", version)
        key: list[tuple[int, object]] = []
        for part in parts:
            if part.isdigit():
                key.append((0, int(part)))
            else:
                key.append((1, part.lower()))
        return tuple(key)

    def is_relevant(path: Path) -> bool:
        lowered = path.as_posix().lower()
        return any(
            marker in lowered
            for marker in (
                "/org/junit/",
                "/org/apiguardian/",
                "/org/opentest4j/",
                "/com/google/guava/",
                "/com/google/auto/service/",
                "/net/bytebuddy/",
                "/io/opentelemetry/",
                "/org/seleniumhq/selenium/",
            )
        )

    def find_latest_jar(group_path: str, artifact: str) -> str | None:
        best_path: Path | None = None
        best_version: tuple | None = None
        for root in roots:
            group_root = root / group_path
            if not group_root.exists():
                continue
            for path in group_root.rglob(f"{artifact}-*.jar"):
                if not path.is_file():
                    continue
                lowered = path.name.lower()
                if lowered.endswith("-sources.jar") or lowered.endswith("-javadoc.jar"):
                    continue
                if not is_relevant(path):
                    continue
                version = path.parent.name
                current_key = version_key(version)
                if best_version is None or current_key > best_version:
                    best_version = current_key
                    best_path = path
        return str(best_path) if best_path else None

    jars: list[str] = []
    seen: set[str] = set()
    for group_path, artifact in desired_artifacts:
        candidate = find_latest_jar(group_path, artifact)
        if candidate and candidate not in seen:
            seen.add(candidate)
            jars.append(candidate)

    return jars


def validate_java_dependencies() -> tuple[bool, list[str]]:
    entries = discover_java_classpath_entries()
    required_markers = {
        "junit-jupiter-api": False,
        "apiguardian-api": False,
        "opentest4j": False,
        "guava": False,
        "byte-buddy": False,
        "opentelemetry-api": False,
        "opentelemetry-context": False,
        "opentelemetry-sdk": False,
        "selenium-api": False,
        "selenium-http": False,
        "selenium-remote-driver": False,
        "selenium-chrome-driver": False,
        "selenium-support": False,
        "selenium-json": False,
        "selenium-manager": False,
        "selenium-os": False,
    }

    for entry in entries:
        lowered = entry.replace("\\", "/").lower()
        for marker in required_markers:
            if marker in lowered:
                required_markers[marker] = True

    missing = [marker for marker, present in required_markers.items() if not present]
    return not missing, missing


def build_java_classpath(*extra_entries: str) -> str:
    entries = [entry for entry in extra_entries if entry]
    entries.extend(discover_java_classpath_entries())
    unique_entries: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        normalized = str(Path(entry))
        if normalized in seen:
            continue
        seen.add(normalized)
        unique_entries.append(normalized)
    return os.pathsep.join(unique_entries)


def build_junit_runner_source() -> str:
    return """
import java.lang.annotation.Annotation;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.List;

public class GeniaJUnitRunner {
    private static boolean hasAnnotation(Method method, String annotationName) {
        for (Annotation annotation : method.getAnnotations()) {
            if (annotation.annotationType().getName().equals(annotationName)) {
                return true;
            }
        }
        return false;
    }

    private static List<Method> collectMethods(Class<?> clazz, String annotationName) {
        List<Method> methods = new ArrayList<>();
        for (Method method : clazz.getDeclaredMethods()) {
            if (hasAnnotation(method, annotationName)) {
                method.setAccessible(true);
                methods.add(method);
            }
        }
        return methods;
    }

    private static Method findMainMethod(Class<?> clazz) {
        try {
            Method method = clazz.getMethod("main", String[].class);
            if (Modifier.isStatic(method.getModifiers())) {
                method.setAccessible(true);
                return method;
            }
        } catch (NoSuchMethodException ignored) {
        }
        return null;
    }

    private static Object newInstance(Class<?> clazz) throws Exception {
        var constructor = clazz.getDeclaredConstructor();
        constructor.setAccessible(true);
        return constructor.newInstance();
    }

    private static void invokeAll(List<Method> methods, Object target) throws Exception {
        for (Method method : methods) {
            try {
                if (Modifier.isStatic(method.getModifiers())) {
                    method.invoke(null);
                } else {
                    method.invoke(target);
                }
            } catch (InvocationTargetException ex) {
                Throwable cause = ex.getCause() != null ? ex.getCause() : ex;
                throw new RuntimeException(cause);
            }
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length == 0) {
            System.err.println("[GENIA-JAVA] Missing test class name");
            System.exit(2);
        }

        Class<?> testClass = Class.forName(args[0]);
        List<Method> beforeAll = collectMethods(testClass, "org.junit.jupiter.api.BeforeAll");
        List<Method> afterAll = collectMethods(testClass, "org.junit.jupiter.api.AfterAll");
        List<Method> beforeEach = collectMethods(testClass, "org.junit.jupiter.api.BeforeEach");
        List<Method> afterEach = collectMethods(testClass, "org.junit.jupiter.api.AfterEach");
        List<Method> tests = new ArrayList<>();
        for (Method method : testClass.getDeclaredMethods()) {
            if (hasAnnotation(method, "org.junit.jupiter.api.Test") || hasAnnotation(method, "org.junit.jupiter.params.ParameterizedTest")) {
                method.setAccessible(true);
                tests.add(method);
            }
        }

        if (tests.isEmpty()) {
            Method mainMethod = findMainMethod(testClass);
            if (mainMethod != null) {
                mainMethod.invoke(null, (Object) new String[0]);
                return;
            }
            System.out.println("[GENIA-JAVA] No @Test methods found");
            return;
        }

        int failures = 0;
        Object beforeAllTarget = null;
        if (!beforeAll.isEmpty() || !afterAll.isEmpty()) {
            try {
                beforeAllTarget = newInstance(testClass);
            } catch (Exception ignored) {
                beforeAllTarget = null;
            }
        }

        try {
            if (beforeAllTarget != null) {
                invokeAll(beforeAll, beforeAllTarget);
            } else {
                invokeAll(beforeAll, null);
            }
        } catch (Exception ex) {
            failures++;
            System.err.println("[GENIA-JAVA] Failed during @BeforeAll: " + ex.getMessage());
            ex.printStackTrace();
        }

        for (Method testMethod : tests) {
            Object testInstance = null;
            if (!Modifier.isStatic(testMethod.getModifiers())) {
                testInstance = newInstance(testClass);
            }

            try {
                invokeAll(beforeEach, testInstance);
                if (Modifier.isStatic(testMethod.getModifiers())) {
                    testMethod.invoke(null);
                } else {
                    testMethod.invoke(testInstance);
                }
                System.out.println("[GENIA-JAVA] PASSED " + testMethod.getName());
            } catch (InvocationTargetException ex) {
                failures++;
                Throwable cause = ex.getCause() != null ? ex.getCause() : ex;
                System.err.println("[GENIA-JAVA] FAILED " + testMethod.getName() + ": " + cause);
                cause.printStackTrace();
            } catch (Exception ex) {
                failures++;
                System.err.println("[GENIA-JAVA] FAILED " + testMethod.getName() + ": " + ex);
                ex.printStackTrace();
            } finally {
                try {
                    invokeAll(afterEach, testInstance);
                } catch (Exception ex) {
                    failures++;
                    System.err.println("[GENIA-JAVA] FAILED during @AfterEach for " + testMethod.getName() + ": " + ex);
                    ex.printStackTrace();
                }
            }
        }

        try {
            if (beforeAllTarget != null) {
                invokeAll(afterAll, beforeAllTarget);
            } else {
                invokeAll(afterAll, null);
            }
        } catch (Exception ex) {
            failures++;
            System.err.println("[GENIA-JAVA] Failed during @AfterAll: " + ex.getMessage());
            ex.printStackTrace();
        }

        if (failures > 0) {
            System.exit(1);
        }
    }
}
""".strip()
