import calendar
import copy
from dataclasses import dataclass
from enum import StrEnum
import time
from typing import Callable

DEBUG = True


class Command(StrEnum):
    FILE_UPLOAD = "FILE_UPLOAD"
    FILE_GET = "FILE_GET"
    FILE_COPY = "FILE_COPY"
    FILE_SEARCH = "FILE_SEARCH"


@dataclass
class File:
    name: str
    size: int

    def __init__(self, name: str, size: str):
        self.name = name
        self.size = parse_size(size)

    def __str__(self) -> str:
        return self.name


# name -> File
data: dict[str, File] = {}
handlers: dict[str, Callable[..., str]] = {
    str(Command.FILE_UPLOAD): upload,
    str(Command.FILE_GET): get,
    str(Command.FILE_COPY): fscopy,
    str(Command.FILE_SEARCH): search,
}


def simulate_coding_framework(commands: list[list[str]]) -> list[str]:
    """
    Simulates a coding framework operation on a list of lists of strings.

    Parameters:
    commands (List[List[str]]): The list of commands and params
    """
    results: list[str] = []
    for command in commands:
        cmd, args = command[0], command[1:]
        fn = handlers[cmd]
        result = fn(*args)
        results.append(result)

    return results


def p(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def parse_size(s: str) -> int:
    size = 0
    if s.endswith("kb"):
        size = int(s[:-2])

    return size


def parse_timestamp(s: str) -> int:
    return calendar.timegm(time.strptime(s, "%Y-%m-%dT%H:%M:%S"))


def upload(name: str, size: str) -> str:
    if name in data:
        raise RuntimeError("File already exists")

    data[name] = File(name, size)
    return f"uploaded {name}"


def get(name: str) -> str:
    if name not in data:
        return ""

    return f"got {name}"


def fscopy(src: str, dest: str) -> str:
    if src not in data:
        raise RuntimeError(f"source file {src} doesn't exist")

    data[dest] = copy.copy(data[src])

    return f"copied {src} to {dest}"


def search(prefix: str) -> str:
    files: list[File] = []
    for key in data:
        if key.startswith(prefix):
            files.append(data[key])

    files = sorted(files, key=lambda f: f.size, reverse=True)[:10]
    p("search", files)
    file_names = ", ".join(f.name for f in files)
    return f"found [{file_names}]"
