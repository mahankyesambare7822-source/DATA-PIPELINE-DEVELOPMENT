import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
import os

# --- 1. DATA EXTRACTION ---
def extract_data(file_path):
    if not os.path.exists(file_path):
        df_sample = pd.DataFrame({
            'age': [25, 30, 35, 45, 22, 50, 28, 40, 32, 48],
            'income': [50000, 62000, 75000, 95000, 42000, 110000, 58000, 88000, 65000, 105000],
            'city': ['Mumbai', 'London', 'London', 'Mumbai', 'Mumbai', 'London', 'Mumbai', 'London', 'Mumbai', 'London'],
            'gender': ['M', 'F', 'F', 'M', 'F', 'M', 'M', 'F', 'M', 'F']
        })
        df_sample.to_csv(file_path, index=False)
    return pd.read_csv(file_path)

# --- 2. MAIN EXECUTION ---
if __name__ == "__main__":
    # A. Get and Clean Data
    df = extract_data('data.csv')
    df_clean = df.dropna(subset=['income']) 
    
    # B. Build Pipeline & Train
    preprocessor = ColumnTransformer([
        ('num', Pipeline([('imp', SimpleImputer()), ('std', StandardScaler())]), ['age']),
        ('cat', Pipeline([('imp', SimpleImputer(strategy='constant')), ('one', OneHotEncoder())]), ['city', 'gender'])
    ])
    model_pipeline = Pipeline([('prep', preprocessor), ('reg', LinearRegression())])
    
    X = df_clean.drop('income', axis=1)
    y = df_clean['income']
    model_pipeline.fit(X, y)
    
    # C. Make Predictions for a few people
    test_people = pd.DataFrame({
        'age': [27, 33, 42],
        'city': ['Mumbai', 'London', 'Mumbai'],
        'gender': ['M', 'F', 'M']
    })
    predictions = model_pipeline.predict(test_people)
    test_people['Predicted_Income'] = predictions

    # --- D. EXCEL LOADING (The Professional Part) ---
    print("--- Generating Excel Report ---")
    with pd.ExcelWriter('Pipeline_Report.xlsx', engine='openpyxl') as writer:
        # Sheet 1: The Raw Data used
        df_clean.to_excel(writer, sheet_name='Cleaned_Source_Data', index=False)
        
        # Sheet 2: The Predictions made by the AI
        test_people.to_excel(writer, sheet_name='AI_Predictions', index=False)

    print("-" * 30)
    print("SUCCESS: 'Pipeline_Report.xlsx' created in your folder!")
    print("-" * 30)
    