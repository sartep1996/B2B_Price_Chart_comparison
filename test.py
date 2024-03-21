
file_variables = {'C:/Users/sarte/Downloads/BYTESexport-tokenholders-for-contract-0xa19f5264f7d7be11c451c093d8f92592820bea86.csv': {'address_column': '1', 'price_column': '2', 'abbreviation': 'PVZ1'}, 'C:/Users/sarte/Downloads/ALTURAexport-tokenholders-for-contract-0x8263CD1601FE73C066bf49cc09841f35348e3be0.csv': {'address_column': '1', 'price_column': '2', 'abbreviation': 'PVZ2'}}


raw_paths = [file_path_key for file_path_key in file_variables.keys()]
address_column = [file_path_value['address_column'] for file_path_value in file_variables.values()]
price_column = [file_path_value['price_column'] for file_path_value in file_variables.values()]
abbreviations = [file_path_value['abbreviation'] for file_path_value in file_variables.values()]


zip_data = zip(raw_paths, address_column, price_column, abbreviations)

file_paths = list(zip_data)

print(file_paths)