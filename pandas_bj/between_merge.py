from typing import Union, Hashable, List

import pandas
from pandas import RangeIndex

from pandas_bj.between import CustomColumn
from pandas_bj.custom_merge import merge as custom_merge

how_types = {'inner', 'outer', 'left', 'right'}


def merge(left: pandas.DataFrame, right: pandas.DataFrame,
          left_on: Union[Hashable, List[Hashable]], right_on: Union[Hashable, List[Hashable]],
          how: str = 'inner', sort: Union[bool, List[int]] = False, suffixes=('_x', '_y')):
    assert isinstance(left.index, RangeIndex), "pandas_bj only supports RangeIndex-ed dataframe as input."
    assert isinstance(right.index, RangeIndex), "pandas_bj only supports RangeIndex-ed dataframe as input."

    if not isinstance(left_on, list):
        left_on = [left_on]
    if not isinstance(right_on, list):
        right_on = [right_on]

    if how not in how_types:
        raise ValueError('how must be inner, outer, left or right.')

    if len(left_on) != len(right_on):
        raise ValueError('Length of left and right merge keys must be same.')

    for l_on_col, r_on_col in zip(left_on, right_on):
        if not isinstance(l_on_col, CustomColumn) and  (l_on_col not in left.columns):
            raise KeyError(l_on_col)
        if isinstance(l_on_col, CustomColumn) and (not l_on_col.column_check(left.columns)):
            raise KeyError(l_on_col)
        if not isinstance(r_on_col, CustomColumn) and (r_on_col not in right.columns):
            raise KeyError(r_on_col)
        if isinstance(r_on_col, CustomColumn) and (not r_on_col.column_check(right.columns)):
            raise KeyError(r_on_col)

    key_length = len(left_on)

    if sort is True:
        sort = list(range(key_length))
    elif sort is False:
        sort = []

    left_key_df = pandas.DataFrame({i: left[k] if not isinstance(k, CustomColumn) else k(left)
                                    for i, k in enumerate(left_on)})
    right_key_df = pandas.DataFrame({i: right[k] if not isinstance(k, CustomColumn) else k(right)
                                    for i, k in enumerate(right_on)})
    left, right = rename(left, right, suffixes)
    return custom_merge(left, right, left_key_df, right_key_df, how, sort)


def rename(left, right, suffixes=('_x', '_y')):
    left_columns = set(left.columns)
    right_columns = set(right.columns)
    left_rename_targets = left_columns & right_columns
    right_rename_targets = right_columns & left_columns
    left_renames = {lname: f'{lname}{suffixes[0]}' for lname in left_rename_targets}
    right_renames = {rname: f'{rname}{suffixes[1]}' for rname in right_rename_targets}
    return left.rename(columns=left_renames), right.rename(columns=right_renames)
