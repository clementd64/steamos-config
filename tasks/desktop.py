from pyinfra import host
from pyinfra.api import deploy
from pyinfra.facts.server import Home
from pyinfra.operations import files


@deploy("Install desktop shortcuts")
def install_desktop_shortcuts():
    desktop = f"{host.get_fact(Home)}/Desktop"
    files.directory(
        name="Ensure desktop directory exists",
        path=desktop,
    )
    files.put(
        name="Install Start SSH desktop shortcut",
        src="files/start-sshd.desktop",
        dest=f"{desktop}/start-sshd.desktop",
        mode="0755",
    )
