"""
Есть Pandas DataFrame со столбцами [“customer_id”, “product_id”, “timestamp”],
который содержит данные по просмотрам товаров на сайте.
Есть проблема – просмотры одного customer_id не разбиты на сессии (появления на сайте).
Мы хотим разместить сессии так, чтобы сессией считались все смежные просмотры,
между которыми не более 3 минут.

Написать методом который создаст в Pandas DataFrame столбец session_id
и проставит в нем уникальный int id для каждой сессии.

У каждого пользователя может быть по несколько сессий.
Исходный DataFrame может быть большим – до 100 млн строк.
"""
import pandas as pd
import numpy as np


def create_data(size:int, cols:str, col_names = None, intervals = None, seed = None)->pd.DataFrame:
    """
    Generate Data
    """
    rng = np.random.default_rng(seed)
    df = pd.DataFrame()
    timstamp_start = pd.Timestamp("2021-01-01 12:00:00").timestamp()
    timstamp_end = pd.Timestamp("2021-01-01 12:20:00").timestamp()
    default_intervals = {"i" : (0,10), "t" : (timstamp_start,timstamp_end)}
    suffix = {"i" : "int", "t" : "timestamp"}
    if col_names is None:
        col_names = [f"column_{str(i)}_{suffix.get(col)}" for i, col in enumerate(cols)]
    for col, col_name, interval in zip(cols, col_names, intervals):
        if interval is None:
            interval = default_intervals[col]
        start, end = interval
        if col == "i":
            df[col_name] = rng.integers(start, end, size)
        elif col == "t":
            df[col_name] = rng.integers(start, end,size )
    return df


def solver(df)->pd.DataFrame:
    # Sorting at customer_id, then timestamp
    df = df.sort_values(['customer_id', 'timestamp'], ascending=[True, True])
    df = df.reset_index(drop=True)
    #Set session columna default value
    df['session'] = 1
    for i in range(1, len(df)):
        #Check matching customer_id
        if (df.loc[i, 'customer_id'] == df.loc[i - 1, 'customer_id']):
            #Check diff timestamp
            if (df.loc[i, 'timestamp'] - df.loc[i - 1, 'timestamp'] >= 180):
                df.loc[i:, 'session'] = df.loc[i, 'session'] + 1
        else:
            df.loc[i:, 'session'] = 1
    #Sorting at timestamp
    df = df.sort_values('timestamp', ascending=True)
    df = df.reset_index(drop=True)
    return df


if __name__ == '__main__':
    df = create_data(size = 30, cols =  "iit", col_names=['customer_id', 'product_id', 'timestamp'],
                intervals = [(1,5), (1, 10), None], seed=10)
    df = solver(df)
    print(df.head(30))