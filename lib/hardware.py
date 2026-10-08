from pyinfra.api import FactBase

class Model(FactBase):
    def command(self) -> str:
        return "cat /sys/class/dmi/id/product_name"
