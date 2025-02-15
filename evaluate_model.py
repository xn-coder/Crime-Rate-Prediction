from sklearn.metrics import mean_absolute_error
import joblib
import pandas as pd
from preprocessing import load_and_preprocess_data

def evaluate_model():
    data = load_and_preprocess_data()
    model = joblib.load('models/crime_prediction_model.pkl')
    
    target = 'Victims_of_Rape_Total'
    features = [col for col in data.columns if col not in [target, 'Area_Name', 'Year']]
    
    predictions = model.predict(data[features])
    mae = mean_absolute_error(data[target], predictions)
    
    print(f'Model MAE: {mae:.2f}')
    print("\nFeature Importances:")
    print(pd.Series(model.feature_importances_, index=features).sort_values(ascending=False).head(10))

if __name__ == "__main__":
    evaluate_model() 