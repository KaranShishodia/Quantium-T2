import pandas as pd
import os

# Define the input files
input_files = [
    'daily_sales_data_0.csv', 
    'daily_sales_data_1.csv', 
    'daily_sales_data_2.csv'
]

def process_data():
    df_list = []
    
    # 1. Load and combine the CSV files
    for file in input_files:
        if os.path.exists(file):
            df_list.append(pd.read_csv(file))
    
    if not df_list:
        print("No input files found.")
        return

    df = pd.concat(df_list, ignore_index=True)

    # 2. Filter for Pink Morsels only
    df = df[df['product'].str.lower() == 'pink morsel']

    # 3. Create 'sales' field (Price * Quantity)
    # Remove '$' from price and convert to float
    df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
    df['sales'] = df['price'] * df['quantity']

    # 4. Keep only required fields: Sales, Date, Region
    df = df[['sales', 'date', 'region']]

    # 5. Export to the formatted output file
    df.to_csv('formatted_data.csv', index=False)
    print("Successfully created formatted_data.csv")

if __name__ == '__main__':
    process_data()