#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'Database config and ORM'

__author__ = 'Anonymous'

import logging;

logging.basicConfig(level=logging.INFO)

import asyncio
import aiomysql

from conf.config import configs


####################
# 数据库连接池
@asyncio.coroutine
def create_database_connection_pool(loop, **kw):
    try:
        if None == configs.get("mysql")['host']:
            return
    except KeyError as e:
        logging.info('Database config not found!')
        return

    logging.info('create database connection pool...')
    global __pool
    __pool = yield from aiomysql.create_pool(
            host=configs.get("mysql")['host'],
            port=configs.get("mysql")['port'],
            user=configs.get("mysql")['user'],
            password=configs.get("mysql")['password'],
            db=configs.get("mysql")['database'],

            maxsize=kw.get('maxsize', 10),
            minsize=kw.get('minsize', 1),

            charset=kw.get('charset', 'utf8'),
            autocommit=kw.get('autocommit', True),
            loop=loop
    )


@asyncio.coroutine
def select(sql, args, size=None):
    logging(sql, args)
    global __pool
    with (yield from __pool) as conn:
        cur = yield from conn.cursor(aiomysql.DictCursor)
        yield from cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            rs = yield from cur.fetchmany(size)
        else:
            rs = yield from cur.fetchall()
        yield from cur.close()
        logging.info('rows returned: %s' % len(rs))
        return rs


@asyncio.coroutine
def execute(sql, args):
    logging(sql, args)
    with (yield from __pool) as conn:
        try:
            cur = yield from conn.cursor()
            yield from cur.execute(sql.replace('?', '%s'), args)
            affected = cur.rowcount
            yield from cur.close()
        except BaseException as e:
            raise
        return affected
