from zenlib.util import get_kwargs

from sys_gpio import Pin


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


def set_pin_value():
    args = [
        {"flags": ["pin_number"], "help": "Pin to set value to", "action": "store", "type": int},
        {"flags": ["value"], "help": "Value to set", "action": "store", "type": int, "choices": [0, 1]},
    ]

    kwargs = get_kwargs(package="sys_gpio", description="set pin value", arguments=args)
    value = kwargs.pop("value")
    pin = Pin(**kwargs)
    pin.value = value


def set_pin_direction():
    args = [
        {"flags": ["pin_number"], "help": "Pin to set direction to", "action": "store", "type": int},
        {"flags": ["direction"], "help": "Direction to set", "action": "store", "choices": ["in", "out"]},
    ]

    kwargs = get_kwargs(package="sys_gpio", description="set pin direction", arguments=args)
    direction = kwargs.pop("direction")
    pin = Pin(**kwargs)
    pin.direction = direction


def get_pin_exports():
    print("Exported pins:" + ", ".join(list(Pin.get_exports())))
