#!/usr/bin/env python
# -*- coding: utf-8 -*-

STORAGE = 'gottwall.storages.RedisStorage'

BACKENDS = {
    'gottwall.backends.redis.RedisBackend': {
        'HOST': "10.8.9.8",
        'PORT': 6379,
        'PASSWORD': None,
        'DB': 2,
        "CHANNEL": "gottwall"},
    'gottwall.backends.tcpip.TCPIPBackend': {}
    }

TEMPLATE_DEBUG = True

STORAGE_SETTINGS = dict(
    REDIS_HOST = "10.8.9.8",
    REDIS_PORT = 6379,
    REDIS_PASSWORD = None,
    REDIS_DB = 2
)

REDIS = {"CHANNEL": "gottwall"}


USERS = []

SECRET_KEY = "dwefwefwefwecwef"

# http://public_key:secret_key@host.com

PROJECTS = {"test_project": "my_public_key",
            "another_project": "public_key2"}

cookie_secret="fkewrlhfwhrfweiurbweuybfrweoubfrowebfioubweoiufbwbeofbowebfbwup2XdTP1o/Vo=",

TEMPLATE_DEBUG = True


DATABASE = {
    "ENGINE": "postgresql+psycopg2",
    "HOST": "localhost",
    "PORT": 5432,
    "USER": "postgres",
    "PASSWORD": "none",
    "NAME": "gottwall"
    }
