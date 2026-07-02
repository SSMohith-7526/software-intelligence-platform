"""
============================================================
Software Intelligence Platform

Common Helper Functions

Used by every AI Agent.

Author : SSM
============================================================
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import time
import uuid
from functools import wraps
from pathlib import Path
from typing import Any, Callable


# ---------------------------------------------------------
# UUID
# ---------------------------------------------------------

def generate_uuid() -> str:
    """Generate unique ID."""

    return str(uuid.uuid4())


# ---------------------------------------------------------
# Timestamp
# ---------------------------------------------------------

def current_timestamp() -> float:
    return time.time()


# ---------------------------------------------------------
# SHA256
# ---------------------------------------------------------

def sha256_file(file_path: str | Path) -> str:

    sha = hashlib.sha256()

    with open(file_path, "rb") as f:

        while chunk := f.read(8192):

            sha.update(chunk)

    return sha.hexdigest()


# ---------------------------------------------------------
# JSON
# ---------------------------------------------------------

def load_json(file_path: str | Path) -> dict:

    with open(file_path, "r", encoding="utf8") as f:

        return json.load(f)


def save_json(data: dict, file_path: str | Path):

    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf8") as f:

        json.dump(data, f, indent=4)


# ---------------------------------------------------------
# Pretty JSON
# ---------------------------------------------------------

def pretty_json(data: dict) -> str:

    return json.dumps(data, indent=4)


# ---------------------------------------------------------
# Safe File Read
# ---------------------------------------------------------

def read_file(file_path: str | Path) -> str:

    with open(file_path, encoding="utf8", errors="ignore") as f:

        return f.read()


# ---------------------------------------------------------
# Safe File Write
# ---------------------------------------------------------

def write_file(file_path: str | Path, content: str):

    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf8") as f:

        f.write(content)


# ---------------------------------------------------------
# Directory
# ---------------------------------------------------------

def ensure_directory(path: str | Path):

    Path(path).mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# Remove Folder
# ---------------------------------------------------------

def remove_directory(path: str | Path):

    if Path(path).exists():

        shutil.rmtree(path)


# ---------------------------------------------------------
# Copy Folder
# ---------------------------------------------------------

def copy_directory(src: str | Path, dst: str | Path):

    shutil.copytree(src, dst, dirs_exist_ok=True)


# ---------------------------------------------------------
# Retry Decorator
# ---------------------------------------------------------

def retry(max_retry=3, delay=1):

    def decorator(func):

        @wraps(func)

        def wrapper(*args, **kwargs):

            last_exception = None

            for _ in range(max_retry):

                try:

                    return func(*args, **kwargs)

                except Exception as e:

                    last_exception = e

                    time.sleep(delay)

            raise last_exception

        return wrapper

    return decorator


# ---------------------------------------------------------
# Timer
# ---------------------------------------------------------

def timer(func):

    @wraps(func)

    def wrapper(*args, **kwargs):

        start = time.perf_counter()

        result = func(*args, **kwargs)

        elapsed = time.perf_counter() - start

        print(f"{func.__name__} : {elapsed:.4f} sec")

        return result

    return wrapper


# ---------------------------------------------------------
# File Size
# ---------------------------------------------------------

def format_size(size: int):

    units = ["B", "KB", "MB", "GB"]

    index = 0

    while size >= 1024 and index < len(units)-1:

        size /= 1024

        index += 1

    return f"{size:.2f} {units[index]}"


# ---------------------------------------------------------
# Chunk List
# ---------------------------------------------------------

def chunk_list(data: list, chunk_size: int):

    for i in range(0, len(data), chunk_size):

        yield data[i:i+chunk_size]


# ---------------------------------------------------------
# Deep Merge
# ---------------------------------------------------------

def deep_merge(a: dict, b: dict):

    result = dict(a)

    for k, v in b.items():

        if (
            k in result
            and isinstance(result[k], dict)
            and isinstance(v, dict)
        ):

            result[k] = deep_merge(result[k], v)

        else:

            result[k] = v

    return result


# ---------------------------------------------------------
# File Extension
# ---------------------------------------------------------

def extension(path: str):

    return Path(path).suffix.lower()


# ---------------------------------------------------------
# File Exists
# ---------------------------------------------------------

def exists(path: str):

    return Path(path).exists()


# ---------------------------------------------------------
# List Files
# ---------------------------------------------------------

def list_files(folder: str):

    return [

        str(p)

        for p in Path(folder).rglob("*")

        if p.is_file()

    ]