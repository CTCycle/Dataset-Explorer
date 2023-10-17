import os
import numpy as np
from distfit import distfit
import random
from tqdm import tqdm
import matplotlib.pyplot as plt
import math
import seaborn as sns
    



# define the class for inspection of the input folder and generation of files list.
# The extension as argument allows identifying specific files (.csv, .xlsx, .pdf, etc)
# and making a list of those than can be called with the 'target_files' method
#==============================================================================
#==============================================================================
#==============================================================================
class DataSetFinder:
    
    """    
    A class to find, load and manipulate dataset files present in a given folder.
    If the folder is empty, prompts the user to add files in the designated path. 
     
    Methods:
        
    __init__(path):   initialize the class for the given directory path 
    dataset_loader(): allows for dataset selection
   
    """   
    def __init__(self, path):        
        self.path = path
        self.extensions = ('.csv', '.xlsx')
        os.chdir(path)
        self.all_files = os.listdir(path)
        self.target_files = [f for f in self.all_files if f.endswith(self.extensions)]   
        
        
        
# define class for cleaning dataframe (NaN zeroing and coluns removal)
#==============================================================================
#==============================================================================
#==============================================================================      
class DataCleaning:    
     
    """    
    Class that includes all functions for dataframe polishing and data preparation
    prior to analysis.
      
    Methods:
        
    header_cleaner(dataframe):                     console menu management 
    NaN_replacer(dataframe, mode):                 replacement of null values 
    columns_remover(dataframe, value, percentage): removal of columns based on value frequency
   
    """       
     
    
    # removal of columns with certain percentage of undesired values
    #==========================================================================
    def remove_columns_by_valfreq(self, dataframe, value, percentage, pbar):
        
        """ 
        columns_remover(dataframe, value, percentage)
        
        Removes columns from a dataset if a certain value has a frequency percentage
        equal or higher than the threshold value. 
                
        Keyword arguments:  
            
        dataframe (pd.dataframe):  target dataframe
        value (float):             target value within the dataframe
        percentage (float):        threshold percentage of the value frequency
        
        Returns: 
            
        dataframe (pd.dataframe): modified dataframe
        
        """               
        self.pre_num_cols = dataframe.shape[1]         
        self.titles_list = dataframe.columns
        self.thres_value = float(percentage/100)
        self.rows_count = dataframe.shape[0]
        self.target_columns = []
        for col, count in dataframe.apply(lambda col: (col == value).sum()).items():
            if count / self.rows_count >= (self.thres_value):
                self.target_columns.append(col)
            
            
                    
        dataframe = dataframe.drop(self.target_columns, axis = 1)
        self.post_num_cols = dataframe.shape[1]
                
        return dataframe
      

      
# define class for correlations calculations
#==============================================================================
#==============================================================================
#==============================================================================
class MultiCorrelator:
    
    """ 
    MultiCorrelator(dataframe)
    
    Calculates the correlation matrix of a given dataframe using specific methods.
    The internal functions retrieves correlations based on Pearson, Spearman and Kendall
    methods. This class is also used to plot the correlation heatmap and filter correlations
    from the original matrix based on given thresholds. Returns the correlation matrix
    
    Keyword arguments: 
        
    dataframe (pd.dataframe): target dataframe
    
    Returns:
        
    df_corr (pd.dataframe): correlation matrix in dataframe form
                
    """
    def __init__(self, dataframe):
        self.dataframe = dataframe
        
    # Spearman correlation calculation
    #==========================================================================
    def Spearman_corr(self, decimals):
        df_corr = self.dataframe.corr(method = 'spearman').round(decimals)
        return df_corr
    
    # Kendall correlation calculation
    #==========================================================================    
    def Kendall_corr(self, decimals):
        df_corr = self.dataframe.corr(method = 'kendall').round(decimals)
        return df_corr
    
    # Pearson correlation calculation
    #==========================================================================    
    def Pearson_corr(self, decimals):
        df_corr = self.dataframe.corr(method = 'pearson').round(decimals)
        return df_corr
    
    # plotting correlation heatmap using seaborn package
    #==========================================================================
    def corr_heatmap(self, matrix, path, dpi, name):
        
        """ 
        corr_heatmap(matrix, path, dpi, name)
        
        Plot the correlation heatmap using the seaborn package. The plot is saved 
        in .jpeg format in the folder that is specified through the path argument. 
        Output quality can be tuned with the dpi argument.
        
        Keyword arguments:    
            
        matrix (pd.dataframe): target correlation matrix
        path (str):            picture save path for the .jpeg file
        dpi (int):             value to set picture quality when saved (int)
        name (str):            name to be added in title and filename
        
        Returns:
            
        None
            
        """
        cmap = 'YlGnBu'
        fig, ax = plt.subplots()
        sns.heatmap(matrix, square = True, annot = False, 
                    mask = False, cmap = cmap, yticklabels = False, 
                    xticklabels = False)
        plt.title('{}_correlation_heatmap'.format(name))
        plt.tight_layout()
        plot_loc = os.path.join(path, '{}_correlation_heatmap.jpeg'.format(name))
        plt.savefig(plot_loc, bbox_inches='tight', format ='jpeg', dpi = dpi)

        return fig        
        
    
     
    # filtering of correlation pairs based on threshold value. Strong, weak and null
    # pairs are isolated and embedded into output lists
    #==========================================================================   
    def regression_filter(self, matrix, threshold): 
        
        """
        corr_filter(matrix, path, dpi)
        
        Generates filtered lists of correlation pairs, based on the given threshold.
        Weak correlations are those below the threshold, strong correlations are those
        above the value and zero correlations identifies all those correlation
        with coefficient equal to zero. Returns the strong, weak and zero pairs lists
        respectively.
        
        Keyword arguments:    
        matrix (pd.dataframe): target correlation matrix
        threshold (float):     threshold value to filter correlations coefficients
        
        Returns:
            
        strong_pairs (list): filtered strong pairs
        weak_pairs (list):   filtered weak pairs
        zero_pairs (list):   filtered zero pairs
                       
        """        
        corr_pairs = matrix.unstack()
        sorted_pairs = corr_pairs.sort_values(kind="quicksort")
        strong_pairs = sorted_pairs[(sorted_pairs) >= threshold]
        strong_pairs = strong_pairs.reset_index(level = [0,1])
        mask = (strong_pairs.level_0 != strong_pairs.level_1) 
        strong_pairs = strong_pairs[mask]
        
        weak_pairs = sorted_pairs[(sorted_pairs) >= -threshold]
        weak_pairs = weak_pairs.reset_index(level = [0,1])
        mask = (weak_pairs.level_0 != weak_pairs.level_1) 
        weak_pairs = weak_pairs[mask]
        
        zero_pairs = sorted_pairs[(sorted_pairs) == 0]
        zero_pairs = zero_pairs.reset_index(level = [0,1])
        mask = (zero_pairs.level_0 != zero_pairs.level_1) 
        zero_pairs = zero_pairs[mask]
        
        return strong_pairs, weak_pairs, zero_pairs
  