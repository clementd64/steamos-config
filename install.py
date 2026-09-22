from pyinfra import host
from pyinfra.facts.files import Directory
from pyinfra.facts.server import Home
from tasks.novafix import install_novafix
from tasks.retrodeck import install_retrodeck
from tasks.sdgyrodsu import install_sdgyrodsu
from lib.steam import LocalConfig

if host.get_fact(Directory, path=f"{host.get_fact(Home)}/.steam") is not None:
    with LocalConfig() as local_config:
        install_novafix(local_config)

if host.data.get("install_retrodeck", False):
    install_retrodeck()

if host.data.get("install_sdgyrodsu", False):
    install_sdgyrodsu()
