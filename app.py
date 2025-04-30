from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv"],
    allow_credentials=True,
    allow_methods=["https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv"],
    allow_headers=["https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv"],
)

modelo = joblib.load("best_model.pkl")

class DatosModelo(BaseModel):
    zn: float
    indus: float
    rm: float
    ptratio: float
    b: float
    lstat: float

@app.post("/predict/")
def predict(data: DatosModelo):
    try:
        X = [[
            data.zn,
            data.indus,
            data.rm,
            data.ptratio,
            data.b,
            data.lstat
        ]]
        pred = modelo.predict(X)[0]
        return {"prediction": pred}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return {"message": "API de predicción de precios de Boston Housing"}
