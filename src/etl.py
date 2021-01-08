import os
import pandas as pd
from pandas_profiling import ProfileReport


def main():
    # os.system('src/etl.sh')

    def normalize(x):
        dictionary = eval(x)
        if dictionary:
            return list(dictionary.values())

    movies = pd.read_csv(
        'data/raw/movie.metadata.tsv',
        converters={'languages': normalize, 'countries': normalize, 'genres': normalize},
        delimiter='\t',
        header=None,
        index_col='id',
        names='id name date revenue runtime languages countries genres'.split(),
        usecols=[0, 2, 3, 4, 5, 6, 7, 8]
    ).assign(date=lambda x: pd.to_datetime(x.date, errors='coerce'))

    summaries = pd.read_csv(
        'data/raw/plot_summaries.txt',
        delimiter='\t',
        header=None,
        index_col='id',
        names='id summary'.split())

    df = movies.merge(summaries, on='id').sort_values('date').reset_index(drop=True)
    df.to_pickle('data/out/data.pkl')
    ProfileReport(df).to_file('data/out/report.html')


if __name__ == '__main__':
    main()