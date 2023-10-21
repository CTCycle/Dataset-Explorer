# [IMPORT PACKAGES AND SETTING WARNINGS]
#==============================================================================
import os
import sys
import pandas as pd
import PySimpleGUI as sg
import warnings
warnings.simplefilter(action='ignore', category = DeprecationWarning)
warnings.simplefilter(action='ignore', category = FutureWarning)   

# [IMPORT MODULES AND CLASSES]
#==============================================================================
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))       
from modules.components.data_classes import DataSetFinder
import modules.global_variables as GlobVar

# [DEFAULT FOLDER PATHS]
#==============================================================================
if getattr(sys, 'frozen', False):    
    initial_folder = os.path.dirname(sys.executable)
else:    
    initial_folder = os.path.dirname(os.path.realpath(__file__))

# [WINDOW THEME AND OPTIONS]
#==============================================================================
sg.theme('LightGrey1')
sg.set_options(font = ('Arial', 11), element_padding = (6, 6))

# [LAYOUT OF THE FILE SELECTION FRAME]
#==============================================================================
list_of_files = GlobVar.list_of_files
input_text = sg.Text('Input folder', font = ('Arial', 12), size = (10,1))
dd_text = sg.Text('List of files', font = ('Arial', 12), size = (10,1))
load_input = sg.Input(enable_events=True, key= '-LOADPATH-', size = (70,1))
load_browser = sg.FolderBrowse(initial_folder = initial_folder, key = '-INBROWSER-')
load_button = sg.Button('Load file', key = '-LOAD-', expand_x=True)
dropdown = sg.DropDown(list_of_files, size = (20, 1), key = '-DROPDOWN-', expand_x = True, enable_events=True)
path_frame = sg.Frame('Select folder path', layout = [[input_text, load_input, load_browser], [dd_text, dropdown]],
                                                      expand_x=True)

# [LAYOUT OF THE DATA PREPARATION FRAME]
#==============================================================================
clean_button = sg.Button('Cleaning data', expand_x=True, key = '-CLEAN-', disabled=True)
epoch_button = sg.Button('Convert epoch', expand_x=True, key = '-EPOCH-', disabled=True)
prep_frame = sg.Frame('Data preparation', layout = [[clean_button], [epoch_button]], expand_x=True)

# [LAYOUT OF MULTIOPS FRAME]
#==============================================================================
describe_button = sg.Button('Description report', key = '-DSCREP-', expand_x=True, disabled=True)
analysis_button = sg.Button('Data analysis', key = '-ANALYSIS-', expand_x=True, disabled=True)
button_frame = sg.Frame('Operations', layout = [[describe_button], [analysis_button]], expand_x=True)
                                               
# [LAYOUT OF FILE SAVING FRAME]
#==============================================================================
save_button = sg.Button('Save', key = '-SAVE-', disabled=True)
save_input = sg.Input(enable_events=True, key = '-SAVEPATH-', expand_x = True)
save_browse = sg.FolderBrowse(initial_folder = initial_folder)
save_frame = sg.Frame('Save file', layout = [[save_input, save_browse, save_button]], expand_x=True)

# [LAYOUT OF THE WINDOW]
#==============================================================================
main_layout = [[path_frame],
               [prep_frame, button_frame],
               [save_frame]]
              
# [WINDOW LOOP]
#==============================================================================
main_window = sg.Window('DataExplorer V1.0', main_layout, 
                        grab_anywhere = True, resizable=True, finalize = True)
while True:
    event, values = main_window.read()

    if event == sg.WIN_CLOSED:
        break  


    # [SELECT FILES USING DROPDOWN MENU]
    #==========================================================================
    if event == '-DROPDOWN-':
        target_file = values['-DROPDOWN-'] 
        folder_path = values['-LOADPATH-']     
        filepath = os.path.join(folder_path, target_file)                
        df = pd.read_csv(filepath, sep= ';', encoding='utf-8')
        GlobVar.dataframe_name = target_file.split('.')[0]   
        GlobVar.dataframe, GlobVar.clean_dataframe = df, df.copy()                
        main_window['-CLEAN-'].update(disabled = False)              
        main_window['-DSCREP-'].update(disabled = False)
        main_window['-EPOCH-'].update(disabled = False)
        main_window['-ANALYSIS-'].update(disabled = False)         
            

    if event == '-LOADPATH-':
        path = values['-LOADPATH-']
        dataset_inspector = DataSetFinder(path)
        list_of_files = dataset_inspector.target_files
        GlobVar.list_of_files = list_of_files
        main_window['-DROPDOWN-'].update(values = list_of_files)     
    
    # [GENERATE DESCRIPTION REPORT]
    #==========================================================================
    if event == '-DSCREP-':
        df = GlobVar.dataframe
        df_statistics = df.describe().T        
        num_missing = df.isna().sum()
        df_statistics['Number of missing values'] = num_missing
        GlobVar.dataframe_statistics = df_statistics

    # [CONVERT EPOCH DATA INTO DATETIME FORMAT]
    #==========================================================================
    if event == '-EPOCH-':
        clean_df = GlobVar.clean_dataframe
        epoch_cols = [col for col in clean_df.columns[clean_df.columns.str.contains('EPOCH|Epoch|epoch|Data|DATA|data')]]
        for col in epoch_cols:
            clean_df[col] = pd.to_datetime(clean_df[col], unit = 's', utc = True).dt.tz_localize(None)
        GlobVar.clean_dataframe = clean_df     

    # [SAVE FILE UPON PROCESSING]
    #==========================================================================
    if event == '-CLEAN-':
        import modules.data_cleaning
        del sys.modules['modules.data_cleaning'] 

    # [LAUNCH DATA DISTRIBUTION]
    #==========================================================================
    if event == '-ANALYSIS-':
        import modules.data_analyzer
        del sys.modules['modules.data_analyzer'] 

    # [LAUNCH CLEANING MODULE]
    #==========================================================================
    if event == '-SAVEPATH-':
        if values['-SAVEPATH-'] == '':
            main_window['-SAVE-'].update(disabled = True)
        else:
            main_window['-SAVE-'].update(disabled = False)   

    if event == '-SAVE-':
        df_name = GlobVar.dataframe_name
        savepath = values['-SAVEPATH-']
        clean_df = GlobVar.clean_dataframe
        df_statistics = GlobVar.dataframe_statistics
        file_loc = os.path.join(savepath, '{}_processed.csv'.format(df_name))    
        clean_df.to_csv(file_loc, index = False, sep = ';', encoding = 'utf-8')
        file_loc = os.path.join(savepath, '{}_statistics.csv'.format(df_name))    
        df_statistics.to_csv(file_loc, index = False, sep = ';', encoding = 'utf-8')


main_window.close()

