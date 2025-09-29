import os
import joblib
import pandas as pd
from typing import List, Tuple
from sklearn.pipeline import Pipeline


if __name__ == "__main__":
    sec_code = '601012'
    data = pd.read_csv(r"C:\Users\liuchufan\Documents\{0}_factor.csv".format(sec_code))
    data['trade_date'] = pd.to_datetime(data['trade_date'])
    data.set_index("trade_date", inplace=True)
    data.sort_index(inplace=True)
    test_data = data.loc['2025-01-01': '2025-09-11']
    test_data = test_data.drop(columns=['change', 'vol', 'amount'])

    model_file = os.path.join(os.path.dirname(__file__), "test.joblib")
    loaded_model: Tuple[Pipeline, List[str]] = joblib.load(model_file)
    model, target = loaded_model

    pred = model.predict(test_data)
    print(pred)
    print(target)
