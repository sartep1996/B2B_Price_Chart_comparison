import pandas as pd
import PySimpleGUI as sg
from datetime import datetime

from backend import find_matching_addresses, configure_columns_layout
from layouts import *





sg.theme('DefaultNoMoreNagging')

window = sg.Window("B2B Price Table Comparison", main_layout)
selected_files = []

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
            
                if file_paths:
                    config_window = configure_columns_layout(file_path)

                    while True:
                        config_event, config_values = config_window.read()
                        
                        if config_event == sg.WINDOW_CLOSED or config_event == 'OK':
                                break

                        address_column = config_window.values.get('ADDRESS_COLUMN', default=1)
                        price_column = config_window.values.get('PRICE_COLUMN', default=2)
                        abbreviation = config_window.values.get('ABBREVIATION')
                
        
        selected_files.extend(file_paths)
        file_paths = [path.strip() for path in selected_files if path.strip()]
        window["SELECTED_FILES"].update(values=file_paths)

        config_window.close()


    elif event == "OUTPUT LOCATION":
        output_location = values['OUTPUT LOCATION']
        window['SELECTED_OUTPUT_LOCATION'].update(output_location)
    elif event == "DELETE_FILES":
        selected_files_to_delete = values["SELECTED_FILES"]
        selected_files = [file for file in selected_files if file not in selected_files_to_delete]
        window["SELECTED_FILES"].update(values=selected_files)

    elif event == "Compare and Save":
        try:
            threshold_balance = float(values["THRESHOLD"])
            output_file_path = find_matching_addresses(file_paths, output_location, threshold_balance)
            window["OUTPUT_PATH"].update(f"Matching addresses saved to {output_file_path}", visible=True)
        except Exception as e:
            sg.popup_error(f"Error: {str(e)}")

window.close()

