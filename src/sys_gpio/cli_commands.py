from zenlib.util import get_kwargs

from sys_gpio import Pin

DEFAULT_ARGS = [
    {"flags": ["pin_number"], "help": "Pin number to operate on", "action": "store", "type": int},
    {
        "flags": ["--pin-offset"],
        "help": "Pin index offset for exporting, defaults to 512 for Raspberry Pi",
        "dest": "pin_index_offset",
        "action": "store",
        "type": int,
        "default": 512,
    },
]


def get_pin_value():
    kwargs = get_kwargs(package="sys_gpio", description="get pin value", arguments=DEFAULT_ARGS)
    pin = Pin(**kwargs)
    print(pin.value)


def get_pin_direction():
    kwargs = get_kwargs(package="sys_gpio", description="get pin direction", arguments=DEFAULT_ARGS)
    pin = Pin(**kwargs)
    print(pin.direction)


def set_pin_value():
    args = DEFAULT_ARGS + [
        {"flags": ["value"], "help": "Value to set", "action": "store", "type": int, "choices": [0, 1]},
    ]

    kwargs = get_kwargs(package="sys_gpio", description="set pin value", arguments=args)
    value = kwargs.pop("value")
    pin = Pin(**kwargs)
    pin.value = value


def set_pin_direction():
    args = DEFAULT_ARGS + [
        {"flags": ["direction"], "help": "Direction to set", "action": "store", "choices": ["in", "out"]},
    ]

    kwargs = get_kwargs(package="sys_gpio", description="set pin direction", arguments=args)
    direction = kwargs.pop("direction")
    pin = Pin(**kwargs)
    pin.direction = direction


def get_pin_exports():
    print("Exported pins:" + ", ".join(list(Pin.get_exports())))
