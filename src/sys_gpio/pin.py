from pathlib import Path

from zenlib.logging import loggify

GPIO_PATH = Path("/sys/class/gpio")
GPIO_INDEX_OFFSET = 512


@loggify
class Pin:
    def __init__(self, pin_number, *args, **kwargs):
        self.number = int(pin_number)

    @classmethod
    def get_exports(cls):
        """ Get all GPIO pin exports, using the system index """
        for path in GPIO_PATH.glob("gpio*"):
            if str(path.name).startswith("gpiochip"):
                continue
            yield int(path.name[4:])

    def export(self):
        """ Exports the pin if it is not already exported """
        self.logger.info("Exporting pin: %d", self.number)
        if self.exported:
            self.logger.warning("Pin is already exported: %d", self.number)
            return
        with open(GPIO_PATH / "export", "wb") as f:
            f.write(str(self.pin_number).encode("ascii"))

    def unexport(self):
        """ Unexports the pin if it is exported """
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
        """ Return the pin number used in the sysfs interface """
        return self.number + GPIO_INDEX_OFFSET

    @property
    def pin_path(self):
        """ Get the path of the current pin in sysfs """
        return GPIO_PATH / f"gpio{self.pin_number}"

    def read_param(self, param_name):
        """ Reads a parameter from /sys/class/gpio/gpioX/ """
        if not self.exported:
            self.export()

        with open(self.pin_path / param_name, "rb") as f:
            return f.read().decode("ascii").strip()

    @property
    def value(self):
        """ Gets the value of the pin """
        return int(self.read_param("value"))

    @property
    def direction(self):
        """ Gets the direction of the pin """
        return self.read_param("direction")
