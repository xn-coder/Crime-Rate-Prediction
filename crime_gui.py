import tkinter as tk
from tkinter import ttk
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from preprocessing import load_and_preprocess_data

class CrimePredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crime Prediction System")
        
        # Load data and model
        self.data = load_and_preprocess_data()
        self.model = joblib.load('models/crime_prediction_model.pkl')
        self.imputer = joblib.load('models/imputer.pkl')
        self.feature_names = joblib.load('models/feature_names.pkl')
        
        # Create GUI components
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid(row=0, column=0)
        
        # Area selection
        ttk.Label(main_frame, text="Select Area:").grid(row=0, column=0)
        self.area_var = tk.StringVar()
        self.area_cb = ttk.Combobox(main_frame, textvariable=self.area_var)
        self.area_cb['values'] = sorted(self.data['Area_Name'].unique())
        self.area_cb.grid(row=0, column=1)
        
        # Year selection
        ttk.Label(main_frame, text="Select Year:").grid(row=1, column=0)
        self.year_var = tk.StringVar()
        self.year_cb = ttk.Combobox(main_frame, textvariable=self.year_var)
        self.year_cb['values'] = sorted(self.data['Year'].unique())
        self.year_cb.grid(row=1, column=1)
        
        # Predict button
        predict_btn = ttk.Button(main_frame, text="Predict", command=self.predict)
        predict_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Result display
        self.result_label = ttk.Label(main_frame, text="")
        self.result_label.grid(row=3, column=0, columnspan=2)
    
    def predict(self):
        area = self.area_var.get()
        year = int(self.year_var.get())
        
        # Get latest data for the selected area
        area_data = self.data[(self.data['Area_Name'] == area) & (self.data['Year'] == year)]
        
        if not area_data.empty:
            features = area_data.drop(['Area_Name', 'Year', 'Victims_of_Rape_Total'], axis=1)
            # Align features with training structure
            features = features.reindex(columns=self.feature_names, fill_value=0)
            features = self.imputer.transform(features)
            prediction = self.model.predict(features)
            self.result_label.config(text=f"Predicted Crime Risk: {prediction[0]:.2f}")
        else:
            self.result_label.config(text="No data available for selected parameters")

if __name__ == "__main__":
    root = tk.Tk()
    app = CrimePredictorApp(root)
    root.mainloop() 