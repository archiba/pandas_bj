from unittest import TestCase

import pandas


def assert_true(exp1, msg=""):
    assert exp1, msg


def assert_false(exp1, msg=""):
    assert not exp1, msg


def raises(exception, msg=""):
    def _raises(f):
        def wrapper(*args, **kwargs):
            raised = False
            try:
                f(*args, **kwargs)
            except exception:
                raised = True
            assert raised, msg
        return wrapper
    return _raises


from pandas_bj.between import Between, GT, GE, LT, LE
from pandas_bj.between_merge import merge as bmerge


class TestBetweenMerge(TestCase):

    def setUp(self):
        self.df1 = pandas.DataFrame({
            'id1': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3],
            'id2': [1, 1, 1, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2],
            's': [1, 2, 3, 4, 5, 2, 3, 4, 5, 6, 3, 4, 5, 6, 7],
            'e': [5, 6, 7, 8, 9, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]}
        )

        self.df2 = pandas.DataFrame({
            'id3': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3],
            'id4': [1, 1, 1, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2],
            'v': [1, 5, 2, 6, 3, 7, 4, 8, 5, 9, 6, 10, 7, 11, 8]})

        self.df3 = pandas.DataFrame({
            'id1': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3],
            'id2': [1, 1, 1, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2],
            'v': [1, 5, 2, 6, 3, 7, 4, 8, 5, 9, 6, 10, 7, 11, 8]})
        self.df4 = pandas.DataFrame({
            'id1': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3],
            'id2': [1, 1, 1, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2],
            's': [1, 5, 2, 6, 3, 7, 4, 8, 5, 9, 6, 10, 7, 11, 8]})
        self.df5 = pandas.DataFrame({
            'id3': [1, 1, 1, 1, None, 2, 2, 2, None, 2, 3, 3, 3, 3, None],
            'id4': [1, 1, 1, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2],
            'v': [1, 5, 2, 6, 3, 7, 4, 8, 5, 9, 6, 10, 7, 11, 8]})
        self.df6 = pandas.DataFrame({
            'id1': [1, 2, 3, 4, 5, 6, 7, 8, 9, None],
            'f': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            't': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'v': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        })
        self.df7 = pandas.DataFrame({
            'id1': [1, 3, 5, 7, 9, 11, 13],
            'id2': [2, 3, 8, 8, 7, 5, 6],
            'v2': [101, 111, 121, 131, 141, 151, 161]
        })

    def test_inner_simple(self):
        result = bmerge(self.df1, self.df2, [Between('s', 'e', True, True)], ['v'])
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_inner_id1l(self):
        result = bmerge(self.df1, self.df2, ['id1', Between('s', 'e', True, True)], ['id3', 'v'])
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['id1'] == row['id3'], row['id1'] == row['id3'])
            assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_inner_id1r(self):
        result = bmerge(self.df1, self.df2, [Between('s', 'e', True, True), 'id1'], ['v', 'id3'])
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['id1'] == row['id3'])
            assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_inner_id2ll(self):
        result = bmerge(self.df1, self.df2, ['id1', 'id2', Between('s', 'e', True, True)], ['id3', 'id4', 'v'])
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['id1'] == row['id3'])
            assert_true(row['id2'] == row['id4'])
            assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_inner_id2rr(self):
        result = bmerge(self.df1, self.df2, [Between('s', 'e', True, True), 'id1', 'id2'], ['v', 'id3', 'id4'])
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['id1'] == row['id3'])
            assert_true(row['id2'] == row['id4'])
            assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_inner_id2lr(self):
        result = bmerge(self.df1, self.df2, ['id1', Between('s', 'e', True, True), 'id2'], ['id3', 'v', 'id4'])
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['id1'] == row['id3'])
            assert_true(row['id2'] == row['id4'])
            assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_left_id2lr(self):
        result = bmerge(self.df1, self.df2, ['id1', Between('s', 'e', True, True), 'id2'], ['id3', 'v', 'id4'], 'left')
        print(result)
        for idx, row in result.iterrows():
            if pandas.isnull(row['id3']):
                assert_false(any([row['id1'] == row_['id3'] and
                                  row['id2'] == row_['id4'] and
                                  row['s'] < row_['v'] < row['e']
                                  for idx, row_ in self.df2.iterrows()]), f'row: {row}')
            else:
                assert_true(row['id1'] == row['id3'], f'row: {row}')
                assert_true(row['id2'] == row['id4'], f'row: {row}')
                assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_right_id2lr(self):
        result = bmerge(self.df1, self.df2, ['id1', Between('s', 'e', True, True), 'id2'], ['id3', 'v', 'id4'], 'right')
        print(result)
        for idx, row in result.iterrows():
            if pandas.isnull(row['id1']):
                assert_false(any([row_['id1'] == row['id3'] and
                                  row_['id2'] == row['id4'] and
                                  row_['s'] < row['v'] < row_['e']
                                  for idx, row_ in self.df1.iterrows()]))
            else:
                assert_true(row['id1'] == row['id3'], f'row: {row}')
                assert_true(row['id2'] == row['id4'], f'row: {row}')
                assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_outer_id2lr(self):
        result = bmerge(self.df1, self.df2, ['id1', Between('s', 'e', True, True), 'id2'], ['id3', 'v', 'id4'], 'outer')
        print(result)
        for idx, row in result.iterrows():
            if pandas.isnull(row['id3']):
                assert_false(any([row['id1'] == row_['id3'] and
                                  row['id2'] == row_['id4'] and
                                  row['s'] < row_['v'] < row['e']
                                  for idx, row_ in self.df2.iterrows()]))
            elif pandas.isnull(row['id1']):
                assert_false(any([row_['id1'] == row['id3'] and
                                  row_['id2'] == row['id4'] and
                                  row_['s'] < row['v'] < row_['e']
                                  for idx, row_ in self.df1.iterrows()]))
            else:
                assert_true(row['id1'] == row['id3'], f'row: {row}')
                assert_true(row['id2'] == row['id4'], f'row: {row}')
                assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_inner_simple_s(self):
        result = bmerge(self.df1, self.df2, [Between('s', 'e', True, True)], ['v'], sort=True)
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_inner_id1l_s(self):
        result = bmerge(self.df1, self.df2, ['id1', Between('s', 'e', True, True)], ['id3', 'v'], sort=True)
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['id1'] == row['id3'])
            assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_inner_id1r_s(self):
        result = bmerge(self.df1, self.df2, [Between('s', 'e', True, True), 'id1'], ['v', 'id3'], sort=[0])
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['id1'] == row['id3'])
            assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_inner_id2ll_s(self):
        result = bmerge(self.df1, self.df2, ['id1', 'id2', Between('s', 'e', True, True)], ['id3', 'id4', 'v'],
                        sort=True)
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['id1'] == row['id3'])
            assert_true(row['id2'] == row['id4'])
            assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_inner_id2rr_s(self):
        result = bmerge(self.df1, self.df2, [Between('s', 'e', True, True), 'id1', 'id2'], ['v', 'id3', 'id4'],
                        sort=[0])
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['id1'] == row['id3'])
            assert_true(row['id2'] == row['id4'])
            assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_inner_id2lr_s(self):
        result = bmerge(self.df1, self.df2, ['id1', Between('s', 'e', True, True), 'id2'], ['id3', 'v', 'id4'],
                        sort=[1, 2])
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['id1'] == row['id3'])
            assert_true(row['id2'] == row['id4'])
            assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_left_id2lr_s(self):
        result = bmerge(self.df1, self.df2, ['id1', Between('s', 'e', True, True), 'id2'], ['id3', 'v', 'id4'], 'left',
                        sort=[2, 1])
        print(result)
        for idx, row in result.iterrows():
            if pandas.isnull(row['id3']):
                assert_false(any([row['id1'] == row_['id3'] and
                                  row['id2'] == row_['id4'] and
                                  row['s'] < row_['v'] < row['e']
                                  for idx, row_ in self.df2.iterrows()]), f'row: {row}')
            else:
                assert_true(row['id1'] == row['id3'], f'row: {row}')
                assert_true(row['id2'] == row['id4'], f'row: {row}')
                assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_right_id2lr_s(self):
        result = bmerge(self.df1, self.df2, ['id1', Between('s', 'e', True, True), 'id2'], ['id3', 'v', 'id4'], 'right',
                        [0, 2])
        print(result)
        for idx, row in result.iterrows():
            if pandas.isnull(row['id1']):
                assert_false(any([row_['id1'] == row['id3'] and
                                  row_['id2'] == row['id4'] and
                                  row_['s'] < row['v'] < row_['e']
                                  for idx, row_ in self.df1.iterrows()]))
            else:
                assert_true(row['id1'] == row['id3'], f'row: {row}')
                assert_true(row['id2'] == row['id4'], f'row: {row}')
                assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_outer_id2lr_s(self):
        result = bmerge(self.df1, self.df2, ['id1', Between('s', 'e', True, True), 'id2'], ['id3', 'v', 'id4'], 'outer',
                        sort=[0, 2, 1])
        print(result)
        for idx, row in result.iterrows():
            if pandas.isnull(row['id3']):
                assert_false(any([row['id1'] == row_['id3'] and
                                  row['id2'] == row_['id4'] and
                                  row['s'] < row_['v'] < row['e']
                                  for idx, row_ in self.df2.iterrows()]))
            elif pandas.isnull(row['id1']):
                assert_false(any([row_['id1'] == row['id3'] and
                                  row_['id2'] == row['id4'] and
                                  row_['s'] < row['v'] < row_['e']
                                  for idx, row_ in self.df1.iterrows()]))
            else:
                assert_true(row['id1'] == row['id3'], f'row: {row}')
                assert_true(row['id2'] == row['id4'], f'row: {row}')
                assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_inner_name1(self):
        result = bmerge(self.df1, self.df3, [Between('s', 'e', True, True)], ['v'])
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_inner_name2(self):
        result = bmerge(self.df1, self.df3, ['id1', Between('s', 'e', True, True)], ['id1', 'v'])
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['id1_x'] == row['id1_y'])
            assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_inner_name3(self):
        result = bmerge(self.df1, self.df4, [Between('s', 'e', True, True)], ['s'])
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['s_x'] < row['s_y'] and row['e'] > row['s_y'], f'row: {row}')

    def test_inner_simple2(self):
        result = bmerge(self.df1, self.df2, Between('s', 'e', True, True), 'v')
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    @raises(ValueError)
    def test_inner_fail_validation1(self):
        result = bmerge(self.df1, self.df2, Between('s', 'e', True, True), ['id1', 'v'])

    @raises(ValueError)
    def test_inner_fail_validation2(self):
        result = bmerge(self.df1, self.df2, Between('s', 'e', True, True), 'v', how='abc')

    @raises(KeyError)
    def test_inner_fail_key1(self):
        result = bmerge(self.df1, self.df2, 'id3', 'id3')

    @raises(KeyError)
    def test_inner_fail_key2(self):
        result = bmerge(self.df1, self.df2, 'id1', 'id1')

    @raises(KeyError)
    def test_inner_fail_key3(self):
        result = bmerge(self.df1, self.df2, Between('a', 'e', True, True), 'v')

    @raises(KeyError)
    def test_inner_fail_key4(self):
        result = bmerge(self.df1, self.df2, Between('s', 'e', True, True), Between('id1', 'id2', True, True))

    def test_inner_id2ll_gt(self):
        result = bmerge(self.df1, self.df2, ['id1', 'id2', GT('s')], ['id3', 'id4', 'v'])
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['id1'] == row['id3'])
            assert_true(row['id2'] == row['id4'])
            assert_true(row['s'] < row['v'], f'row: {row}')

    def test_inner_id2ll_ge(self):
        result = bmerge(self.df1, self.df2, ['id1', 'id2', GE('s')], ['id3', 'id4', 'v'])
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['id1'] == row['id3'])
            assert_true(row['id2'] == row['id4'])
            assert_true(row['s'] <= row['v'], f'row: {row}')

    def test_inner_id2ll_lt(self):
        result = bmerge(self.df1, self.df2, ['id1', 'id2', LT('e')], ['id3', 'id4', 'v'])
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['id1'] == row['id3'])
            assert_true(row['id2'] == row['id4'])
            assert_true(row['e'] > row['v'], f'row: {row}')

    def test_inner_id2ll_le(self):
        result = bmerge(self.df1, self.df2, ['id1', 'id2', LE('e')], ['id3', 'id4', 'v'])
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['id1'] == row['id3'])
            assert_true(row['id2'] == row['id4'])
            assert_true(row['e'] >= row['v'], f'row: {row}')

    def test_null_id1(self):
        result = bmerge(self.df1, self.df5, ['id1', Between('s', 'e', True, True)], ['id3', 'v'])
        print(result)
        for idx, row in result.iterrows():
            assert_true(row['id1'] == row['id3'])
            assert_true(row['s'] < row['v'] and row['e'] > row['v'], f'row: {row}')

    def test_null_id1l(self):
        result = bmerge(self.df1, self.df5, ['id1', Between('s', 'e', True, True)], ['id3', 'v'], how='left')
        print(result)
        for idx, row in result.iterrows():
            if not pandas.isnull(row['id3']):
                assert_true(row['id1'] == row['id3'])
                assert_true(row['s'] <= row['v'], f'row: {row}')
                assert_true(row['e'] >= row['v'], f'row: {row}')

    def test_null_id1l_opposite(self):
        result = bmerge(self.df5, self.df1, ['id3', 'v'], ['id1', Between('s', 'e', True, True)], how='inner')
        print(result)
        for idx, row in result.iterrows():
            if not pandas.isnull(row['id3']):
                assert_true(row['id1'] == row['id3'])
                assert_true(row['s'] <= row['v'], f'row: {row}')
                assert_true(row['e'] >= row['v'], f'row: {row}')

    def test_left_20220603(self):
        result = bmerge(self.df6, self.df7, ['id1', Between('f', 't')], ['id1', 'id2'], how='left')
        print(result)
        assert len(result) == 10