# Pandas BETWEEN JOIN

This library provides efficient way to `JOIN` pandas dataframes with gt/lt-comparison-based process, 
while pandas' default merge only applies hash-comparison-based process.

This library supports more SQL-ish joining flexibility like below:

- `JOIN yyy WHERE yyy.a BETWEEN xxx.b AND xxx.c`
- `JOIN yyy WHERE yyy.a > xxx.b`
- `JOIN yyy WHERE yyy.a >= xxx.b`
- `JOIN yyy WHERE yyy.a < xxx.b`
- `JOIN yyy WHERE yyy.a <= xxx.b`

Please refer [Performance](#performance) if you need performance information.

# Latest version

0.1.3

# Requirements

- python >= 3.6
- numpy >= 1.14.0
- pandas >= 0.22.0

# Install

```bash
pip install pandas-bj
```

# How to use
You can do `JOIN WHERE BETWEEN`-ish merging using pandas_bj with codes like: 

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

# WHERE xxx.id1 = yyy.id3 AND
#       xxx.id2 = yyy.id4 AND
#       yyy.v BETWEEN xxx.s AND xxx.e
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

Use `sort` option for better performance.

```python
result = pandas_bj.merge(
    left=df1, right=df2,
    left_on=['id1', 'id2', pandas_bj.Between('s', 'e', True, True)], right_on=['id3', 'id4', 'v'],
    how='inner',
    sort=True
)
```

Also, we provide dataframe mergin using greater-than, less-than, greater-than-equal, less-than-equal expression.

```python
# WHERE xxx.id1 = yyy.id3 AND
#       xxx.id2 = yyy.id4 AND
#       xxx.s < yyy.v
result = pandas_bj.merge(
    left=df1, right=df2,
    left_on=['id1', 'id2', pandas_bj.GT('s')], right_on=['id3', 'id4', 'v'],
    how='inner',
    sort=True
)
print('GT')
print(result)

# WHERE xxx.id1 = yyy.id3 AND
#       xxx.id2 = yyy.id4 AND
#       xxx.s <= yyy.v
result = pandas_bj.merge(
    left=df1, right=df2,
    left_on=['id1', 'id2', pandas_bj.GE('s')], right_on=['id3', 'id4', 'v'],
    how='inner',
    sort=True
)
print('GE')
print(result)

# WHERE xxx.id1 = yyy.id3 AND
#       xxx.id2 = yyy.id4 AND
#       xxx.e > yyy.v
result = pandas_bj.merge(
    left=df1, right=df2,
    left_on=['id1', 'id2', pandas_bj.LT('e')], right_on=['id3', 'id4', 'v'],
    how='inner',
    sort=True
)
print('LT')
print(result)

# WHERE xxx.id1 = yyy.id3 AND
#       xxx.id2 = yyy.id4 AND
#       xxx.e >= yyy.v
result = pandas_bj.merge(
    left=df1, right=df2,
    left_on=['id1', 'id2', pandas_bj.LE('e')], right_on=['id3', 'id4', 'v'],
    how='inner',
    sort=True
)
print('LE')
print(result)
```

```
GT
       e  id1  id2    s  id3  id4     v
0    5.0  1.0  1.0  1.0  1.0  1.0   5.0
1    5.0  1.0  1.0  1.0  1.0  1.0   2.0
2    6.0  1.0  1.0  2.0  1.0  1.0   5.0
3    7.0  1.0  1.0  3.0  1.0  1.0   5.0
4    8.0  1.0  2.0  4.0  1.0  2.0   6.0
5    9.0  1.0  2.0  5.0  1.0  2.0   6.0
6    5.0  2.0  1.0  2.0  2.0  1.0   7.0
7    5.0  2.0  1.0  2.0  2.0  1.0   4.0
8    6.0  2.0  1.0  3.0  2.0  1.0   7.0
9    6.0  2.0  1.0  3.0  2.0  1.0   4.0
10   7.0  2.0  2.0  4.0  2.0  2.0   8.0
11   7.0  2.0  2.0  4.0  2.0  2.0   5.0
12   7.0  2.0  2.0  4.0  2.0  2.0   9.0
13   8.0  2.0  2.0  5.0  2.0  2.0   8.0
14   8.0  2.0  2.0  5.0  2.0  2.0   9.0
15   9.0  2.0  2.0  6.0  2.0  2.0   8.0
16   9.0  2.0  2.0  6.0  2.0  2.0   9.0
17  10.0  3.0  1.0  3.0  3.0  1.0   6.0
18  10.0  3.0  1.0  3.0  3.0  1.0  10.0
19  10.0  3.0  1.0  3.0  3.0  1.0   7.0
20  11.0  3.0  1.0  4.0  3.0  1.0   6.0
21  11.0  3.0  1.0  4.0  3.0  1.0  10.0
22  11.0  3.0  1.0  4.0  3.0  1.0   7.0
23  12.0  3.0  1.0  5.0  3.0  1.0   6.0
24  12.0  3.0  1.0  5.0  3.0  1.0  10.0
25  12.0  3.0  1.0  5.0  3.0  1.0   7.0
26  13.0  3.0  2.0  6.0  3.0  2.0  11.0
27  13.0  3.0  2.0  6.0  3.0  2.0   8.0
28  14.0  3.0  2.0  7.0  3.0  2.0  11.0
29  14.0  3.0  2.0  7.0  3.0  2.0   8.0

GE
       e  id1  id2    s  id3  id4     v
0    5.0  1.0  1.0  1.0  1.0  1.0   1.0
1    5.0  1.0  1.0  1.0  1.0  1.0   5.0
2    5.0  1.0  1.0  1.0  1.0  1.0   2.0
3    6.0  1.0  1.0  2.0  1.0  1.0   5.0
4    6.0  1.0  1.0  2.0  1.0  1.0   2.0
5    7.0  1.0  1.0  3.0  1.0  1.0   5.0
6    8.0  1.0  2.0  4.0  1.0  2.0   6.0
7    9.0  1.0  2.0  5.0  1.0  2.0   6.0
8    5.0  2.0  1.0  2.0  2.0  1.0   7.0
9    5.0  2.0  1.0  2.0  2.0  1.0   4.0
10   6.0  2.0  1.0  3.0  2.0  1.0   7.0
11   6.0  2.0  1.0  3.0  2.0  1.0   4.0
12   7.0  2.0  2.0  4.0  2.0  2.0   8.0
13   7.0  2.0  2.0  4.0  2.0  2.0   5.0
14   7.0  2.0  2.0  4.0  2.0  2.0   9.0
15   8.0  2.0  2.0  5.0  2.0  2.0   8.0
16   8.0  2.0  2.0  5.0  2.0  2.0   5.0
17   8.0  2.0  2.0  5.0  2.0  2.0   9.0
18   9.0  2.0  2.0  6.0  2.0  2.0   8.0
19   9.0  2.0  2.0  6.0  2.0  2.0   9.0
20  10.0  3.0  1.0  3.0  3.0  1.0   6.0
21  10.0  3.0  1.0  3.0  3.0  1.0  10.0
22  10.0  3.0  1.0  3.0  3.0  1.0   7.0
23  11.0  3.0  1.0  4.0  3.0  1.0   6.0
24  11.0  3.0  1.0  4.0  3.0  1.0  10.0
25  11.0  3.0  1.0  4.0  3.0  1.0   7.0
26  12.0  3.0  1.0  5.0  3.0  1.0   6.0
27  12.0  3.0  1.0  5.0  3.0  1.0  10.0
28  12.0  3.0  1.0  5.0  3.0  1.0   7.0
29  13.0  3.0  2.0  6.0  3.0  2.0  11.0
30  13.0  3.0  2.0  6.0  3.0  2.0   8.0
31  14.0  3.0  2.0  7.0  3.0  2.0  11.0
32  14.0  3.0  2.0  7.0  3.0  2.0   8.0

LT
       e  id1  id2    s  id3  id4     v
0    5.0  1.0  1.0  1.0  1.0  1.0   1.0
1    5.0  1.0  1.0  1.0  1.0  1.0   2.0
2    6.0  1.0  1.0  2.0  1.0  1.0   1.0
3    6.0  1.0  1.0  2.0  1.0  1.0   5.0
4    6.0  1.0  1.0  2.0  1.0  1.0   2.0
5    7.0  1.0  1.0  3.0  1.0  1.0   1.0
6    7.0  1.0  1.0  3.0  1.0  1.0   5.0
7    7.0  1.0  1.0  3.0  1.0  1.0   2.0
8    8.0  1.0  2.0  4.0  1.0  2.0   6.0
9    8.0  1.0  2.0  4.0  1.0  2.0   3.0
10   9.0  1.0  2.0  5.0  1.0  2.0   6.0
11   9.0  1.0  2.0  5.0  1.0  2.0   3.0
12   5.0  2.0  1.0  2.0  2.0  1.0   4.0
13   6.0  2.0  1.0  3.0  2.0  1.0   4.0
14   7.0  2.0  2.0  4.0  2.0  2.0   5.0
15   8.0  2.0  2.0  5.0  2.0  2.0   5.0
16   9.0  2.0  2.0  6.0  2.0  2.0   8.0
17   9.0  2.0  2.0  6.0  2.0  2.0   5.0
18  10.0  3.0  1.0  3.0  3.0  1.0   6.0
19  10.0  3.0  1.0  3.0  3.0  1.0   7.0
20  11.0  3.0  1.0  4.0  3.0  1.0   6.0
21  11.0  3.0  1.0  4.0  3.0  1.0  10.0
22  11.0  3.0  1.0  4.0  3.0  1.0   7.0
23  12.0  3.0  1.0  5.0  3.0  1.0   6.0
24  12.0  3.0  1.0  5.0  3.0  1.0  10.0
25  12.0  3.0  1.0  5.0  3.0  1.0   7.0
26  13.0  3.0  2.0  6.0  3.0  2.0  11.0
27  13.0  3.0  2.0  6.0  3.0  2.0   8.0
28  14.0  3.0  2.0  7.0  3.0  2.0  11.0
29  14.0  3.0  2.0  7.0  3.0  2.0   8.0

LE
       e  id1  id2    s  id3  id4     v
0    5.0  1.0  1.0  1.0  1.0  1.0   1.0
1    5.0  1.0  1.0  1.0  1.0  1.0   5.0
2    5.0  1.0  1.0  1.0  1.0  1.0   2.0
3    6.0  1.0  1.0  2.0  1.0  1.0   1.0
4    6.0  1.0  1.0  2.0  1.0  1.0   5.0
5    6.0  1.0  1.0  2.0  1.0  1.0   2.0
6    7.0  1.0  1.0  3.0  1.0  1.0   1.0
7    7.0  1.0  1.0  3.0  1.0  1.0   5.0
8    7.0  1.0  1.0  3.0  1.0  1.0   2.0
9    8.0  1.0  2.0  4.0  1.0  2.0   6.0
10   8.0  1.0  2.0  4.0  1.0  2.0   3.0
11   9.0  1.0  2.0  5.0  1.0  2.0   6.0
12   9.0  1.0  2.0  5.0  1.0  2.0   3.0
13   5.0  2.0  1.0  2.0  2.0  1.0   4.0
14   6.0  2.0  1.0  3.0  2.0  1.0   4.0
15   7.0  2.0  2.0  4.0  2.0  2.0   5.0
16   8.0  2.0  2.0  5.0  2.0  2.0   8.0
17   8.0  2.0  2.0  5.0  2.0  2.0   5.0
18   9.0  2.0  2.0  6.0  2.0  2.0   8.0
19   9.0  2.0  2.0  6.0  2.0  2.0   5.0
20   9.0  2.0  2.0  6.0  2.0  2.0   9.0
21  10.0  3.0  1.0  3.0  3.0  1.0   6.0
22  10.0  3.0  1.0  3.0  3.0  1.0  10.0
23  10.0  3.0  1.0  3.0  3.0  1.0   7.0
24  11.0  3.0  1.0  4.0  3.0  1.0   6.0
25  11.0  3.0  1.0  4.0  3.0  1.0  10.0
26  11.0  3.0  1.0  4.0  3.0  1.0   7.0
27  12.0  3.0  1.0  5.0  3.0  1.0   6.0
28  12.0  3.0  1.0  5.0  3.0  1.0  10.0
29  12.0  3.0  1.0  5.0  3.0  1.0   7.0
30  13.0  3.0  2.0  6.0  3.0  2.0  11.0
31  13.0  3.0  2.0  6.0  3.0  2.0   8.0
32  14.0  3.0  2.0  7.0  3.0  2.0  11.0
33  14.0  3.0  2.0  7.0  3.0  2.0   8.0
```

# Notice
pandas_bj only supports dataframe with RangeIndex. 
Make sure your dataframes have RangeIndex, and if you not then use reset_index() to make it so.

# Options

#### how
- inner
- left
- right
- outer

#### sort
- bool
    - `True` to use sort for all join keys
    - `False` not to use sort for all join keys
- List of ints
    - `[0, 1]` to use sort for first and second join keys
    - `[]` equals to `False`

# Performance

#### Performance test

- Randomly generate X and Y data frames.
- Both X and Y has integer id1: (0, 100] and integer id2: (0, 50].
- X has float s: (0, 1000] and e: (0, 1000] and e >= s.
- Y has float v: (0, 1000].
- Use left_on=`['id1', 'id2', pandas_bj.Between('s', 'e')]`, right_on=`['id1', 'id2', 'v']`

See `test/performance.py` for more information.

#### Result

| X record count | Y record count | use Sort | Time in sec | Joined Y record count per X |
| :--- | :--- | --- | :--- | :--- |
|100 | 1,000 | False | 0.1776 | 1.0 |
|100 | 1,000 | True | 0.0913 | 1.0 |
|1,000 | 10,000 | False | 10.9851 | 1.4669 |
|1,000 | 10,000 | True | 0.4158 | 1.4669 |
|10,000 | 100,000 | True | 5.6312 | 6.0406 |
|10,000 | 1,000,000 | True | 57.0484 | 51.8505 |

The result shows that if you want to join  `10,000` rows Y with `1,000,000` rows X, and it is expected that 
`50` X for each Y record in average, then pandas-bj can finish process in 60 seconds.
