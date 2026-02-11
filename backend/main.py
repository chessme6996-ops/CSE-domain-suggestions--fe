import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import pandas as pd
import joblib

scaler = joblib.load("scaler.pkl")
pca = joblib.load("pca.pkl")
frf_model = joblib.load("frf.pkl")

corr_features = ['Computer Architecture', 'Programming Skills', 'Project Management', 'Communication skills']
other_features = ['Openness', 'Conscientousness', 'Extraversion', 'Agreeableness', 'Emotional_Range', 
                  'Conversation', 'Openness to Change', 'Hedonism', 'Self-enhancement', 'Self-transcendence']

role_mapping = {0: 'Database Administrator', 1: 'Hardware Engineer', 2: 'Application Support Engineer', 
                3: 'Cyber Security Specialist', 4: 'Networking Engineer', 5: 'Software Developer', 
                6: 'API Specialist', 7: 'Project Manager', 8: 'Information Security Specialist', 
                9: 'Technical Writer', 10: 'AI ML Specialist', 11: 'Software Tester', 
                12: 'Business Analyst', 13: 'Customer Service Executive', 14: 'Helpdesk Engineer', 15: 'Graphics Designer'}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://purpose-next-app.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    values: list

@app.get("/")
def home():
    return {"status": "Backend is live"}

@app.post("/predict")
def predict_career(data: UserInput):
    sample_input = np.array([data.values])
    sample_df = pd.DataFrame(sample_input, columns=corr_features + other_features)

    scaled_corr = scaler.transform(sample_df[corr_features])
    pca_corr = pca.transform(scaled_corr)
    sample_df = sample_df.drop(columns=corr_features)
    sample_df[['PCA_1', 'PCA_2']] = pca_corr

    predicted_index = frf_model.predict(sample_df)[0]
    return {"predicted_role": role_mapping[predicted_index]}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

