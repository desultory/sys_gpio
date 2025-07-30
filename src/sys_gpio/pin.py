from contextlib import contextmanager
from pathlib import Path

from zenlib.logging import loggify

GPIO_PATH = Path("/sys/class/gpio")


@loggify
class Pin:
    DEFAULT_PIN_INDEX_OFFSET = 512
    def __init__(self, pin_number, pin_index_offset=None, *args, **kwargs):
        self.number = int(pin_number)
        self.pin_index_offset = int(pin_index_offset) if pin_index_offset is not None else self.DEFAULT_PIN_INDEX_OFFSET

    @classmethod
    def get_exports(cls):
        """Get all GPIO pin exports, using the system index"""
        for path in GPIO_PATH.glob("gpio*"):
            if str(path.name).startswith("gpiochip"):
                continue
            yield int(path.name[4:])

    def export(self):
        """Exports the pin if it is not already exported"""
        self.logger.info("Exporting pin: %d", self.number)
        if self.exported:
            self.logger.warning("Pin is already exported: %d", self.number)
            return
        with open(GPIO_PATH / "export", "wb") as f:
            f.write(str(self.pin_number).encode("ascii"))

    def unexport(self):
        """Unexports the pin if it is exported"""
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
        """Return the pin number used in the sysfs interface"""
        return self.number + self.pin_index_offset

    @property
    def pin_path(self):
        """Get the path of the current pin in sysfs"""
        return GPIO_PATH / f"gpio{self.pin_number}"

    def read_param(self, param_name):
        """Reads a parameter from /sys/class/gpio/gpioX/"""
        if not self.exported:
            self.export()

        with open(self.pin_path / param_name, "rb") as f:
            return f.read().decode("ascii").strip()

    def write_param(self, param_name, value):
        """Writes a parameter to /sys/class/gpio/gpioX/"""
        if not self.exported:
            self.export()

        with open(self.pin_path / param_name, "wb") as f:
            f.write(value.encode("ascii"))

    @property
    def value(self):
        """Gets the value of the pin"""
        return int(self.read_param("value"))

    @value.setter
    def value(self, value):
        """Sets the value of the pin, sets the direction to out if not already set"""
        if value not in [0, 1]:
            raise ValueError("Value must be either 0 or 1")
        if self.direction != "out":
            self.direction = "out"
        self.write_param("value", str(value))

    @property
    def direction(self):
        """Gets the direction of the pin"""
        return self.read_param("direction")

    @direction.setter
    def direction(self, value):
        """Sets the direction of the pin"""
        if value not in ["in", "out"]:
            raise ValueError("Direction must be either 'in' or 'out'")
        self.write_param("direction", value)

    @property
    def edge(self):
        """Gets the edge of the pin"""
        return self.read_param("edge")

    @edge.setter
    def edge(self, value):
        """Sets the edge of the pin"""
        if value not in ["none", "rising", "falling", "both"]:
            raise ValueError("Edge must be either 'none', 'rising', 'falling' or 'both'")
        self.write_param("edge", value)

    def poll_value(self, timeout=5):
        """Polls the value of the pin"""
        from select import select

        with open(self.pin_path / "value", "rb") as f:
            f.read()
            readable, _, exceptional = select([], [], [f], timeout)

    @contextmanager
    def on_rise(self, timeout=1):
        """Sets the edge to rising, and then polls the value until it changes.
        Yields 1 if the value ended high, 0 if the value ended low."""
        original_edge = self.edge
        self.edge = "rising"
        self.poll_value(timeout)
        if self.value == 0:
            yield 0
        else:
            yield 1
        self.edge = original_edge

    @contextmanager
    def on_fall(self, timeout=1):
        """Sets the edge to falling, and then polls the value until it changes.
        Yields 1 if the value ended low, 0 if the value ended high."""
        original_edge = self.edge
        self.edge = "falling"
        self.poll_value(timeout)
        if self.value == 1:
            yield 0
        else:
            yield 1
        self.edge = original_edge

    @contextmanager
    def on_change(self, timeout=1):
        """Sets the edge to both, and then polls the value until it changes"""
        original_edge = self.edge
        self.edge = "both"
        self.poll_value(timeout)
        yield 1
        self.edge = original_edge

    def __str__(self):
        return f"<Pin {self.number} direction={self.direction} value={self.value}>"
