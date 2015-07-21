#!/usr/bin/env python3
# =^.^= coding = utf-8 =^.^=
# andy.akame@gmail.com


# TODO: Other name arguments.


import json
import logging
import pprint
import requests


def main():
    btc = BTC()
    pprint.pprint(btc.info())
    pprint.pprint(btc.ticker("eur_rur"))
    pprint.pprint(btc.ticker("btc_usd", "usd_rur"))
    pprint.pprint(btc.depth("usd_rur"))
    pprint.pprint(btc.trades("usd_rur"))
    return


class BTC:
    _base_url = "https://btc-e.com/api/3/{}/{}"
    def __init__(self):
        self._session = requests.Session()
        return None

    def __getattr__(self, method_name, *args):
        return APIMethod(self, method_name, args)

    def __call__(self, method_name, *args):
        return json.loads(self._method_request(method_name, *args))

    def _method_request(self, method_name, *args):
        pairs = '-'.join(args[ 0 ]) # Well :/
        request = self._base_url.format(method_name, pairs)
        logging.debug(request)
        r = self._session.get(request)
        return r.content.decode("utf-8")


class APIMethod(object):
    __slots__ = ['_session', '_method_name']

    def __init__(self, session, method_name, *args):
        self._session = session
        self._method_name = method_name
        return None

    def __getattr__(self):
        return APIMethod(self._session, self._method_name)

    def __call__(self, *args):
        return self._session(self._method_name, args)


if "__main__" in __name__:
    main()


