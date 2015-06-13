pypebbleapi
============
Pebble-api for python.
This is a library to ease the access to the Pebble Timeline and the creation of Pins.
It supports python 2.7, 3.3 and 3.4.


Usage
-----

Usage is pretty simple:
```python
from pypebbleapi import Timeline, Pin
import datetime

timeline = Timeline(my_api_key)

my_pin = Pin(id='123', time=datetime.date.today().isoformat())

timeline.send_shared_pin(['a_topic', 'another_topic'], my_pin)
```


Install
-------

Installation is simple too::

    $ pip install pypebbleapi

