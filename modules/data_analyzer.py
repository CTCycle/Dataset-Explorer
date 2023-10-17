# [IMPORT PACKAGES AND SETTING WARNINGS]
#==============================================================================
import os
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import warnings
warnings.simplefilter(action='ignore', category = DeprecationWarning)
warnings.simplefilter(action='ignore', category = FutureWarning) 


# [IMPORT MODULES AND CLASSES]
#==============================================================================
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from modules.components.plot_classes import DistributionPlot
from modules.components.data_classes import MultiCorrelator
import modules.global_variables as GlobVar

# [DEFAULT FOLDER PATHS]
#==============================================================================
if getattr(sys, 'frozen', False):    
    initial_folder = os.path.dirname(os.path.dirname(sys.executable))
else:    
    initial_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# [WINDOW THEME AND OPTIONS]
#==============================================================================
sg.theme('LightGrey1')
sg.set_options(font = ('Arial', 11), element_padding = (10,10))

# [LAYOUT OF SAVEPATH FRAME]
#==============================================================================
folder_browse = sg.FolderBrowse(initial_folder = initial_folder, key = '-INBROWSER-')
plot_path_input = sg.Input(enable_events=True, key= '-PLOTPATH-', size = (30,1))
savepath_frame = sg.Frame('Select folder where to save figures', layout = [[folder_browse, plot_path_input]], expand_x=True)                                                                  

# [LAYOUT OF ROUTINE DISTRIBUTION ANALYSIS FRAME]
#==============================================================================
hist_button = sg.Button('Plot histograms', key = '-HISTOGRAMS-', expand_x=True, disabled=True)
CDF_button = sg.Button('Plot CDF curves', key = '-CDF-', expand_x=True, disabled=True)
boxplot_button = sg.Button('Plot boxplots', key = '-BOXPLOT-', expand_x=True, disabled=True)
plot_frame = sg.Frame('Analysis of data distribution', layout = [[hist_button],
                                                                 [CDF_button],
                                                                 [boxplot_button]], expand_x=True)

# [LAYOUT OF THE CORRELATION FRAME]
#==============================================================================
pearson = sg.Radio('Pearson', 'regressor', key = '-PEARSON-', default=True)
kendall = sg.Radio('Kendall', 'regressor', key = '-KENDALL-')
spearman = sg.Radio('Spearman', 'regressor', key = '-SPEARMAN-')
regression_button = sg.Button('Calculate correlations', key = '-REGRESSION-', expand_x=True, disabled=True)
corr_input_text = sg.Text('Filter threshold value', font = ('Arial', 10))
corr_input = sg.Input(key = '-THRESHOLD-', size = (10,1), expand_x = True, enable_events=True)
filter_button = sg.Button('Filter correlations', key = '-FILTER-', expand_x=True, disabled=True)
regression_frame = sg.Frame('Correlations between variables', layout = [[pearson, kendall, spearman],
                                                                        [regression_button],
                                                                        [corr_input_text, corr_input],
                                                                        [filter_button]], expand_x=True)
                                                                       
# [LAYOUT OF THE WINDOW]
#==============================================================================
canvas_draw = False
canvas = sg.Canvas(key='-CANVAS-', size=(500, 500), expand_x=True)
left_column = sg.Column(layout = [[savepath_frame], [plot_frame],[regression_frame]])
right_column = sg.Column(layout = [[canvas]])
progress_bar = sg.ProgressBar(100, orientation = 'horizontal', size = (50, 20), key = '-PBAR-', expand_x=True)
main_layout = [[left_column, sg.VSeparator(), right_column],
               [sg.HSeparator()],
               [progress_bar]]

              
# [WINDOW LOOP]
#==============================================================================
analysis_window = sg.Window('Data analysis', main_layout, 
                        grab_anywhere = True, resizable=True, finalize = True)
while True:
    event, values = analysis_window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-PLOTPATH-':
        if values['-PLOTPATH-'] != '':
            analysis_window['-HISTOGRAMS-'].update(disabled = False) 
            analysis_window['-CDF-'].update(disabled = False)              
            analysis_window['-BOXPLOT-'].update(disabled = False)
            analysis_window['-REGRESSION-'].update(disabled = False)
        else:
            analysis_window['-HISTOGRAMS-'].update(disabled = True) 
            analysis_window['-CDF-'].update(disabled = True)              
            analysis_window['-BOXPLOT-'].update(disabled = True)
            analysis_window['-REGRESSION-'].update(disabled = True)
        
        
    # [PLOT HISTOGRAMS FOR EACH DATAFRAME COLUMN]
    #==========================================================================
    if event == '-HISTOGRAMS-':
        df_clean = GlobVar.clean_dataframe
        df_name = GlobVar.dataframe_name         
        if canvas_draw == True:
            fig_canvas.get_tk_widget().pack_forget()
            canvas_draw = False
        plot_path = values['-PLOTPATH-']
        plotter = DistributionPlot()    
        figures = plotter.plot_histograms(df_clean, df_name, 'auto', plot_path, 600, progress_bar)
        fig_canvas = FigureCanvasTkAgg(figures, master = analysis_window['-CANVAS-'].TKCanvas)
        fig_canvas.draw()
        fig_canvas.get_tk_widget().pack(side='top', fill='none', expand=False)
        canvas_draw = True  

    # [PLOT CUMULATIVE DISTRIBUTION FUNCTION CURVES FOR EACH DATAFRAME COLUMN]
    #==========================================================================
    if event == '-CDF-':  
        df_clean = GlobVar.clean_dataframe
        df_name = GlobVar.dataframe_name      
        if canvas_draw == True:
            fig_canvas.get_tk_widget().pack_forget()
            canvas_draw = False
        plot_path = values['-PLOTPATH-']
        plotter = DistributionPlot()    
        figures = plotter.plot_CDF(df_clean, df_name, plot_path, 600)  
        fig_canvas = FigureCanvasTkAgg(figures, master = analysis_window['-CANVAS-'].TKCanvas)
        fig_canvas.draw()
        fig_canvas.get_tk_widget().pack(side='top', fill='none', expand=False)
        canvas_draw = True
           
    # [PLOT CUMULATIVE DISTRIBUTION FUNCTION CURVES FOR EACH DATAFRAME COLUMN]
    #==========================================================================
    if event == '-REGRESSION-':
        df_clean = GlobVar.clean_dataframe
        df_name = GlobVar.dataframe_name        
        plot_path = values['-PLOTPATH-']
        regressor = MultiCorrelator(df_clean)
        if canvas_draw == True:
            fig_canvas.get_tk_widget().pack_forget()
            canvas_draw = False        
        if values['-PEARSON-'] == True:
            df_correlations = regressor.Pearson_corr(2)
        elif values['-KENDALL-'] == True:
            df_correlations = regressor.Kendall_corr(2)
        elif values['-SPEARMAN-'] == True:
            df_correlations = regressor.Spearman_corr(2)

        GlobVar.dataframe_correlations = df_correlations
        figure = regressor.corr_heatmap(df_correlations, plot_path, 600, df_name)
        fig_canvas = FigureCanvasTkAgg(figure, master = analysis_window['-CANVAS-'].TKCanvas)
        fig_canvas.draw()
        fig_canvas.get_tk_widget().pack(side='top', fill='none', expand=False)
        canvas_draw = True

    # [PLOT CUMULATIVE DISTRIBUTION FUNCTION CURVES FOR EACH DATAFRAME COLUMN]
    #==========================================================================
    if event == '-FILTER-':
        threshold = float(values['-THRESHOLD-'])
        if 0 <= threshold <= 1:
            analysis_window['-FILTER-'].update(disabled = False)
        else:
            analysis_window['-FILTER-'].update(disabled = True)
        




analysis_window.close()


#     elif op_sel == 2:        
#         regressor = MultiCorrelator(df)
#         print('------------------------------------------------------------------------')
#         print('Calculation of correlation matrix')
#         print('------------------------------------------------------------------------')
#         print('Generating Pearson correlation matrix...')
#         print()
#         df_corr_P = regressor.Pearson_corr(df, 2)
#         print('Generating Kendall correlation matrix...')
#         print()
#         df_corr_K = regressor.Kendall_corr(df, 2)
#         print('Generating Spearman correlation matrix...')
#         print()
#         df_corr_S = regressor.Spearman_corr(df, 2)
#         print()
#         print('Filtering correlation values')
#         print()
#         while True:
#             try:
#                 corr_t = float(input('Select correlation value: '))
#             except:
#                 continue
#             break 
        
#         filtered_correlations = regressor.corr_filter(df_corr_P, corr_t) 
#         strong_pairs = regressor.strong_pairs
#         weak_pairs = regressor.weak_pairs
#         zero_pairs = regressor.zero_pairs        
#         print('------------------------------------------------------------------------')
#         print('Calculation of correlation matrix')
#         print('------------------------------------------------------------------------')
#         regressor.corr_heatmap(df_corr_K, plot_path, 800, 'clean_dataframe')
#         print()        
#         file_loc = os.path.join(save_path, 'Correlation_matrix_multiple.xlsx')
#         writer = pd.ExcelWriter(file_loc, engine = 'xlsxwriter')
#         df_corr_P.to_excel(writer, sheet_name='Pearson')
#         df_corr_K.to_excel(writer, sheet_name='Kendall')
#         df_corr_S.to_excel(writer, sheet_name='Spearman')
#         writer.save()

#         file_loc = os.path.join(save_path, 'Correlation_matrix_filter.xlsx')
#         writer = pd.ExcelWriter(file_loc, engine = 'xlsxwriter')
#         strong_pairs.to_excel(writer, sheet_name='Strong correlations')
#         weak_pairs.to_excel(writer, sheet_name='Weak correlations')
#         zero_pairs.to_excel(writer, sheet_name='Zero correlations')
#         writer.save()
      
        

#     # ...
#     #========================================================================== 
#     elif op_sel == 3:
#         pass
    
#     # ...
#     #========================================================================== 
#     elif op_sel == 4:
#         break
    


# # [SAVE FILES]
# #============================================================================== 
# # Saving dataframes into excel file 
# #==============================================================================  
# print('------------------------------------------------------------------------')
# print('Saving multiple dataframes as excel files')
# print('------------------------------------------------------------------------') 
# file_loc = os.path.join(save_path, 'Clean_dataframe.xlsx') 
# writer = pd.ExcelWriter(file_loc, engine = 'xlsxwriter')
# df.to_excel(writer, sheet_name='Clean_data')
# writer.save()
# print('File has been saved!')  
# print()

# # script end 
# #==============================================================================
# if __name__ == '__main__':
#     pass


