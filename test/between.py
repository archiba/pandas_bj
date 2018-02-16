from typing import List, Any
from unittest import TestCase

import numpy
import pandas
from nose.tools import eq_, assert_true, assert_false, raises

from pandas_bj.between import Range, Between, CustomColumn


class TestRange(TestCase):
    def test_init(self):
        r = Range(100, 200)
        eq_(r.range_from, 100)
        eq_(r.range_to, 200)
        eq_(r.from_opened, False)
        eq_(r.to_opened, False)

        r = Range(100, 200, True, True)
        eq_(r.range_from, 100)
        eq_(r.range_to, 200)
        eq_(r.from_opened, True)
        eq_(r.to_opened, True)

        r = Range(numpy.NaN, numpy.NaN)
        eq_(r.range_from, None)
        eq_(r.range_to, None)

        r = Range(None, None)
        eq_(r.range_from, None)
        eq_(r.range_to, None)

    def test_comp(self):
        r1 = Range(100, 200)
        assert_true(r1 == 100)
        assert_false(r1 != 100)
        assert_true(r1 == 150)
        assert_true(r1 == 200)
        assert_false(r1 == 80)
        assert_false(r1 == 220)
        assert_false(r1 < 100)
        assert_false(r1 < 150)
        assert_false(r1 < 200)
        assert_false(r1 < 80)
        assert_true(r1 < 220)
        assert_false(r1 > 100)
        assert_false(r1 > 150)
        assert_false(r1 > 200)
        assert_true(r1 > 80)
        assert_false(r1 > 220)


        r2 = Range(100, 200, False, True)
        assert_true(r2 == 100)
        assert_true(r2 == 150)
        assert_false(r2 == 200)
        assert_false(r2 == 80)
        assert_false(r2 == 220)

        r3 = Range(100, 200, True, False)
        assert_false(r3 == 100)
        assert_true(r3 == 150)
        assert_true(r3 == 200)
        assert_false(r3 == 80)
        assert_false(r3 == 220)

        r4 = Range(100, 200, True, True)
        assert_false(r4 == 100)
        assert_true(r4 == 150)
        assert_false(r4 == 200)
        assert_false(r4 == 80)
        assert_false(r4 == 220)

        r3 = Range(None, 200)
        assert_true(r3 == 100)
        assert_true(r3 == 150)
        assert_true(r3 == 200)
        assert_true(r3 == 80)
        assert_false(r3 == 220)

        r4 = Range(100, None)
        assert_true(r4 == 100)
        assert_true(r4 == 150)
        assert_true(r4 == 200)
        assert_false(r4 == 80)
        assert_true(r4 == 220)

    def test_comp_range(self):
        r1 = Range(100, 200)
        r2 = Range(100, 200)
        assert_true(r1 == r2)
        assert_false(r1 < r2)
        assert_false(r1 > r2)

        r1 = Range(100, 200)
        r2 = Range(80, 200)
        assert_false(r1 == r2)
        assert_false(r1 < r2)
        assert_true(r1 > r2)
        assert_false(r2 > r1)
        assert_true(r2 < r1)

        r1 = Range(80, 200)
        r2 = Range(100, 200)
        assert_false(r1 == r2)
        assert_true(r1 < r2)
        assert_false(r1 > r2)
        assert_true(r2 > r1)
        assert_false(r2 < r1)

        r1 = Range(100, 200)
        r2 = Range(100, 180)
        assert_false(r1 == r2)
        assert_false(r1 < r2)
        assert_true(r1 > r2)
        assert_false(r2 > r1)
        assert_true(r2 < r1)

        r1 = Range(100, 180)
        r2 = Range(100, 200)
        assert_false(r1 == r2)
        assert_true(r1 < r2)
        assert_false(r1 > r2)
        assert_true(r2 > r1)
        assert_false(r2 < r1)

    def test_comp_range_open1(self):
        r1 = Range(100, 200, True, False)
        r2 = Range(100, 200, True, False)
        assert_true(r1 == r2)
        assert_false(r1 < r2)
        assert_false(r1 > r2)

        r1 = Range(100, 200, True, False)
        r2 = Range(80, 200, True, False)
        assert_false(r1 == r2)
        assert_false(r1 < r2)
        assert_true(r1 > r2)
        assert_false(r2 > r1)
        assert_true(r2 < r1)

        r1 = Range(80, 200, True, False)
        r2 = Range(100, 200, True, False)
        assert_false(r1 == r2)
        assert_true(r1 < r2)
        assert_false(r1 > r2)
        assert_true(r2 > r1)
        assert_false(r2 < r1)

        r1 = Range(100, 200, True, False)
        r2 = Range(100, 180, True, False)
        assert_false(r1 == r2)
        assert_false(r1 < r2)
        assert_true(r1 > r2)
        assert_false(r2 > r1)
        assert_true(r2 < r1)

        r1 = Range(100, 180, True, False)
        r2 = Range(100, 200, True, False)
        assert_false(r1 == r2)
        assert_true(r1 < r2)
        assert_false(r1 > r2)
        assert_true(r2 > r1)
        assert_false(r2 < r1)

    def test_comp_range_open2(self):
        r1 = Range(100, 200, True, False)
        r2 = Range(100, 200, False, False)
        assert_false(r1 == r2)
        assert_false(r1 < r2)
        assert_true(r1 > r2)

        r1 = Range(100, 200, True, False)
        r2 = Range(80, 200, False, False)
        assert_false(r1 == r2)
        assert_false(r1 < r2)
        assert_true(r1 > r2)
        assert_false(r2 > r1)
        assert_true(r2 < r1)

        r1 = Range(80, 200, True, False)
        r2 = Range(100, 200, False, False)
        assert_false(r1 == r2)
        assert_true(r1 < r2)
        assert_false(r1 > r2)
        assert_true(r2 > r1)
        assert_false(r2 < r1)

        r1 = Range(100, 200, True, False)
        r2 = Range(100, 180, False, False)
        assert_false(r1 == r2)
        assert_false(r1 < r2)
        assert_false(r1 < r2)
        assert_false(r2 > r1)
        assert_true(r2 < r1)

        r1 = Range(100, 180, True, False)
        r2 = Range(100, 200, False, False)
        assert_false(r1 == r2)
        assert_false(r1 < r2)
        assert_false(r1 > r2)
        assert_true(r2 > r1)
        assert_true(r2 < r1)

    def test_comp_range_open3(self):
        r1 = Range(100, 200, False, True)
        r2 = Range(100, 200, False, False)
        assert_false(r1 == r2)
        assert_true(r1 < r2)
        assert_false(r1 > r2)

        r1 = Range(100, 200, False, True)
        r2 = Range(80, 200, False, False)
        assert_false(r1 == r2)
        assert_false(r1 < r2)
        assert_false(r1 > r2)
        assert_true(r2 > r1)
        assert_true(r2 < r1)

        r1 = Range(80, 200, False, True)
        r2 = Range(100, 200, False, False)
        assert_false(r1 == r2)
        assert_true(r1 < r2)
        assert_false(r1 > r2)
        assert_true(r2 > r1)
        assert_false(r2 < r1)

        r1 = Range(100, 200, False, True)
        r2 = Range(100, 180, False, False)
        assert_false(r1 == r2)
        assert_false(r1 < r2)
        assert_false(r1 < r2)
        assert_false(r2 > r1)
        assert_true(r2 < r1)

        r1 = Range(100, 180, False, True)
        r2 = Range(100, 200, False, False)
        assert_false(r1 == r2)
        assert_true(r1 < r2)
        assert_false(r1 > r2)
        assert_true(r2 > r1)
        assert_false(r2 < r1)

    def test_comp_range_inf(self):
        r1 = Range(None, 200)
        r2 = Range(None, 200)
        assert_true(r1 == r2)
        assert_false(r1 < r2)
        assert_false(r1 > r2)

        r1 = Range(100, None)
        r2 = Range(100, None)
        assert_true(r1 == r2)
        assert_false(r1 < r2)
        assert_false(r1 > r2)

        r1 = Range(None, 200)
        r2 = Range(None, 220)
        assert_false(r1 == r2)
        assert_true(r1 < r2)
        assert_false(r1 > r2)

        r1 = Range(100, None)
        r2 = Range(120, None)
        assert_false(r1 == r2)
        assert_true(r1 < r2)
        assert_false(r1 > r2)

        r1 = Range(None, 200)
        r2 = Range(100, 200)
        assert_false(r1 == r2)
        assert_true(r1 < r2)
        assert_false(r1 > r2)
        assert_true(r2 > r1)
        assert_false(r2 < r1)

        r1 = Range(100, 200)
        r2 = Range(None, 200)
        assert_false(r1 == r2)
        assert_false(r1 < r2)
        assert_true(r1 > r2)
        assert_false(r2 > r1)
        assert_true(r2 < r1)

        r1 = Range(100, 200)
        r2 = Range(100, None)
        assert_false(r1 == r2)
        assert_true(r1 < r2)
        assert_false(r1 > r2)
        assert_true(r2 > r1)
        assert_false(r2 < r1)

        r1 = Range(100, None)
        r2 = Range(100, 200)
        assert_false(r1 == r2)
        assert_false(r1 < r2)
        assert_true(r1 > r2)
        assert_false(r2 > r1)
        assert_true(r2 < r1)

        r1 = Range(None, None, True, False)
        r2 = Range(None, None, False, False)
        assert_false(r1 == r2)
        assert_false(r1 < r2)
        assert_false(r1 > r2)

        r1 = Range(None, None, False, True)
        r2 = Range(None, None, False, False)
        assert_false(r1 == r2)
        assert_false(r1 < r2)
        assert_false(r1 > r2)

    def test_str(self):
        eq_(str(Range(100, 200)), '[100, 200]')
        eq_(str(Range(100, 200, True, True)), '(100, 200)')
        eq_(str(Range(100, 200)), repr(Range(100, 200)))

class TestBetween(TestCase):
    def test_init(self):
        b = Between('a', 'b')
        eq_(b.f, 'a')
        eq_(b.t, 'b')
        eq_(b.f_open, False)
        eq_(b.t_open, False)

        b = Between('a', 'b', True, False)
        eq_(b.f, 'a')
        eq_(b.t, 'b')
        eq_(b.f_open, True)
        eq_(b.t_open, False)

        b = Between('a', 'b', False, True)
        eq_(b.f, 'a')
        eq_(b.t, 'b')
        eq_(b.f_open, False)
        eq_(b.t_open, True)

    def test_build(self):
        df = pandas.DataFrame({'a': [1,2,3], 'b': [5,6,7]})
        b = Between('a', 'b')
        r = b(df)[1]
        eq_(r.range_from, 2)
        eq_(r.range_to, 6)
        eq_(r.from_opened, False)
        eq_(r.to_opened, False)

        b = Between('a', 'b', True, False)
        r = b(df)[1]
        eq_(r.range_from, 2)
        eq_(r.range_to, 6)
        eq_(r.from_opened, True)
        eq_(r.to_opened, False)

        b = Between('a', 'b', False, True)
        r = b(df)[1]
        eq_(r.range_from, 2)
        eq_(r.range_to, 6)
        eq_(r.from_opened, False)
        eq_(r.to_opened, True)

    @raises(KeyError)
    def test_build_fail1(self):
        df = pandas.DataFrame({'a': [1, 2, 3], 'b': [5, 6, 7]})
        b = Between('c', 'b')
        r = b(df)[1]

    @raises(KeyError)
    def test_build_fail2(self):
        df = pandas.DataFrame({'a': [1, 2, 3], 'b': [5, 6, 7]})
        b = Between('a', 'c')
        r = b(df)[1]

    def test_column_check1(self):
        df = pandas.DataFrame({'a': [1, 2, 3], 'b': [5, 6, 7]})
        b = Between('c', 'b')
        assert_false(b.column_check(df.columns))

    def test_column_check2(self):
        df = pandas.DataFrame({'a': [1, 2, 3], 'b': [5, 6, 7]})
        b = Between('a', 'c')
        assert_false(b.column_check(df.columns))

    def test_column_check3(self):
        df = pandas.DataFrame({'a': [1, 2, 3], 'b': [5, 6, 7]})
        b = Between('a', 'b')
        assert_true(b.column_check(df.columns))

    @raises(Exception)
    def test_abs_class(self):
        class TestClass(CustomColumn):
            pass
        TestClass()

    def test_abs_cover(self):
        df = pandas.DataFrame({'a': [1, 2, 3], 'b': [5, 6, 7]})
        class TestClass(CustomColumn):

            def __call__(self, df: pandas.DataFrame) -> pandas.Series:
                return super(TestClass, self).__call__(df)

            def column_check(self, columns: List[Any]) -> bool:
                return super(TestClass, self).column_check(columns)

        TestClass()(df)
        TestClass().column_check(df.columns)