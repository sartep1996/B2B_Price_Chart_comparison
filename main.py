import pandas as pd
import PySimpleGUI as sg
from datetime import datetime

from backend import find_matching_addresses, configure_columns_layout
from layouts import *





sg.theme('DefaultNoMoreNagging')

window = sg.Window("B2B Price Table Comparison", main_layout)
selected_files = []
file_variables = {}


while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    # elif event == "FILES":
    #     file_paths = values["FILES"].split(';')
    #     selected_files.extend(file_paths)
    #     file_paths = [path.strip() for path in selected_files if path.strip()]
    #     window["SELECTED_FILES"].update(values=file_paths)
    
    elif event == 'Browse For File':
        file_paths = sg.PopupGetFile("Select File")

        if file_paths:

            file_paths = file_paths.split(';')

            for file_path in file_paths:
            
                if file_path:
                    config_window = configure_columns_layout(file_path)

                    while True:
                        config_event, config_values = config_window.read()
                        
                        if config_event == sg.WINDOW_CLOSED or config_event == 'OK':
                                break
                        
                        
                    address_column = config_values['ADDRESS_COLUMN']
                    price_column = config_values['PRICE_COLUMN']
                    abbreviation = config_values['ABBREVIATION']

        
                    file_variables[file_path] = {'address_column': address_column, 'price_column': price_column, 'abbreviation': abbreviation}
                
            print(file_variables)
        
        selected_files.extend(file_paths)
        file_paths = [path.strip() for path in selected_files if path.strip()]
        window["SELECTED_FILES"].update(values=file_paths)

        config_window.close()


    elif event == "OUTPUT LOCATION":
        output_location = values['OUTPUT LOCATION']
        window['SELECTED_OUTPUT_LOCATION'].update(output_location)
        print(output_location)
    elif event == "DELETE_FILES":
        selected_files_to_delete = values["SELECTED_FILES"]
        selected_files = [file for file in selected_files if file not in selected_files_to_delete]
        window["SELECTED_FILES"].update(values=selected_files)

    elif event == "Compare and Save":
        print(output_location)
        try:
            threshold_balance = float(values["THRESHOLD"])
            output_file_path = find_matching_addresses(file_variables, output_location, threshold_balance)
            window["OUTPUT_PATH"].update(f"Matching addresses saved to {output_file_path}", visible=True)
            sg.popup('Success!')
        except Exception as e:
            sg.popup_error(f"Error: {str(e)}")
            print(f"Error: {str(e)}")
            print(type(threshold_balance))

window.close()

