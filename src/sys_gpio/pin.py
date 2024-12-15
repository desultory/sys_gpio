from pathlib import Path

from zenlib.logging import loggify

GPIO_PATH = Path("/sys/class/gpio")
GPIO_INDEX_OFFSET = 512


@loggify
class Pin:
    def __init__(self, number, *args, **kwargs):
        self.number = number

    @classmethod
    def get_exports(cls):
        for path in GPIO_PATH.glob("gpio*"):
            if str(path.name).startswith("gpiochip"):
                continue
            yield int(path.name[4:])

    def export(self):
        self.logger.info("Exporting pin: %d", self.number)
        if self.exported:
            self.logger.warning("Pin is already exported: %d", self.number)
            return
        with open(GPIO_PATH / "export", "wb") as f:
            f.write(str(self.pin_number).encode("ascii"))

    def unexport(self):
        self.logger.info("Unexporting pin: %d", self.number)
        if not self.exported:
            self.logger.warning("Pin is not exported: %d", self.number)
            return
        with open(GPIO_PATH / "unexport", "wb") as f:
            f.write(str(self.pin_number).encode("ascii"))

    @property
    def exported(self):
        return self.pin_number in self.get_exports()

    @property
    def pin_number(self):
        return int(self.number + GPIO_INDEX_OFFSET)

    @property
    def pin_path(self):
        return GPIO_PATH / f"gpio{self.pin_number}"

    def read_param(self, param_name):
        if not self.exported:
            self.export()

        with open(self.pin_path / param_name, "rb") as f:
            return f.read().decode("ascii").strip()

    @property
    def value(self):
        return int(self.read_param("value"))

    @property
    def direction(self):
        return self.read_param("direction")
