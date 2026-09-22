from pyinfra.api import deploy
from pyinfra.operations import flatpak

@deploy("Install RetroDeck")
def install_retrodeck():
    flatpak.packages(
        name="Install flatpak",
        packages="net.retrodeck.retrodeck",
    )
