import joblib
import pandas as pd
import os.path as osp

from pydantic import BaseModel
from fastapi import FastAPI, Depends
from sklearn.pipeline import Pipeline
from typing import List, Optional, Tuple, Dict


class PredictionInput(BaseModel):
    file_name: str

class PredictionOutput(BaseModel):
    up_down: List[Dict]

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

    async def predict(self, input: PredictionInput) -> PredictionOutput:
        """Runs a prediction"""
        if not self.model or not self.classes:
            raise RuntimeError("Model is not loaded")
        data_file = osp.join(osp.dirname(__file__), input.file_name)
        data = pd.read_csv(data_file)
        data['trade_date'] = pd.to_datetime(data['trade_date'])
        data.set_index("trade_date", inplace=True)
        data.sort_index(inplace=True)
        test_data = data.loc['2025-01-01': '2025-09-11']
        trading_dates = test_data.reset_index()["trade_date"].astype(str)
        test_data = test_data.drop(columns=['change', 'vol', 'amount'])
        prediction = self.model.predict(test_data)
        up_down = []
        for val in prediction:
            up_down.append(self.classes.get(str(int(val)), "unkown"))
        result_pd = pd.DataFrame({
            "trade_date": trading_dates,
            "up_down": up_down
        })
        result_dict = result_pd.to_dict('records')

        return PredictionOutput(up_down=result_dict)

app = FastAPI()
newgroups_model = NewsgroupsModel()

@app.post("/prediction")
async def prediction(
        output: PredictionOutput = Depends(newgroups_model.predict)
) -> PredictionOutput:

    return output

@app.on_event("startup")
async def startup():
    newgroups_model.load_model()
