from copy import deepcopy
from io import StringIO
from pathlib import PurePosixPath
from functools import cache

import vdf

from pyinfra import host
from pyinfra.facts.files import FileContents, FindDirectories
from pyinfra.facts.server import Command, Home
from pyinfra.operations import files


def read_vdf(path):
    lines = host.get_fact(FileContents, path=path)
    return vdf.loads("\n".join(lines) + "\n", escaped=True) if lines else {}


@cache
def root_dir():
    return f"{host.get_fact(Home)}/.steam/steam"


@cache
def libraries():
    libraries = set()
    libraryfolders = read_vdf(f"{root_dir()}/steamapps/libraryfolders.vdf")
    for library in libraryfolders.get("libraryfolders", {}).values():
        if isinstance(library, dict) and "path" in library:
            libraries.add(library["path"])
    if not libraries:
        libraries.add(root_dir())

    return sorted(libraries)


def read_appmanifest(app_id):
    for library in libraries():
        manifest = read_vdf(f"{library}/steamapps/appmanifest_{app_id}.acf")
        if manifest:
            return library, manifest
    return None, {}


@cache
def user_id():
    user_dirs = [
        path
        for path in host.get_fact(FindDirectories, path=f"{root_dir()}/userdata", maxdepth=1)
        if PurePosixPath(path).name.isdecimal()
    ]
    if len(user_dirs) == 0:
        raise RuntimeError("No Steam user directories found.")
    if len(user_dirs) > 1:
        raise RuntimeError("Multiple Steam user directories found.")
    return int(PurePosixPath(user_dirs[0]).name)


class _ConfigNode:
    def __init__(self, mapping):
        self.mapping = mapping

    @staticmethod
    def _matching_key(mapping, key):
        return next((existing for existing in mapping if existing.lower() == key.lower()), key)

    def get(self, key):
        mapping = self.mapping.setdefault(self._matching_key(self.mapping, key), {})
        return _ConfigNode(mapping)

    def set(self, key, value):
        self.mapping[self._matching_key(self.mapping, key)] = value
        return self


class LocalConfig():
    def __init__(self):
        self.path = ""
        self.config = None
        self.original_config = None

    def get(self, key):
        return _ConfigNode(self.config).get(key)

    def set(self, key, value):
        _ConfigNode(self.config).set(key, value)
        return self

    def __enter__(self):
        self.path = f"{root_dir()}/userdata/{user_id()}/config/localconfig.vdf"
        self.config = read_vdf(self.path)
        if not self.config:
            return
        self.original_config = deepcopy(self.config)
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_type:
            return

        if self.config == self.original_config:
            return

        if host.get_fact(
            Command,
            command='pgrep -x -u "$(id -u)" steam || test "$?" -eq 1',
        ):
            raise RuntimeError("Exit Steam and rerun to update local config.")

        files.put(
            name="Configure Steam local config",
            src=StringIO(vdf.dumps(self.config, pretty=True, escaped=True)),
            dest=self.path,
        )
