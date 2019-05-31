import importlib

from py3status.core import Module
from py3status.module_test import MockPy3statusWrapper

from . import base


class Py3status(base.InLoopPollText):
    defaults = [
        ("module_name", None, "Name of the py3status module to use"),
        ("update_interval", 1, "Update interval in seconds, if none, the "
         "widget updates whenever the event loop is idle."),
    ]

    def __init__(self, **config):
        base.InLoopPollText.__init__(self, **config)
        self.add_defaults(Py3status.defaults)

        package_name = "py3status.modules.{}".format(self.module_name)
        package = importlib.import_module(package_name)
        mock = MockPy3statusWrapper({"general": {},
                                     ".module_groups": {},
                                     "py3status": config})
        self.module = Module("py3status", {}, mock, package.Py3status())
        self.module.prepare_module()

    def poll(self):
        self.module.run()
        return self.module.get_latest()[0]["full_text"]
