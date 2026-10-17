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

    FILE_UPLOAD_AT = "FILE_UPLOAD_AT"
    FILE_GET_AT = "FILE_GET_AT"
    FILE_COPY_AT = "FILE_COPY_AT"
    FILE_SEARCH_AT = "FILE_SEARCH_AT"


@dataclass
class File:
    name: str
    size: int
    avail_from: int
    avail_to: int | None  # inclusive

    def __init__(self, name: str, size: str, now: int, ttl: int | None):
        self.name = name
        self.size = parse_size(size)

        if ttl is None:
            self.avail_from = now
        else:
            self.avail_to = now + ttl

    def __str__(self) -> str:
        return self.name

    def is_available(self, ts: int) -> bool:
        exist_yet = self.avail_from <= ts
        exist_still = (self.avail_to is None) or (ts <= self.avail_to)
        return exist_yet and exist_still


# name -> File
data: dict[str, File] = {}


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

    data[name] = File(name, size, 0, None)
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


def upload_at(timestamp: str, name: str, size: str, ttl: None | int = None) -> str:
    ts = parse_timestamp(timestamp)

    if in_fs(name, ts):
        raise RuntimeError("File already exists")

    data[name] = File(name, size, ts, ttl)
    return f"uploaded at {name}"


def get_at(timestamp: str, name: str) -> str:
    ts = parse_timestamp(timestamp)
    if not in_fs(name, ts):
        return ""

    return f"got at {name}"


def fscopy_at(timestamp: str, src: str, dest: str) -> str:
    ts = parse_timestamp(timestamp)
    if not in_fs(src, ts):
        raise RuntimeError(f"source file {src} doesn't exist")

    data[dest] = copy.copy(data[src])

    return f"copied at {src} to {dest}"


def search_at(timestamp: str, prefix: str) -> str:
    ts = parse_timestamp(timestamp)

    files: list[File] = []
    for name in data:
        if in_fs(name, ts) and name.startswith(prefix):
            files.append(data[name])

    files = sorted(files, key=lambda f: f.size, reverse=True)[:10]
    p("search at", files)
    file_names = ", ".join(f.name for f in files)
    return f"found at [{file_names}]"


def in_fs(name: str, ts: int):
    return name in data and data[name].is_available(ts)


handlers: dict[str, Callable[..., str]] = {
    str(Command.FILE_UPLOAD): upload,
    str(Command.FILE_GET): get,
    str(Command.FILE_COPY): fscopy,
    str(Command.FILE_SEARCH): search,
    str(Command.FILE_UPLOAD_AT): upload_at,
    str(Command.FILE_GET_AT): get_at,
    str(Command.FILE_COPY_AT): fscopy_at,
    str(Command.FILE_SEARCH_AT): search_at,
}
