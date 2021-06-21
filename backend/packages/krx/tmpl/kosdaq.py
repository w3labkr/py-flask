# Miscellaneous operating system interfaces
import os

# Flexible and powerful data analysis / manipulation library for Python, providing labeled data structures similar to R data.frame objects, statistical functions, and much more
import pandas as pd

# Set absolute module path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
MODULE_PATH = os.path.dirname(BASE_PATH)
DATA_PATH = os.path.join(MODULE_PATH, 'data')


def main(**kwargs):
    df = pd.read_csv(DATA_PATH + '/kosdaq.csv')
    df = df[['종목코드', '기업명']]

    df['종목코드'] = df['종목코드'].astype(str).str.zfill(6)
    df.set_index('종목코드', inplace=True)
    df.rename(columns={
        '기업명': 'codes'
    }, inplace=True)

    return df.to_json(orient='columns', force_ascii=False)


if __name__ == '__main__':
    main()
