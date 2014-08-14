# coding=utf-8
__author__ = "Gareth Coles"

import dicttoxml
import sys

from internal.manager import Manager

# To conform to the uWSGI spec
sys.stdout_ = sys.stdout
sys.stdout = sys.stderr

# So it's not so noisy
dicttoxml.set_debug(False)

manager = Manager()

application = app = manager.get_app()

if __name__ == "__main__":
    manager.start()
