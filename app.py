from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

# Load the trained model
model = joblib.load('optimized_xgboost_model.joblib')

# Define the input data schema
class InsuranceData(BaseModel):
    age: int
    gender: str
    marital_status: str
    vehicle_age: int
    vehicle_type: str
    annual_mileage: int
    location: str
    num_claims: int
    credit_score: int
    coverage_type: str

# Define the prediction endpoint
@app.post("/predict/")
def predict_premium(data: InsuranceData):
    # Convert the data to a DataFrame
    input_df = pd.DataFrame([data.dict()])
    
    # One-Hot Encoding (same as training)
    categorical_cols = ['gender', 'marital_status', 'vehicle_type', 'location', 'coverage_type']
    input_encoded = pd.get_dummies(input_df, columns=categorical_cols, drop_first=True)
    
    # Ensure all expected columns are present
    missing_cols = set(X.columns) - set(input_encoded.columns)
    for col in missing_cols:
        input_encoded[col] = 0  # Assign 0 to missing columns
    
    # Reorder columns to match training data
    input_encoded = input_encoded[X.columns]
    
    # Predict
    prediction = model.predict(input_encoded)
    
    return {"predicted_premium": prediction[0]}
