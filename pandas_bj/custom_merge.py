from typing import Tuple, List, Set

import pandas


def reindex(df_l: pandas.DataFrame, df_r: pandas.DataFrame, on_l: pandas.DataFrame, on_r: pandas.DataFrame,
            sortable_columns: List[int], eq_null: bool = False) \
        -> Tuple[pandas.DataFrame, pandas.DataFrame, Set[int], Set[int]]:
    left_data_idx = []
    right_data_idx = []

    left_data_first_idx = df_l.index[0]
    right_data_first_idx = df_r.index[0]

    def add_left_row(idx):
        left_data_idx.append(idx)

    def add_right_row(idx):
        right_data_idx.append(idx)

    i = 0
    llabels = set()
    rlabels = set()

    num_keys = len(on_l.columns)

    # pandas use __gt__ for sorting, so we can use sorting.
    if len(sortable_columns) > 0:
        on_l.sort_values(by=[on_l.columns[i] for i in sortable_columns], inplace=True)
        on_r.sort_values(by=[on_r.columns[i] for i in sortable_columns], inplace=True)
    # for lrow, rrow in product(df_l.iterrows(), df_r.iterrows()):
    _df_l = on_l
    _df_r = on_r
    use_sort = len(sortable_columns) > 0
    sortable_column_dict = {ci: i for i, ci in enumerate(sortable_columns)}
    skip_r_head = 0
    riter = list(_df_r.itertuples())
    r_len = len(riter)
    for lrow in _df_l.itertuples():
        li = lrow[0]
        fin_rnames = []
        lname = li
        rnames = []
        current_r_iter = skip_r_head
        for r_idx in range(skip_r_head, r_len):
            rrow = riter[r_idx]
            ri = rrow[0]
            bad = False
            if not use_sort:
                for ci in range(num_keys):
                    lv = lrow[ci + 1]
                    rv = rrow[ci + 1]
                    if lv != rv:
                        bad = True
                        break
            else:
                sort_state = [0] * len(sortable_columns)
                skip = False
                for ci in range(num_keys):
                    lv = lrow[ci + 1]
                    rv = rrow[ci + 1]
                    lnull = pandas.isnull(lv)
                    rnull = pandas.isnull(rv)
                    column_sort_index = sortable_column_dict.get(ci, -1)
                    if column_sort_index > -1:
                        if lv == rv:
                            continue
                        if lnull and rnull:
                            if eq_null:
                                continue
                            bad = True
                            continue
                        if lnull or rnull:
                            bad = True
                            continue
                        if lv > rv:
                            bad = True
                            sort_state[column_sort_index] = 1
                            continue
                        if lv < rv:
                            bad = True
                            sort_state[column_sort_index] = 2
                            continue
                    else:
                        if lv != rv:
                            bad = True
                            continue
                if sum(sort_state) > 0:
                    for state in sort_state:
                        if state == 2:
                            skip = True
                            break
                        if state == 1:
                            skip_r_head = current_r_iter
                            break
                if skip:
                    break
            if not bad:
                rnames.append(ri)
            fin_rnames = rnames
            current_r_iter += 1
        for ri in fin_rnames:
            llabels.add(lname)
            rlabels.add(ri)
            add_left_row(li)
            add_right_row(ri)
            i += 1
    louter = set(range(i))
    router = set(range(i))
    lmiss_count = 0
    rmiss_count = 0
    for li in df_l.index:
        if li not in llabels:
            add_left_row(li)
            add_right_row(right_data_first_idx)
            louter.add(i)
            i += 1
            rmiss_count += 1
    for ri in df_r.index:
        if ri not in rlabels:
            add_right_row(ri)
            add_left_row(left_data_first_idx)
            router.add(i)
            i += 1
            lmiss_count += 1

    right_data_ = df_r.loc[right_data_idx].reset_index(drop=True)
    lr = len(right_data_.index)
    if lmiss_count > 0:
        right_data_.iloc[[lr - 1 - j - lmiss_count for j in range(rmiss_count)]] = None

    left_data_ = df_l.loc[left_data_idx].reset_index(drop=True)
    ll = len(left_data_.index)
    if rmiss_count > 0:
        left_data_.iloc[[ll - 1 - j for j in range(lmiss_count)]] = None
    return left_data_, right_data_, louter, router


def drop_outer(merged: pandas.DataFrame, louter: Set[int], router: Set[int], method: str):
    if method == 'left':
        outer = louter
    elif method == 'right':
        outer = router
    elif method == 'inner':
        outer = router & louter
    else:
        return merged
    merged = merged[merged.index.isin(outer)]
    return merged


def merge(left: pandas.DataFrame, right: pandas.DataFrame,
          left_key_df: pandas.DataFrame, right_key_df: pandas.DataFrame,
          how: str = 'inner', sortable_columns: List[int] = list()) -> pandas.DataFrame:
    df_left_, df_right_, louter, router = reindex(left, right, left_key_df, right_key_df,
                                                  sortable_columns)
    result: pandas.DataFrame = pandas.merge(df_left_, df_right_, how,
                                            left_index=True, right_index=True, copy=False)
    result: pandas.DataFrame = drop_outer(result, louter, router, how)
    return result
