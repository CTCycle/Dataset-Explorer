# Dataset-Explorer

## Project description
This is a simple python-based GUI application to clean data and briefly analyze distribution of variables in a dataset. The application makes use of different methods for plotting histograms and cumulative distribution functions (CDF) of each column in the dataframe, and for calculating the correlation matrix based on different methodologies such as Pearson, Kendall, and Spearman correlation. The script also provides a way to filter the correlation coefficients based on a user-defined threshold, and generates plots and outputs that can be saved in designated folders. 

## How to use
Run the main python file (DATAEXP.py) and use the GUI to navigate the various options. In the main window you will find the **Browse** button, which allows to select the target folder where your files are stored. Then, all files in the folder will be available in the **List of files** dropdown menu. Once you have selected a specific file, the other buttons will become functional, since they are deactivated by default. At the bottom of the main GUi, you canm also select the output folder where to save your processed data. Different options for data cleaning and data analysis are provided:

**Cleaning data:** launches a second window to perform data cleaning operations

**Convert epochs:** convert epoch data to datetime (finds epoch column by keyword in the column title)

**Description report:** generates a statistical descriptive report of the dataset

**Data analysis:** launches a second window to perform data analysis operations

### Data cleaning window
Coming soon

### Data analysis window
Coming soon

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
Here you can find some snapshots of the program GUI. From first to last, you can see the main window, the data cleaning window and finally the data analsys window:

![main_gui](https://github.com/CTCycle/Dataset-Explorer/assets/101833494/e619b8aa-a448-4558-9d00-385d58bbfe2e)

![sec_gui](https://github.com/CTCycle/Dataset-Explorer/assets/101833494/cbe8ff9b-d289-4d2e-bfd5-ee590cf60971)

![sec2_gui](https://github.com/CTCycle/Dataset-Explorer/assets/101833494/1277c18b-0371-4e20-9bff-9833d132615e)

## License
This project is licensed under the terms of the MIT license. See the LICENSE file for details.