from pathlib import PurePosixPath

from pyinfra import host
from pyinfra.api import deploy
from pyinfra.facts.files import Directory, FindFiles
from pyinfra.operations import files
from lib import steam


GRID_FILES = {
    "292140p.png": (
        "https://cdn2.steamgriddb.com/grid/27ca10d5e1017db90da4c60bd352a5b4.png",
        "68503783d5b99fd34f0389b0a8e587fecf25e9cf8e6ba8e0d822a9bb6a88a63f",
    ),
    "292140_hero.jpg": (
        "https://cdn2.steamgriddb.com/hero/116dc4b9cd1faf32bc3bb9d47be29a22.jpg",
        "831b0b0e133979070ab47195b791123fbe7277ebf45411b2acf9acd6d7904c78",
    ),
    "345350p.png": (
        "https://cdn2.steamgriddb.com/grid/7baf695c128c49ef645ca814a3ad7fb6.png",
        "b9cf68a02cb612a4211118d58fd28f6efab84764891b9dc961bc727bcea4e7dc",
    ),
    "345350_hero.png": (
        "https://cdn2.steamgriddb.com/hero/197559967b14279a504f8f1018607491.png",
        "7dccd748dc818db343539e5050e85ec472219b045338d1a420946f2debcb52f8",
    ),
}


@deploy("Sync Steam grid artwork")
def sync_grid():
    grid_dir = f"{steam.root_dir()}/userdata/{steam.user_id()}/config/grid"

    existing_files = (
        host.get_fact(FindFiles, path=grid_dir, maxdepth=1)
        if host.get_fact(Directory, path=grid_dir)
        else []
    )

    files.directory(name="Ensure Steam grid directory exists", path=grid_dir)

    for filename, (url, sha256sum) in GRID_FILES.items():
        files.download(
            name=f"Download grid artwork {filename}",
            src=url,
            dest=f"{grid_dir}/{filename}",
            sha256sum=sha256sum,
        )

    for path in existing_files:
        if PurePosixPath(path).name not in GRID_FILES:
            files.file(name=f"Remove unlisted grid artwork {path}", path=path, present=False)
