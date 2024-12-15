from sys_gpio import Pin
from zenlib.util import get_kwargs


def get_pin_value():
    args = [
            {"flags": ["pin_number"], "help": "Pin to get value from", "action": "store", "type": int},
    ]

    kwargs = get_kwargs(package="sys_gpio", description="get pin value", arguments=args)
    pin = Pin(**kwargs)
    print(pin.value)

def get_pin_direction():
    args = [
            {"flags": ["pin_number"], "help": "Pin to get direction from", "action": "store", "type": int},
    ]

    kwargs = get_kwargs(package="sys_gpio", description="get pin direction", arguments=args)
    pin = Pin(**kwargs)
    print(pin.direction)

def get_pin_exports():
    print("Exported pins:" + ", ".join(Pin.get_exports()))
