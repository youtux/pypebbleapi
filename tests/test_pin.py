from __future__ import print_function
from pypebbleapi import Pin

from datetime import datetime

import json


def test_create_pin():
    pin = Pin('1', datetime.now())

    pin.id = 3

    pin.time = datetime.now()

    print(pin)

    # print(json.dumps(pin))
