import pandas as pd
import PySimpleGUI as sg
from datetime import datetime

def find_matching_addresses(file_paths, output_file, threshold_balance=10000):
    dfs = [pd.read_csv(file_path, header=None, skiprows=1) for file_path in file_paths]

    addresses_sets = [set(df.iloc[:, 0].astype(str)) for df in dfs]
    common_addresses = set.intersection(*addresses_sets)

    num_files = len(file_paths)
    column_names = ["Address"] + [f"Balance_{i+1}" for i in range(num_files)]
    consolidated_df = pd.DataFrame(columns=column_names)

    for address in common_addresses:
        balances = []
        for df in dfs:
            balance = df.loc[df.iloc[:, 0].astype(str) == address, 1].str.replace(',', '').astype(float).values
            if len(balance) > 0: 
                balances.append(balance[0])
            else:
                balances.append(0)

        if all(balance > threshold_balance for balance in balances):
            row_data = [address] + balances
            consolidated_df = pd.concat([consolidated_df, pd.DataFrame([row_data], columns=column_names)], ignore_index=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_path = f'{output_file}\\Crypto_Files_{timestamp}.xlsx'

    with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
        consolidated_df.to_excel(writer, sheet_name='Sheet1', index=False, header=True)

    return output_file_path