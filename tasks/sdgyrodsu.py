from pyinfra.api import deploy
from pyinfra.operations import files, server
from pyinfra.operations import systemd

@deploy("Install SteamDeckGyroDSU")
def install_sdgyrodsu():
    for dir in [".local/share/sdgyrodsu", ".config/systemd/user"]:
        files.directory(
            name=f"Ensure {dir} exists",
            path=dir,
            present=True,
        )

    files.download(
        name=f"Download release",
        src="https://github.com/kmicki/SteamDeckGyroDSU/releases/latest/download/SteamDeckGyroDSUSetup.zip",
        dest="/tmp/SteamDeckGyroDSUSetup.zip",
    )

    server.shell(
        name="Extract",
        _chdir=".local/share/sdgyrodsu",
        commands=[
            "unzip -j -o /tmp/SteamDeckGyroDSUSetup.zip SteamDeckGyroDSUSetup/sdgyrodsu",
        ],
    )

    files.file(
        name="Ensure sdgyrodsu is executable",
        path=".local/share/sdgyrodsu/sdgyrodsu",
        mode="0755",
    )

    files.put(
        name="Ensure systemd service file",
        src="files/sdgyrodsu.service",
        dest=".config/systemd/user/sdgyrodsu.service",
    )

    systemd.service(
        name="Enable and start sdgyrodsu",
        service="sdgyrodsu",
        daemon_reload=True,
        enabled=True,
        restarted=True,
        running=True,
        user_mode=True,
    )
