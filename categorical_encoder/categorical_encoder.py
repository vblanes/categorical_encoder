from sklearn.base import BaseEstimator, TransformerMixin


class CategoricalEncoder(BaseEstimator, TransformerMixin):

    def __init__(self, columns):
        # list of dictionaries, one per column
        self.dicts = []
        # list of strings (columname)
        self.columns = columns
        self.fit_ = False

    def fit(self, df, y=None):
        for col in self.columns:
            # flexibility for missing columns
            if col not in df.columns.values:
                # OJO ESTO
                self.dicts.append({})

            dictionary = {}
            lst = df[col]

            for element in lst:
                if element not in dictionary:
                    # avoid None as category
                    if element is not None and type(element) == str:
                        dictionary[element] = len(dictionary)
            self.dicts.append(dictionary)
        self.fit_ = True
        return self

    def transform(self, df):
        # iterate over columns to be transformed
        for ind, col in enumerate(self.columns):
            # flexibility for missing columns
            if col not in df.columns.values:
                continue

            lst = df[col]
            new_col = []
            # transform elements 1 by 1
            for element in lst:
                if element in self.dicts[ind]:
                    new_col.append(self.dicts[ind][element])
                else:
                    new_col.append(-1)
            # insert this new column in the df
            df = df.assign(**{col: new_col})
        return df

    def get_values_column(self, col_name):
        """
        Method created to automatize the django file creation
        returns the possible values of a column
        """
        for ind, col in enumerate(self.columns):
            if col == col_name:
                return [str(k) for k in self.dicts[ind].keys()]
        else:
            # not found in the for
            return None