import PySimpleGUI as sg
import pandas as pd

main_layout = [
    [sg.Text("Select CSV files for B2B Price Table Comparison:")],
    # [sg.Input(key="FILES", enable_events=True, visible=False), sg.FilesBrowse("Browse for Files")],
    [sg.Button('Browse For File')],
    [sg.Listbox(values=[], size=(70, 5), key="SELECTED_FILES", select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED, enable_events=True)],
    [sg.Button("Delete Selected Files", key="DELETE_FILES")],
    [sg.Text("Threshold Balance:"), sg.InputText(default_text="10000", key="THRESHOLD")],
    [sg.Text("Output Location:"), sg.Multiline("", key="SELECTED_OUTPUT_LOCATION", size=(50, 1), disabled=True)],
    [sg.Input(key="OUTPUT LOCATION", enable_events=True, visible=False), sg.FolderBrowse("Browse for Output Location")],
    [sg.Button("Compare and Save")],
    [sg.Text("", size=(40, 1), key="OUTPUT_PATH", visible=False)]
]

