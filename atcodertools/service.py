import os
import json
import urllib
import pickle
import getpass
import requests

import click
from lxml import html

HOME_PATH = os.path.join(os.getenv('HOME'), '.atcodertools')
COOKIE_FILE = os.path.join(HOME_PATH, 'cookiejar')


class Service:

    def __init__(self, filename=COOKIE_FILE):
        self.session = requests.Session()
        self._is_authorized = False

        if not os.path.isdir(HOME_PATH):
            os.makedirs(HOME_PATH)

        if not os.path.isfile(filename):
            return

        with open(filename, 'rb') as f:
            cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
            self.session.cookies = cookies
            self._is_authorized = True

    def is_authorized(self):
        return self._is_authorized

    def request(self, method, url, data=None, redirect=True):
        if method not in ['GET', 'POST']:
            click.echo('Unsupported methods.')
            return

        try:
            res = self.session.request(
                method,
                url,
                data=data,
                timeout=30,
                allow_redirects=redirect
                )
        except Exception as e:
            click.echo('Request Error')
        else:
            res.raise_for_status()
            return res

    def login(self):
        url = 'https://practice.contest.atcoder.jp/login'
        username = input('Username: ')
        password = getpass.getpass()
        data = {'name': username, 'password': password}

        res = self.request('POST', url, data, False)
        result, msg = self._get_messages_from_cookie(res.cookies)

        if result in ['', 'error']:
            click.echo(msg)
            return

        with open(COOKIE_FILE, 'wb') as f:
            pickle.dump(requests.utils.dict_from_cookiejar(res.cookies), f)
            click.echo(msg)

    def logout(self):
        if os.path.isfile(COOKIE_FILE):
            os.remove(COOKIE_FILE)

    def _get_messages_from_cookie(self, cookies):
        result, msg = '', ''
        for cookie in cookies:
            if cookie.name.startswith('__message_'):
                value = json.loads(urllib.parse.unquote_plus(cookie.value))
                root = html.fromstring(value['c'])
                elements = root.cssselect('span.lang-en')[0]
                result = value['t']
                msg = elements.text_content()
        return result, msg
