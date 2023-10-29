import os
import PySimpleGUI as sg  

# set warnings
#------------------------------------------------------------------------------
import warnings
warnings.simplefilter(action='ignore', category = Warning)

# import modules and classes
#------------------------------------------------------------------------------   
from modules.components.data_classes import DataCleaning
import modules.global_variables as GlobVar

# set default folder path
#------------------------------------------------------------------------------ 
initial_folder = os.path.dirname(os.path.realpath(__file__))

# [WINDOW THEME AND OPTIONS]
#==============================================================================
sg.theme('LightGrey1')
sg.set_options(font = ('Arial', 11), element_padding = (10,10))

# [LAYOUT OF ROUTINE CLEANING OPERATIONS FRAME]
#==============================================================================
duplicates_button = sg.Button('Remove duplicated rows', key = '-DUPLICATES-', expand_x=True)
NaN_button = sg.Button('Remove all-NaN rows', key = '-NAN-', expand_x=True)
routine_frame = sg.Frame('Routine cleaning operations', layout = [[duplicates_button],
                                                                  [NaN_button]], expand_x=True)

# [LAYOUT OF THE REMOVE COLUMNS FRAME]
#==============================================================================
value_input_text = sg.Text('Insert value', size = (10,1), font = ('Arial', 10))
colrem_value_input = sg.Input(key = '-VALUECOL-', size = (8,1), expand_x = True, enable_events=True)
percentage_text = sg.Text('(%) of values', size = (10,1), font = ('Arial', 10))
percentage_input= sg.Input(key = '-PERCENTAGE-', size = (8,1), expand_x = True, enable_events=True)
colrem_button = sg.Button('Remove columns', key = '-COLREM-', disabled=True, expand_x=True)
advanced_frame = sg.Frame('Remove columns with high target frequency', layout = [[value_input_text, colrem_value_input],
                                                                                 [percentage_text, percentage_input],
                                                                                 [colrem_button]])

# [LAYOUT OF THE WINDOW]
#==============================================================================
main_layout = [[routine_frame],
               [advanced_frame]]
               
# [WINDOW LOOP]
#==============================================================================
cleaning_window = sg.Window('Data Cleaning', main_layout, 
                             grab_anywhere = True, resizable = True, finalize = True)

while True:
    event, values = cleaning_window.read()

    if event == sg.WIN_CLOSED:
        break     
         
        
    # [REMOVE DUPLICATED ROWS FROM DATASET]
    #==========================================================================
    if event == '-DUPLICATES-':  
        df_clean = GlobVar.clean_dataframe        
        df_clean.drop_duplicates(inplace=True)
        df_clean.reset_index(inplace=True, drop=True)
        GlobVar.clean_dataframe = df_clean

    # [REMOVE DUPLICATED ROWS FROM DATASET]
    #==========================================================================
    if event == '-NAN-': 
        df_clean = GlobVar.clean_dataframe            
        df_clean.dropna(inplace=True)
        df_clean.reset_index(inplace=True, drop=True)
        GlobVar.clean_dataframe = df_clean

    # [REFRESH AND RESET STATUS OF SELECTION]
    #==========================================================================
    if event == '-VALUECOL-':        
            if values['-PERCENTAGE-'].isdigit():
                percentage_value = int(percentage)
                if 1 <= percentage_value <= 100:
                    cleaning_window['-COLREM-'].update(disabled = False)
                else:
                    cleaning_window['-COLREM-'].update(disabled = True)
            else:
                cleaning_window['-COLREM-'].update(disabled = True)           
             
    # [REFRESH AND RESET STATUS OF SELECTION]
    #==========================================================================
    if event == '-PERCENTAGE-':
        percentage = values['-PERCENTAGE-']
        if percentage.isdigit():
            percentage_value = int(percentage)
            if 1 <= percentage_value <= 100:
                cleaning_window['-COLREM-'].update(disabled = False)
            else:
                cleaning_window['-COLREM-'].update(disabled = True)
        else:
            cleaning_window['-COLREM-'].update(disabled = True)       
            

    # [REFRESH AND RESET STATUS OF SELECTION]
    #==========================================================================
    if event == '-COLREM-':        
        reference_val = values['-VALUECOL-']
        percentage = int(values['-PERCENTAGE-'])
        df_clean = GlobVar.clean_dataframe 
        data_cleaning = DataCleaning()
        df_clean = data_cleaning.remove_columns_by_valfreq(df_clean, reference_val, percentage)
        GlobVar.clean_dataframe = df_clean
        target_columns = data_cleaning.target_columns
        columns_list = '\n'.join(target_columns)        
        popup_text = 'A total of {0} columns has been removed\n\nCheck the column list hereinafter\n\n{1}'.format(len(target_columns), columns_list)
        sg.popup(popup_text, title='Report window')
        
            

  

cleaning_window.close()


