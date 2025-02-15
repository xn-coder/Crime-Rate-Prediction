from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
import joblib
from preprocessing import load_and_preprocess_data

def train_and_save_model():
    data = load_and_preprocess_data()
    
    # Clean data before processing
    data = data.loc[:, ~data.columns.duplicated()]
    data = data.dropna(axis=1, how='all')
    
    target = 'Victims_of_Rape_Total'
    features = [col for col in data.columns if col not in [target, 'Area_Name', 'Year']]
    
    # Handle remaining NaN values
    imputer = SimpleImputer(strategy='median')
    imputed_data = imputer.fit_transform(data[features])
    data[features] = imputed_data
    
    X_train, X_test, y_train, y_test = train_test_split(
        data[features], data[target], test_size=0.2, random_state=42
    )
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save the model
    joblib.dump(model, 'models/crime_prediction_model.pkl')
    joblib.dump(imputer, 'models/imputer.pkl')  # Save imputer for inference
    joblib.dump(features, 'models/feature_names.pkl')  # Save feature list

if __name__ == "__main__":
    train_and_save_model() 