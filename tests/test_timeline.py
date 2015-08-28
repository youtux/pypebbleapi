import re
from datetime import datetime

import httpretty as _httpretty
import pytest

from httpretty import GET, PUT
from pypebbleapi import Timeline

FAKE_API_ROOT = 'http://timeline_api'
FAKE_API_KEY = 'FAKE_API_KEY'

PEBBLE_API_ROOT = 'https://timeline-api.getpebble.com'

fake_pin = {
    'id': '1234',
    'time': datetime.now().isoformat(),
    'layout': {},
}


def urlize(partial_url):
    return re.compile(re.escape(FAKE_API_ROOT) + partial_url)


@pytest.fixture
def httpretty(request):
    _httpretty.enable()

    def fin():
        _httpretty.disable()
        _httpretty.reset()
    request.addfinalizer(fin)
    return _httpretty


@pytest.fixture(params=[200, 429, 503])
def server(request):
    _httpretty.enable()
    _httpretty.register_uri(
        PUT,
        urlize(r"/v1/shared/pins/(.*)"),
        body='[{"title": "Test Deal"}]',
        content_type="application/json",
        status=request.param)

    def fin():
        _httpretty.disable()
        _httpretty.reset()
    request.addfinalizer(fin)
    return _httpretty


@pytest.fixture
def timeline():
    return Timeline(api_root=FAKE_API_ROOT, api_key=FAKE_API_KEY)


def test_can_create_with_no_opts():
    t = Timeline()

    assert t


def test_sets_default_api_root():
    t = Timeline()

    assert t._api_root == PEBBLE_API_ROOT


def test_can_set_api_key():
    t = Timeline(api_key='TEST_KEY')

    assert t._api_key == 'TEST_KEY'


def test_can_set_api_root():
    t = Timeline(api_root=FAKE_API_ROOT)

    assert t._api_root == FAKE_API_ROOT


# def test_send_shared_pin(server):
#     t = Timeline(api_root=FAKE_API_ROOT)

#     assert t._api_root == FAKE_API_ROOT

#     response = t.send_shared_pin(['a', 'b'], {'id': 3})

#     assert response.status_code in [200, 429, 503]


def test_send_user_token_good(httpretty, timeline):
    httpretty.register_uri(
        PUT,
        urlize(r"/v1/user/pins/(.*)"),
        body='{status: "OK"}',
        content_type="application/json",
        status=200)
    timeline.send_user_pin(user_token='3323', pin=fake_pin)


def test_error_if_user_token_is_not_a_string(server, timeline):
    with pytest.raises(ValueError):
        timeline.send_user_pin(user_token=5, pin=fake_pin)


def test_should_handle_remote_errors(server, timeline):
    pass
