# %%
import timeit
import numpy as np
import numpy.random
import pandas as pd

def randint_series(n_rows, n_vals=5):
    return pd.Series(numpy.random.randint(n_vals, size=(n_rows,)))

def random_series(n_rows):
    return pd.Series(numpy.random.random((n_rows,)))

def rand_str_series(n_rows, str_len=8):
    A, Z = np.array(['A', 'Z']).view('int32')
    return pd.Series(np.random.randint(low=A, high=Z, size=n_rows * str_len,
                                       dtype='int32').view(f'U{str_len}'))

def test_df1(n_rows, n_str=10):
    few_str = rand_str_series(n_str).sample(n_rows, replace=True, ignore_index=True)
    return pd.DataFrame({'int1': randint_series(n_rows),
                         'int2': randint_series(n_rows),
                         'str1': rand_str_series(n_rows, str_len=8),
                         'few_str': few_str,
                         'float': random_series(n_rows)})

def time_filtering_methods(n_rows, sort_df_first=False):
    df = test_df1(n_rows)
    if sort_df_first:
        df = df.sort_values(by=['int1', 'int2', 'str1', 'few_str'])
    reps = 10
    int1_boolean = timeit.timeit("""df[df['int1']==1]""", globals={'df': df}, number=reps)
    print('on int1 by boolean', int1_boolean)
    int2_boolean = timeit.timeit("""df[df['int2']==1]""", globals={'df': df}, number=reps)
    few_str_boolean = timeit.timeit("""df[df['few_str']==df.loc[0, 'few_str']]""", 
                                    globals={'df': df}, number=reps)

    df_idx = df.set_index(['int1'])
    int1_idx = timeit.timeit("""df.loc[1]""", globals={'df': df_idx}, number=reps)
    print('on int1 index by loc', int1_idx)

    df_idx = df_idx.sort_index()
    int1_idx_sorted = timeit.timeit("""df.loc[1]""", globals={'df': df_idx}, number=reps)
    print('on int1 sorted index by loc', int1_idx_sorted)

    df_idx = df.set_index(['int1', 'int2'])
    int1_idx_all = timeit.timeit("""df.loc[1]""", globals={'df': df_idx}, number=reps)
    print('on int1 by loc with index for all', int1_idx_all)

    df_idx = df_idx.sort_index()
    int1_idx_all_sorted = timeit.timeit("""df.loc[1]""", globals={'df': df_idx}, number=reps)
    print('on int1 by loc with sorted index for all', int1_idx_all_sorted)

    int2_idx_all_sorted = timeit.timeit("""df.loc[(slice(None), 1), :]""", 
                                        globals={'df': df_idx}, number=reps)
    print('on int2 by loc with sorted index for all', int2_idx_all_sorted)

    int2_idx_all_sorted_xs = timeit.timeit("""df.xs(1, level='int2')""", 
                                        globals={'df': df_idx}, number=reps)
    print('on int2 by loc with sorted index for all (xs)', int2_idx_all_sorted_xs)

    int1_int2_idx_all_sorted = timeit.timeit("""df.loc[(1, 1)]""", 
                                        globals={'df': df_idx}, number=reps)
    print('on int1 & int2 by loc with sorted index for all', int1_int2_idx_all_sorted)



    return df, df_idx
# %%
