from sys_gpio import Pin
from zenlib.util import get_kwargs


def main():
    args = [
            {"flags": ["pin"], "help": "Pin to get value from", "action": "store", "type": int},
    ]

    kwargs = get_kwargs(package="sys_gpio", description="get pin value", arguments=args)
    pin = Pin(**kwargs)
    print(pin.value)
