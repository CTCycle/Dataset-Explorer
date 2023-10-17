import os
import numpy as np
from tqdm import tqdm
import PySimpleGUI as sg
import matplotlib.pyplot as plt


# define class for plotting data
#==============================================================================
#==============================================================================
#==============================================================================
class DistributionPlot:
    
    """ 
    DistributionPlot(self, dataframe)
    
    Plot dataseries using different types of charts (histograms, CDF). Generated pictures
    are saved in a designated folder by assigning the argument path to the functions.
    
    Keyword arguments:    
    
    dataframe (pd.dataframe): target dataframe
    
    Returns:
        
    None
        
    """    
    
    
    # histogram plotting
    #==========================================================================            
    def plot_histograms(self, dataframe, df_name, nbin, path, dpi, pbar):
        
        """ 
        plot_histograms(dataframe, nbin, path, dpi, norm)
        
        Plots the histogram of each column within the dataframe, if the column is 
        filled with numerical variables. The histograms are either plotted with 
        normalized frequency or absolute frequency in the y-axis. The pictures are
        saved in the designated folder in .jpeg format
        
        Keyword arguments:  
            
        dataframe (pd.dataframe): target dataframe   
        nbin (int):               number of bins in the histograms
        path (str):               folder path to save plots
        dpi (int):                value to set picture quality
        norm (int):               normalization parameter
                                  if norm = 1, the frequency is normalized based on the area;
                                  if norm = 0, the absolute frequency is used instead        
        
        Returns:
            
        None
        
        """ 
                  
        dataframe_numeric = dataframe.select_dtypes(include = np.number)        
        for id, col in enumerate(dataframe.columns): 
            values = dataframe_numeric[col].values
            fig, ax = plt.subplots()            
            plt.hist(values, bins = nbin, histtype = 'bar', 
                     align = 'mid', color = 'deepskyblue', 
                     edgecolor = 'black')               
            plt.title(col)
            plot_loc = os.path.join(path, '{}_histogram.jpeg'.format(col))
            plt.savefig(plot_loc, bbox_inches = 'tight', format ='jpeg', dpi = dpi)
            pbar.update(id + 1, max=dataframe.shape[1])

        plt.xlabel('Values')
        plt.ylabel('Frequency')            
        plt.tight_layout()            
        plot_loc = os.path.join(path, '{}_histograms.jpeg'.format(df_name))
        plt.savefig(plot_loc, bbox_inches = 'tight', format ='jpeg', dpi = dpi)

        return fig

            
            
    
    # CDF plotting
    #==========================================================================            
    def plot_CDF(self, dataframe, df_name, path, dpi):
        
        """ 
        plot_CDF(dataframe, path, dpi)
        
        Plots the cumulative distribution function (CDF) of each column 
        within the dataframe, if the column contains numerical variables. 
        The pictures are saved in the designated folder in .jpeg format
        
        Keyword arguments:
            
        dataframe (pd.dataframe): target dataframe   
        path (str):               folder path to save plots
        dpi (int):                value to set picture quality
        
        Returns:
            
        None
               
        """
        dataframe_numeric = dataframe.select_dtypes(include = np.number)        
        for col in tqdm(dataframe_numeric.columns):
            values = dataframe_numeric[col].values
            ry, rx = np.histogram(values, bins = 'auto')
            cumsum = np.cumsum(ry)
            norm_cumsum = [x/cumsum[-1] for x in cumsum]
            fig, ax = plt.subplots()
            plt.plot(rx[:-1], norm_cumsum, c = 'blue')
            plt.xlabel(col, fontsize = 8)
            plt.ylabel('Cumulative frequency', fontsize = 8) 
            plt.xticks(fontsize = 8)
            plt.yticks(fontsize = 8)
            plt.title('CDF of {}'.format(col))
            plot_loc = os.path.join(path, 'CDF_of_{}.jpeg'.format(col))
            plt.savefig(plot_loc, bbox_inches = 'tight', format ='jpeg', dpi = dpi)
        
        plt.xlabel('Values')
        plt.ylabel('Cumulative frequency')            
        plt.tight_layout()            
        plot_loc = os.path.join(path, '{}_histograms.jpeg'.format(df_name))
        plt.savefig(plot_loc, bbox_inches = 'tight', format ='jpeg', dpi = dpi)

        return fig