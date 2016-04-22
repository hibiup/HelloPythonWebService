#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Anonymous'

'Web service entry'

import logging;

logging.basicConfig(level=logging.INFO)

from aiohttp import web
from www.core.decorators import get


####################
# Service URIs
@get("/")
def index(request):
    return web.Response(body=b'<h1>Awesome</h1>')
