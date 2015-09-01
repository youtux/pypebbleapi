import requests
from cerberus import Validator as _Validator

from pypebbleapi import __version__, schemas

PEBBLE_API_ROOT = 'https://timeline-api.getpebble.com'

PEBBLE_CODES = {
    400: 'The pin object submitted was invalid.',
    403: 'The API key submitted was invalid.',
    410: 'The user token submitted was invalid or does not exist.',
    429: 'Server is sending updates too quickly.',
    503: 'Could not save pin due to a temporary server error.',
}


def _raise_for_status(response):
    status = response.status_code
    if 400 <= response.status_code < 500:
        try:
            body = response.json()
            response.reason = body['errorMessage']
            return response.raise_for_status()
        except (KeyError, ValueError):
            pass

        try:
            response.reason = PEBBLE_CODES[status]
            return response.raise_for_status()
        except KeyError:
            pass

    response.raise_for_status()


def _request(method, url, api_key=None, user_token=None, topics_list=None,
        json=None, user_agent=None):
    headers = {}
    if api_key:
        headers['X-API-Key'] = api_key
    if user_token:
        headers['X-User-Token'] = user_token
    if topics_list:
        headers['X-PIN-Topics'] = ','.join(t for t in topics_list)
    if user_agent:
        headers['User-Agent'] = user_agent

    return requests.request(method, url, headers=headers, json=json)


def validate_pin(pin):
    v = _Validator(schemas.pin)
    if v.validate(pin):
        return
    else:
        raise schemas.DocumentError(errors=v.errors)


class Timeline(object):
    user_agent = '''pypebbleapi/{}'''.format(__version__)

    @property
    def api_key(self):
        return self._api_key

    @property
    def api_root(self):
        return self._api_root

    def __init__(self, api_key=None, api_root=PEBBLE_API_ROOT):
        self._api_key = api_key

        self._api_root = api_root

    def url_v1(self, partial_url=None):
        return '{}/v1{}'.format(self.api_root, partial_url)

    def send_shared_pin(self, topics, pin, skip_validation=False):
        if not self.api_key:
            raise ValueError("You need to specify an api_key.")
        if not skip_validation:
            validate_pin(pin)

        response = _request('PUT',
            url=self.url_v1('/shared/pins/' + pin['id']),
            user_agent=self.user_agent,
            api_key=self.api_key,
            topics_list=topics,
            json=pin,
        )
        _raise_for_status(response)

    def delete_shared_pin(self, pin_id):
        if not self.api_key:
            raise ValueError("You need to specify an api_key.")

        response = _request('DELETE',
            url=self.url_v1('/shared/pins/' + pin_id),
            user_agent=self.user_agent,
            api_key=self.api_key,
        )
        _raise_for_status(response)

    def send_user_pin(self, user_token, pin, skip_validation=False):
        if not skip_validation:
            validate_pin(pin)

        response = _request('PUT',
            url=self.url_v1('/user/pins/' + pin['id']),
            user_agent=self.user_agent,
            user_token=user_token,
            json=pin,
        )
        _raise_for_status(response)

    def delete_user_pin(self, user_token, pin_id):
        response = _request('DELETE',
            url=self.url_v1('/user/pins/' + pin_id),
            user_agent=self.user_agent,
            user_token=user_token,
        )
        _raise_for_status(response)

    def subscribe(self, user_token, topic):
        response = _request('POST',
            url=self.url_v1('/user/subscriptions/' + topic),
            user_agent=self.user_agent,
            user_token=user_token,
        )
        _raise_for_status(response)

    def unsubscribe(self, user_token, topic):
        response = _request('DELETE',
            url=self.url_v1('/user/subscriptions/' + topic),
            user_agent=self.user_agent,
            user_token=user_token,
        )
        _raise_for_status(response)

    def list_subscriptions(self, user_token):
        response = _request('GET',
            url=self.url_v1('/user/subscriptions'),
            user_agent=self.user_agent,
            user_token=user_token,
        )
        _raise_for_status(response)„

        return response.json()['topics']
