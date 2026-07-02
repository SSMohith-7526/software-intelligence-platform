"""
backend/utils/language_detector.py
"""

from pathlib import Path
from collections import Counter
from typing import Dict, List

# -----------------------------------------
# Language Extensions
# -----------------------------------------

LANGUAGE_MAP = {
    ".py": "Python",
    ".java": "Java",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".c": "C",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".go": "Go",
    ".rs": "Rust",
    ".cs": "C#",
}

# -----------------------------------------
# Framework Detection
# -----------------------------------------

FRAMEWORK_FILES = {

    "FastAPI": ["fastapi"],

    "Flask": ["flask"],

    "Django": ["django"],

    "React": ["package.json"],

    "NextJS": ["next.config.js"],

    "Spring Boot": ["pom.xml"],

    "Gradle": ["build.gradle"],

    "Cargo": ["Cargo.toml"],

    "Flutter": ["pubspec.yaml"]

}

# -----------------------------------------
# Build Systems
# -----------------------------------------

BUILD_SYSTEMS = {

    "pom.xml": "Maven",

    "build.gradle": "Gradle",

    "package.json": "NPM",

    "Cargo.toml": "Cargo",

    "requirements.txt": "PIP"

}

# -----------------------------------------
# Entry Files
# -----------------------------------------

ENTRY_PRIORITY = [

    "main.py",

    "app.py",

    "server.py",

    "manage.py",

    "index.js",

    "main.cpp",

    "Main.java"

]

# -----------------------------------------
# Detect Languages
# -----------------------------------------

def detect_languages(repo_path: str) -> Dict:

    repo = Path(repo_path)

    counter = Counter()

    files = []

    for file in repo.rglob("*"):

        if file.is_file():

            files.append(file)

            ext = file.suffix.lower()

            if ext in LANGUAGE_MAP:

                counter[LANGUAGE_MAP[ext]] += 1

    return {

        "languages": dict(counter),

        "files": len(files)

    }

# -----------------------------------------
# Detect Framework
# -----------------------------------------

def detect_framework(repo_path: str) -> List[str]:

    repo = Path(repo_path)

    detected = []

    all_names = {

        f.name.lower()

        for f in repo.rglob("*")

    }

    for framework, indicators in FRAMEWORK_FILES.items():

        for item in indicators:

            if item.lower() in all_names:

                detected.append(framework)

                break

    return detected

# -----------------------------------------
# Detect Build System
# -----------------------------------------

def detect_build_system(repo_path: str):

    repo = Path(repo_path)

    names = {

        p.name

        for p in repo.rglob("*")

    }

    for build_file, system in BUILD_SYSTEMS.items():

        if build_file in names:

            return system

    return "Unknown"

# -----------------------------------------
# Detect Entry File
# -----------------------------------------

def detect_entry_file(repo_path: str):

    repo = Path(repo_path)

    files = {

        f.name: f

        for f in repo.rglob("*")

    }

    for entry in ENTRY_PRIORITY:

        if entry in files:

            return str(files[entry])

    return None

# -----------------------------------------
# Full Detection
# -----------------------------------------

def detect_repository(repo_path: str):

    return {

        "language": detect_languages(repo_path),

        "frameworks": detect_framework(repo_path),

        "build_system": detect_build_system(repo_path),

        "entry_point": detect_entry_file(repo_path)

    }