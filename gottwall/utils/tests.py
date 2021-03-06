#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
gottwall.utils.tests
~~~~~~~~~~~~~~~~~~~~

Utils for gottwall tests

:copyright: (c) 2012 - 2014 by GottWall team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
:github: http://github.com/GottWall/GottWall
"""
import datetime
import os
import unittest
from itertools import groupby
from random import randint, choice
from string import ascii_letters

from dateutil.relativedelta import relativedelta
from gottwall.utils import get_by_period, date_min, date_max
from tornado.testing import AsyncHTTPTestCase, AsyncTestCase


def async_test_ex(timeout=5):
    def _inner(func):
        def _runner(self, *args, **kwargs):
            try:
                func(self, *args, **kwargs)
            except Exception as e:
                print(e)
                self.stop()
                raise
            return self.wait(timeout=timeout)
        return _runner
    return _inner


def async_test(func):
    _inner = async_test_ex()
    return _inner(func)



class UtilsMixin(object):

    def random_str(self, size=10):
        return ''.join([choice(ascii_letters) for x in range(10)])

    @staticmethod
    def build_data(from_date, to_date, project_name,
                   metric_name, filters={}, size=1000, value=1):
        data = []

        for x in range(size):
            if not filters or not list(filters.keys()) or (None in filters):
                filter_name = None
                filter_value = None
            else:
                filter_name = choice(list(filters.keys()))
                filter_value = choice(filters[filter_name]) \
                               if isinstance(filters[filter_name], list) \
                               else filters[filter_name]

            data.append({'timestamp': datetime.datetime(randint(from_date.year, to_date.year),
                                                        randint(1, 12), randint(1, 27)) + relativedelta(days=randint(1, 10)),
                         'project': project_name,
                         'name': metric_name,
                         'filter_name': filter_name,
                         'filter_value': filter_value,
                         'value': value})
        return data

    def filter_data_by_period(self, data, from_date, to_date):
        """Filter data by period

        :param data: data list
        :param from_date: datetime
        :param to_date: datetime
        """
        return sorted(filter(lambda x: (x['timestamp'] >= from_date) and (x['timestamp'] <= to_date), data),
                      key=lambda x: x['timestamp'])

    def get_for_period(self, data, period):
        """Build data range grouped by period

        :param data: data list
        :param period: period name
        """
        return data

    @staticmethod
    def get_max(data_range):
        return max([x[1] for x in data_range])

    @staticmethod
    def get_min(data_range):
        return min([x[1] for x in data_range])

    @staticmethod
    def get_avg(data_range):
        filtered_range_values = [x[1] for x in data_range]
        return (sum(filtered_range_values) / len(filtered_range_values)) \
                if (len(filtered_range_values) > 0) else 0

    def get_range(self, data, from_date, to_date, period,
                  filter_name=None, filter_value=None):
        """Shortcut for datarange

        :param data: data list
        :param from_date:
        :param to_date:
        :param period:
        """
        from_date = date_min(from_date, period)
        to_date = date_max(to_date, period)

        data = self.filter_data_by_period(data, from_date, to_date)

        groups = groupby(data, key=lambda x: get_by_period(date_min(x['timestamp'], period), period))

        for group, group_items in groups:

            if not group_items:
                yield (group, 0)
                continue

            group_sum = 0

            if not filter_name:
                group_sum = sum([x['value'] for x in group_items])
            else:
                group_sum = sum([x['value'] for x in group_items
                                 if (x['filter_name'] == filter_name)
                                 and (x['filter_value'] == filter_value)])

            yield (group, group_sum)

class BaseTestCase(unittest.TestCase, UtilsMixin):
    pass

class AsyncBaseTestCase(AsyncTestCase, UtilsMixin):
    pass

class AsyncHTTPBaseTestCase(AsyncHTTPTestCase, UtilsMixin):
    pass
