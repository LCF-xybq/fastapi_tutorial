import time
import joblib
import pandas as pd
import os.path as osp

from pydantic import BaseModel
from sklearn.pipeline import Pipeline
from fastapi import FastAPI, Depends, status
from typing import List, Optional, Tuple, Dict


class PredictionInput(BaseModel):
    file_name: str

class PredictionOutput(BaseModel):
    up_down: List[Dict]

memory = joblib.Memory(location="test_cache.joblib")

@memory.cache(ignore=["model"])
def predict(model: Pipeline, file_name: str)  -> Tuple[list, pd.DataFrame]:
    data_file = osp.join(osp.dirname(__file__), file_name)
    data = pd.read_csv(data_file)
    data['trade_date'] = pd.to_datetime(data['trade_date'])
    data.set_index("trade_date", inplace=True)
    data.sort_index(inplace=True)
    test_data = data.loc['2025-01-01': '2025-09-11']
    trading_dates = test_data.reset_index()["trade_date"].astype(str)
    test_data = test_data.drop(columns=['change', 'vol', 'amount'])
    prediction = model.predict(test_data)
    return (prediction, trading_dates)

class NewsgroupsModel:
    model: Optional[Pipeline]
    targets: Optional[List[str]]

    def load_model(self):
        """Loads the model"""
        model_file = osp.join(osp.dirname(__file__), "test.joblib")
        loaded_model: Tuple[Pipeline, List[str]] = joblib.load(model_file)
        model, classes = loaded_model
        self.model = model
        self.classes =classes

    def predict(self, input: PredictionInput) -> PredictionOutput:
        """Runs a prediction"""
        start_time = time.time()
        if not self.model or not self.classes:
            raise RuntimeError("Model is not loaded")
        prediction, trading_dates = predict(self.model, input.file_name)
        up_down = []
        for val in prediction:
            up_down.append(self.classes.get(str(int(val)), "unkown"))
        result_pd = pd.DataFrame({
            "trade_date": trading_dates,
            "up_down": up_down
        })
        result_dict = result_pd.to_dict('records')
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"耗时: {elapsed_time:.4f}秒")

        return PredictionOutput(up_down=result_dict)

app = FastAPI()
newgroups_model = NewsgroupsModel()

@app.post("/prediction")
async def prediction(
        output: PredictionOutput = Depends(newgroups_model.predict)
) -> PredictionOutput:

    return output

@app.delete("/cache", status_code=status.HTTP_204_NO_CONTENT)
def delete_cache():
    memory.clear()

@app.on_event("startup")
async def startup():
    newgroups_model.load_model()
