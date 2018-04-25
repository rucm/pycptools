import configparser
import sys
import os


class _const:
    class ConstError(object):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError('Can\'t rebind const ({})'.format(name))
        self.__dict__[name] = value

    def setup(self):
        config = configparser.ConfigParser().read('config.ini')
        for section in config.sections():
            for item in config.items(section):
                self.__setattr__(item[0], item[1])

    def default_setup(self):
        config = configparser.ConfigParser()
        config['main'] = {
            'HOME_PATH': os.path.join(os.getenv('HOME'), '.cptools')
        }

        with open('config.ini', 'w') as file:
            config.write(file)

sys.modules[__name__] = _const()
