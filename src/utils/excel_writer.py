import pandas as pd

def save_to_excel(h1_test_results,h1_h6_test_results,image_test_result,url_test_results,currency_result, data, filename="results/test_results.xlsx"):
    try:
        # Create a pandas ExcelWriter object
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Save test_results to Sheet1
            df_test_results = pd.DataFrame(h1_test_results)
            df_test_results.to_excel(writer, sheet_name="Sheet1", index=False)
            
            # Save test_results to Sheet2
            df_test_results = pd.DataFrame(h1_h6_test_results)
            df_test_results.to_excel(writer, sheet_name="Sheet2", index=False)
            
            # Save test_results to Sheet3
            df_test_results = pd.DataFrame(image_test_result)
            df_test_results.to_excel(writer, sheet_name="Sheet3", index=False)
            
            # Save test_results to Sheet4
            df_test_results = pd.DataFrame(url_test_results)
            df_test_results.to_excel(writer, sheet_name="Sheet4", index=False)
            
            # Save data to Sheet5
            df_data = pd.DataFrame(currency_result)
            df_data.to_excel(writer, sheet_name="Sheet5", index=False)

            # Save data to Sheet6
            df_data = pd.DataFrame(data)
            df_data.to_excel(writer, sheet_name="Sheet6", index=False)
        
        print(f"Data saved successfully to {filename}")
    except Exception as e:
        print(f"Error saving to Excel: {e}")

