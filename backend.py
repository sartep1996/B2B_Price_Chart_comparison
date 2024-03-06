import pandas as pd
import PySimpleGUI as sg
from datetime import datetime



def find_matching_addresses(file_paths, output_file, threshold_balance, address_column, price_column, abbreviation):
    dfs = [pd.read_csv(file_path, header=None, skiprows=1, skipfooter=1, engine='python') for file_path in file_paths]


    addresses_sets = [set(df.iloc[:, address_column].astype(str)) for df in dfs]
    common_addresses = set.intersection(*addresses_sets)

    column_names = ["Address"] + [f"Balance_{abbreviation}"]
    consolidated_df = pd.DataFrame(columns=column_names)

    for address in common_addresses:
        balances = []
        for df in dfs:
            address_mask = df.iloc[:, address_column].astype(str) == address
            if address_mask.any():  # Check if there are any matches
                balance = df.loc[address_mask, price_column].str.replace(',', '').astype(float).values
                if len(balance) > 0: 
                    balances.append(balance[0])
                else:
                    balances.append(0)
            else:
                print(f"No matching address '{address}' found in DataFrame from {file_paths}")

        if all(balance > float(threshold_balance) for balance in balances):
            row_data = [address] + balances
            consolidated_df = pd.concat([consolidated_df, pd.DataFrame([row_data], columns=column_names)], ignore_index=True)


    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_path = f'{output_file}\\Crypto_Files_{timestamp}.xlsx'

    with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
        consolidated_df.to_excel(writer, sheet_name='Sheet1', index=False, header=True)

    return output_file_path

def configure_columns_layout(file_path):
    df = pd.read_csv(file_path, nrows=5, encoding='latin-1')
    rows = [
        [sg.Text(f"Sample data from {file_path}:")],
        [sg.Table(values=df.values.tolist(), headings=df.columns.tolist(),
                  auto_size_columns=True, justification='right')],
        [sg.Text("Select the column for Wallet Address:"), sg.InputCombo(values=df.columns.tolist(), key='ADDRESS_COLUMN')],
        [sg.Text("Select the column for Price:"), sg.InputCombo(values=df.columns.tolist(), key='PRICE_COLUMN')],
        [sg.Text('Select Abbreviation:'), sg.InputText(default_text="PVZ", key="ABBREVIATION")],
        [sg.Button("OK")]
    ]
    return sg.Window("Configure Columns", rows, finalize=True)
