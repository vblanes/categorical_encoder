from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class CategoricalEncoder(BaseEstimator, TransformerMixin):

    def __init__(self, columns, missing_value=-1):
        # list of dictionaries, one per column
        self.translators = {}
        # list of strings (columname)
        self.columns = columns
        self.fit_ = False
        self.missing_value = missing_value

    # TODO add support for numpy arrays, noy only pandas dataframes
    def fit(self, df, y=None):
        if self.fit_:
            raise Exception("Categorical Encoder is already fit")
        for col in self.columns:
            # flexibility for missing columns
            if col not in df.columns.values:
                continue

            trans_ = {}
            lst = df[col]
            for element in lst:
                if element not in trans_:
                    # avoid None as category
                    if not pd.isnull(element) and type(element) == str:
                        trans_[element] = len(trans_)
            self.translators[col] = trans_
        self.fit_ = True
        return self

    def transform(self, df):
        # iterate over columns to be transformed
        for col in self.columns:
            # flexibility for missing columns
            if col not in df.columns.values:
                continue

            lst = df[col]
            new_col = []
            # transform elements 1 by 1
            # TODO use apply instead of 1 be 1 transformation
            for element in lst:
                if element in self.dicts[ind]:
                    new_col.append(self.dicts[ind][element])
                else:
                    new_col.append(self.missing_value)
            # insert this new column in the df
            df = df.assign(**{col: new_col})
        return df

    def get_map_column(self, col_name):
        return self.translators.get(col_name)