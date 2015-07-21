#!/usr/bin/env python3
# =^.^= coding = utf-8 =^.^=


# TODO: add possibility of passing string (well, any) arguments to the method.


import json
import logging
import pprint
import requests


def main():
    btc = BTC()
    pprint.pprint(btc.info())
    pprint.pprint(btc.ticker("btc_usd"))
    return


class BTC:
    def __init__(self):
        self._session = requests.Session()
        return None

    def __getattr__(self, method_name, args = ""):
        logging.debug(args)
        return APIMethod(self, method_name, args)

    def __call__(self, method_name, args = ""):
        logging.debug(args)
        return json.loads(self._method_request(method_name, args = ""))

    def _method_request(self, method_name, args = ""):
        logging.debug(args)
        request = "https://btc-e.com/api/3/{}/".format(method_name, args)
        logging.debug(request)
        r = self._session.get(request)
        return r.content.decode("utf-8")


class APIMethod(object):
    __slots__ = ['_session', '_method_name']

    def __init__(self, session, method_name, args = ""):
        logging.debug(args)
        self._session = session
        self._method_name = method_name

    def __getattr__(self):
        return APIMethod(self._session, self._method_name)

    def __call__(self, args = ""):
        logging.debug(args)
        return self._session(self._method_name, args)


if "__main__" in __name__:
    main()


