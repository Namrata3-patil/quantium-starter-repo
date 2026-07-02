import os
import pandas as pd

# 1. Define paths to the data folder and the files
data_dir = "./data"
files = ["daily_sales_data_0.csv", "daily_sales_data_1.csv", "daily_sales_data_2.csv"]

dfs = []

# 2. Read and process each file
for file in files:
    file_path = os.path.join(data_dir, file)
    
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Filter: Keep ONLY rows where the product is 'pink morsel'
    # (Using .str.lower() ensures we catch it even if capitalization varies)
    df = df[df["product"].str.lower() == "pink morsel"]
    
    # Clean up formatting: Strip any whitespace or '$' symbols from the price column
    if df["price"].dtype == "object":
        df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)
    else:
        df["price"] = df["price"].astype(float)
        
    df["quantity"] = df["quantity"].astype(int)
    
    # Combine: Calculate 'sales' by multiplying quantity and price
    df["sales"] = df["quantity"] * df["price"]
    
    # Select only the required fields: sales, date, region
    df = df[["sales", "date", "region"]]
    
    # Add to our list of dataframes
    dfs.append(df)

# 3. Combine all three datasets into one
combined_df = pd.concat(dfs, ignore_index=True)

# 4. Save the cleanly formatted output to a new CSV file
output_path = "./formatted_output.csv"
combined_df.to_csv(output_path, index=False)

print(f"Success! Cleaned data saved to {output_path}")