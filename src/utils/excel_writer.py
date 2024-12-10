import pandas as pd

def save_to_excel(test_results, data, filename="results/test_results.xlsx"):
    try:
        # Create a pandas ExcelWriter object
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Save test_results to Sheet1
            df_test_results = pd.DataFrame(test_results)
            df_test_results.to_excel(writer, sheet_name="Sheet1", index=False)
            
            # Save data to Sheet2
            df_data = pd.DataFrame(data)
            df_data.to_excel(writer, sheet_name="Sheet2", index=False)
        
        print(f"Data saved successfully to {filename}")
    except Exception as e:
        print(f"Error saving to Excel: {e}")

