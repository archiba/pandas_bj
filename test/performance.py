from random import Random
from unittest import TestCase

import pandas
import pandas_bj
from nose.tools import nottest
import time


class PerformanceTest(TestCase):

    @nottest
    def prepare_data_x(self, n, id1_range, id2_range, value_range, range_limit):
        r = Random(0)

        x_records = {'id1': [], 'id2': [], 's': [], 'e': []}

        for i in range(n):
            id1 = int(r.random() * id1_range)
            id2 = int(r.random() * id2_range)
            s_r = r.random()
            e_r = s_r + (1.0 - s_r) * r.random() * range_limit
            s = s_r * value_range
            e = e_r * value_range
            x_records['id1'].append(id1)
            x_records['id2'].append(id2)
            x_records['s'].append(s)
            x_records['e'].append(e)
        return pandas.DataFrame(x_records)

    @nottest
    def prepare_data_y(self, n, id1_range, id2_range, value_range):
        r = Random(0)

        y_records = {'id1': [], 'id2': [], 'v': []}

        for i in range(n):
            id1 = int(r.random() * id1_range)
            id2 = int(r.random() * id2_range)
            v = r.random() * value_range
            y_records['id1'].append(id1)
            y_records['id2'].append(id2)
            y_records['v'].append(v)
        return pandas.DataFrame(y_records)

    @nottest
    def performance_test(self, x_n, y_n, sort=True, id1_range=100, id2_range=50, value_range=1000, range_limit=1.0):
        x = self.prepare_data_x(x_n, id1_range, id2_range, value_range, range_limit)
        y = self.prepare_data_y(y_n, id1_range, id2_range, value_range)

        start = time.time()
        result = pandas_bj.merge(x, y, ['id1', 'id2', pandas_bj.Between('s', 'e')], ['id1', 'id2', 'v'], sort=sort)
        end = time.time()

        mean_merged_count = result.groupby(['id1_x', 'id2_x', 's', 'e'])['v'].count().mean()

        print(f'X: {x_n}, Y: {y_n}, SORT: {sort}, TIME: {end-start}, AVG COUNT: {mean_merged_count}')
        return end - start

    def test_inner_join1(self):
        self.performance_test(100, 1000, False)
        self.performance_test(100, 1000, True)

    def test_inner_join2(self):
        self.performance_test(1000, 10000, False)
        self.performance_test(1000, 10000, True)

    def test_inner_join3(self):
        self.performance_test(10000, 100000, True)

    def test_inner_join4(self):
        self.performance_test(10000, 1000000, True)