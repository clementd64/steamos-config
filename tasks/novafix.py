from pathlib import PurePosixPath

from pyinfra import host
from pyinfra.api import deploy
from pyinfra.facts.files import File
from pyinfra.operations import files
from lib import steam


RELEASE_URL = "https://github.com/Kartin8/FF13NovaFix/releases/download/v1.0.1/d3d9.dll"
RELEASE_SHA256 = "7522fdde7b42e28ed1344bfa6ea4c5c6dee3b14669ef465463b06436ec2c9938"


def install_game(app_id, executable, local_config: steam.LocalConfig):
    library, manifest = steam.read_appmanifest(app_id)
    install_dir = manifest.get("AppState", {}).get("installdir")
    if not install_dir:
        return

    game_exe = PurePosixPath(library, "steamapps/common", install_dir, executable)
    if not host.get_fact(File, path=str(game_exe)):
        return

    (
        local_config
        .child("UserLocalConfigStore")
        .child("Software")
        .child("Valve")
        .child("Steam")
        .child("apps")
        .child(app_id)
        .set("LaunchOptions", 'WINEDLLOVERRIDES="d3d9=n,b" %command%')
    )

    files.download(
        name=f"Install FF13NovaFix for {manifest.get('AppState', {}).get('name')}",
        src=RELEASE_URL,
        dest=str(game_exe.parent / "d3d9.dll"),
        sha256sum=RELEASE_SHA256,
    )


@deploy("Install FF13NovaFix")
def install_novafix(local_config: steam.LocalConfig):
    install_game("292120", "white_data/prog/win/bin/ffxiiiimg.exe", local_config)
    install_game("292140", "alba_data/prog/win/bin/ffxiii2img.exe", local_config)
    install_game("345350", "LRFF13.exe", local_config)
