import copy
from dataclasses import dataclass
from enum import StrEnum
from typing import Callable


class Command(StrEnum):
    FILE_UPLOAD = "FILE_UPLOAD"
    FILE_GET = "FILE_GET"
    FILE_COPY = "FILE_COPY"


@dataclass
class File:
    name: str
    size: str


def upload(name: str, size: int) -> str:
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


# name -> File
data: dict[str, File] = {}
handlers: dict[str, Callable[..., str]] = {
    str(Command.FILE_UPLOAD): upload,
    str(Command.FILE_GET): get,
    str(Command.FILE_COPY): fscopy,
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
