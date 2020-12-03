from categorical_encoder import CategoricalEncoder
import unittest
import pandas as pd

class TestCategoricalEncoder(unittest.TestCase):
    
    def test_basic(self):
        df = [
            {'col1':'papa', 'col2':'pepe'},
            {'col1':'pepe', 'col2':'papa'},
            {'col1':'pipi', 'col2':'pipi'},
            {'col1':'papa', 'col2':'popo'},
        ]

        df = pd.DataFrame(df)
        enc = CategoricalEncoder(columns=['col1', 'col2'])
        res = enc.fit_transform(df)
        unittest.assertEquals(list(res['col1']), [0, 1, 2, 0])
        
