import pandas as pd

def load_and_preprocess_data():
    # Property crimes data
    property_df = pd.read_csv('crime/10_Property_stolen_and_recovered.csv')
    # Convert numeric columns explicitly
    numeric_cols = ['Cases_Property_Recovered', 'Cases_Property_Stolen', 
                    'Value_of_Property_Recovered', 'Value_of_Property_Stolen']
    property_df[numeric_cols] = property_df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    property_agg = property_df.groupby(['Area_Name', 'Year', 'Sub_Group_Name']).sum().unstack()
    # Flatten multi-index columns and format names
    property_agg.columns = [f'{col[0]}_{col[1].replace(" ", "_").replace(".", "")}' 
                           .replace("__", "_")  # Handle double underscores from decimal replacement
                           for col in property_agg.columns]
    
    # Ensure unique column names
    property_agg = property_agg.loc[:, ~property_agg.columns.duplicated()]
    
    # Drop completely empty columns
    property_agg = property_agg.dropna(axis=1, how='all')
    
    # Rape cases data
    rape_df = pd.read_csv('crime/20_Victims_of_rape.csv')
    rape_df = rape_df.apply(pd.to_numeric, errors='ignore')  # Preserve categorical columns
    rape_agg = rape_df[rape_df['Subgroup'] == 'Total Rape Victims'].groupby(['Area_Name', 'Year']).sum()
    
    # Police complaints data
    police_df = pd.read_csv('crime/25_Complaints_against_police.csv')
    police_df = police_df.apply(pd.to_numeric, errors='coerce')
    police_agg = police_df.groupby(['Area_Name', 'Year']).sum()
    
    # Merge datasets
    merged_df = pd.merge(property_agg, rape_agg, on=['Area_Name', 'Year'], how='outer')
    merged_df = pd.merge(merged_df, police_agg, on=['Area_Name', 'Year'], how='outer')
    
    # Ensure all numeric columns
    for col in merged_df.select_dtypes(include=['object']).columns:
        merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')
    
    # Fill missing values
    merged_df = merged_df.groupby('Area_Name').ffill().bfill()
    
    # Create time-lagged features
    merged_df = merged_df.sort_values(['Area_Name', 'Year'])
    for col in merged_df.columns:
        if col not in ['Area_Name', 'Year']:
            merged_df[f'{col}_lag1'] = merged_df.groupby('Area_Name')[col].shift(1)
    
    # Only drop rows missing target variable
    return merged_df.dropna(subset=['Victims_of_Rape_Total']).reset_index() 