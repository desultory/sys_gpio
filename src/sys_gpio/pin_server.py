#!/usr/bin/python3

from aiohttp.web import Application, Response, run_app

from zenlib.logging import loggify

from pin import Pin


PINS = list(range(0, 26))


@loggify
class PinServer:
    """ Webserver which provides status info and the option to set GPIO pins usign sys_gpio """


    def __init__(self, listen_ip="0.0.0.0", listen_port=8080, pins=None, **kwargs):
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.app = Application(logger=self.logger)

        self._init_pins(pins or PINS)
        self.app.router.add_get('/get/{pin}', self.get_pin_value)
        self.app.router.add_get('/set/{pin}/{value}', self.set_pin_value)

    def _init_pins(self, pins: list):
        """ Initialize the pins """
        self.pins = {}
        for pin_number in pins:
            self.pins[pin_number] = Pin(pin_number, logger=self.logger)

    def get_pin_value(self, request):
        """ Get the value of a pin, in the format /get/<pin_number> """
        pin_number = int(request.match_info['pin'])
        if pin_number in self.pins:
            return Response(text=str(self.pins[pin_number].value))
        else:
            return Response(status=404, text="Pin not found")

    def set_pin_value(self, request):
        """ Set the value of a pin, in the format /set/<pin_number>/<value> """
        pin_number = int(request.match_info['pin'])
        try:
            value = int(request.match_info['value'])
        except ValueError:
            return Response(status=400, text="Invalid value")
        if pin_number in self.pins:
            try:
                self.pins[pin_number].value = value
                return Response(text="OK")
            except ValueError as e:
                return Response(status=400, text=f"Invalid value: {e}")
        else:
            self.logger.warning(self.pins)
            return Response(status=404, text="Pin not found")

    def start(self):
        """ Start the webserver """
        self.logger.info(f"Starting PinServer on {self.listen_ip}:{self.listen_port}")
        run_app(self.app, host=self.listen_ip, port=self.listen_port)



if __name__ == "__main__":
    server = PinServer()
    server.start()
