import configparser
import sys


class _const:
    class ConstError(object):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError('Can\'t rebind const ({})'.format(name))

        self.__dict__[name] = value

    def setup(self):
        config = configparser.ConfigParser().read('config.ini', 'utf-8')
        for section in config.sections():
            for item in config.items(section):
                self.__setattr__(item[0], item[1])

    def default_setup(self):
        pass

sys.modules[__name__] = _const()
