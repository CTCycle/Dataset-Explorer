# Dataset-Explorer

## Project description
This is a simple python-based GUI application to clean data and briefly analyze distribution of variables in a dataset. The application makes use of different methods for plotting histograms and cumulative distribution functions (CDF) of each column in the dataframe, and for calculating the correlation matrix based on different methodologies such as Pearson, Kendall, and Spearman. The script also provides a way to filter the correlation coefficients based on a user-defined threshold, and generates plots and outputs that can be saved in designated folders. 

## How to use
Run the main python file (DataExplorer.py) and use the GUI to navigate the various options. 

### Main window
The main window is divided in 3 sections, in the upper part you can select an input folder (where you data is located) using the **Browse** button. All files in the folder will be available in the **List of files** dropdown menu. Once you have selected a file, the other buttons become functional. In the lower section, you can select the output folder where to save your data.

The main window provides different options for data cleaning and data analysis:

**Cleaning data:** launches a second window to perform data cleaning operations
**Convert epochs:** convert epoch data to datetime (finds epoch column by keyword in the column title)
**Description report:** generates a statistical descriptive report of the dataset
**Data analysis:** launches a second window to perform data analysis operations

### Data cleaning window

### Data analysis window

### Requirements
This application has been developed and tested using the following dependencies (Python 3.10.12):

- `distfit==1.6.11`
- `matplotlib==3.7.2`
- `numpy==1.25.2`
- `pandas==2.0.3`
- `seaborn==0.12.2`
- `PySimpleGUI==4.60.5`
- `tqdm==4.66.1`

These dependencies are specified in the provided `requirements.txt` file to ensure full compatibility with the application. 

## Graphic interface
Here you can find a snapshot of the program GUI. First, the main window:

![main_gui](https://github.com/CTCycle/Dataset-Explorer/assets/101833494/e619b8aa-a448-4558-9d00-385d58bbfe2e)

Then, the window to perform data cleaning operations:

![sec_gui](https://github.com/CTCycle/Dataset-Explorer/assets/101833494/cbe8ff9b-d289-4d2e-bfd5-ee590cf60971)

And finally, the GUI to navigate the various options for data analysis

![sec2_gui](https://github.com/CTCycle/Dataset-Explorer/assets/101833494/1277c18b-0371-4e20-9bff-9833d132615e)


