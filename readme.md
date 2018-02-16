# Pandas BJ

This is library that provides efficient way to use `JOIN` with `BETWEEN` comparison.

# How to use

```python
import pandas_bj
import pandas

df1 = pandas.DataFrame({
    'id1': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3],
    'id2': [1, 1, 1, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2],
    's': [1, 2, 3, 4, 5, 2, 3, 4, 5, 6, 3, 4, 5, 6, 7],
    'e': [5, 6, 7, 8, 9, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]}
)

df2 = pandas.DataFrame({
    'id3': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3],
    'id4': [1, 1, 1, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2],
    'v': [1, 5, 2, 6, 3, 7, 4, 8, 5, 9, 6, 10, 7, 11, 8]}
)

result = pandas_bj.merge(
    left=df1, right=df2,
    left_on=['id1', 'id2', pandas_bj.Between('s', 'e', True, True)], right_on=['id3', 'id4', 'v'],
    how='inner'
)

print(result)
```

```
       e  id1  id2    s  id3  id4     v
0    5.0  1.0  1.0  1.0  1.0  1.0   2.0
1    6.0  1.0  1.0  2.0  1.0  1.0   5.0
2    7.0  1.0  1.0  3.0  1.0  1.0   5.0
3    8.0  1.0  2.0  4.0  1.0  2.0   6.0
4    9.0  1.0  2.0  5.0  1.0  2.0   6.0
5    5.0  2.0  1.0  2.0  2.0  1.0   4.0
6    6.0  2.0  1.0  3.0  2.0  1.0   4.0
7    7.0  2.0  2.0  4.0  2.0  2.0   5.0
8    9.0  2.0  2.0  6.0  2.0  2.0   8.0
9   10.0  3.0  1.0  3.0  3.0  1.0   6.0
10  10.0  3.0  1.0  3.0  3.0  1.0   7.0
11  11.0  3.0  1.0  4.0  3.0  1.0   6.0
12  11.0  3.0  1.0  4.0  3.0  1.0  10.0
13  11.0  3.0  1.0  4.0  3.0  1.0   7.0
14  12.0  3.0  1.0  5.0  3.0  1.0   6.0
15  12.0  3.0  1.0  5.0  3.0  1.0  10.0
16  12.0  3.0  1.0  5.0  3.0  1.0   7.0
17  13.0  3.0  2.0  6.0  3.0  2.0  11.0
18  13.0  3.0  2.0  6.0  3.0  2.0   8.0
19  14.0  3.0  2.0  7.0  3.0  2.0  11.0
20  14.0  3.0  2.0  7.0  3.0  2.0   8.0

```

Use `sort` for efficient between join.

```python
result = pandas_bj.merge(
    left=df1, right=df2,
    left_on=['id1', 'id2', pandas_bj.Between('s', 'e', True, True)], right_on=['id3', 'id4', 'v'],
    how='inner',
    sort=True
)
```

# Options

#### how
- inner
- left
- right
- outer

#### sort
- bool
    `True` to use sort for all join keys
    `False` not to use sort for all join keys
- List of ints
    `[0, 1]` to use sort for first and second join keys
