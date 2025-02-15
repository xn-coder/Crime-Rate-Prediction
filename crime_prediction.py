import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Load and preprocess data
def load_data():
    # Property crimes data
    property_df = pd.read_csv('crime/10_Property_stolen_and_recovered.csv')
    property_agg = property_df.groupby(['Area_Name', 'Year', 'Subgroup']).sum().unstack()
    property_agg.columns = [f'Property_{col[1]}' for col in property_agg.columns]
    
    # Rape cases data
    rape_df = pd.read_csv('crime/20_Victims_of_rape.csv')
    rape_agg = rape_df[rape_df['Subgroup'] == 'Total Rape Victims'].groupby(['Area_Name', 'Year']).sum()
    
    # Police complaints data
    police_df = pd.read_csv('crime/25_Complaints_against_police.csv')
    police_agg = police_df.groupby(['Area_Name', 'Year']).sum()
    
    # Merge datasets
    merged_df = pd.merge(property_agg, rape_agg, on=['Area_Name', 'Year'])
    merged_df = pd.merge(merged_df, police_agg, on=['Area_Name', 'Year'])
    
    return merged_df

# Feature engineering
def create_features(df):
    # Create time-lagged features
    df = df.sort_values(['Area_Name', 'Year'])
    for col in df.columns:
        if col not in ['Area_Name', 'Year']:
            df[f'{col}_lag1'] = df.groupby('Area_Name')[col].shift(1)
    
    # Drop initial null values from lagging
    df = df.dropna()
    return df

# Main workflow
def main():
    # Load and prepare data
    data = load_data()
    data = create_features(data)
    
    # Define target and features
    target = 'Victims_of_Rape_Total'
    features = [col for col in data.columns if col not in [target, 'Area_Name', 'Year']]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        data[features], data[target], test_size=0.2, random_state=42
    )
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f'Mean Absolute Error: {mae:.2f}')
    
    # Feature importance
    importance = pd.Series(model.feature_importances_, index=features)
    print("\nTop 10 Features:")
    print(importance.sort_values(ascending=False).head(10))

if __name__ == "__main__":
    main() 