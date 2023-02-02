# TBPS Project

## Project Structure
This repository is structured with the source (Python) files in the `src/` directory, the data files downloaded from Box should be stored in `data/` and any plots should be saved in `plots/`. The working directory should be the source directory, which will be the default if you are using Spyder. This means that to load data, you must first exit the source directory to access the data directory. This can be achieved with the following code

`df = pd.read_csv("../data/total_dataset.csv")`

The repository has at least one branch for each subgroup, although you are free to make as many branches as you need to use. You can do this from within GitHub desktop or on this site by clicking on the currently selected branch. Make sure when you are trying to push your commits that you are on a branch other than "main", as this will give an error. 

## KstarMuMu Example Notebook
There is an example Jupyter notebook that goes through the process of loading and fitting to set of toy data available on the blackboard page and the TBPS site. There is also an introductory video that goes through this notebook and breaks it down, that can be found in the "Introductory Lectures" folder on blackboard. To run the notebook locally, you can clone this repository using Github Desktop and opening the file `resources/starter_notebook.ipynb` in Jupyter Notebooks or in another IDE.

## Useful Links
[Link to Github Pages for TBPS Course](https://mesmith75.github.io/ic-teach-kstmumu-public/)

[Link to introductory video(s)](https://bb.imperial.ac.uk/webapps/blackboard/content/listContent.jsp?course_id=_33970_1&content_id=_2529407_1)

[Link to toy Jupyter notebook](https://github.com/TBPS-Team10/TBPS-Project/blob/main/resources/starter_notebook.ipynb)