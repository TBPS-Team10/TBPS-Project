from pathlib import Path
from os import getcwd
from enum import Enum

#%%
try:
    project = Path(__file__).parent.parent
    data = project / 'data'
    plots = project / 'plots'
    code =  project / 'src'
    
except NameError:
    cwd = Path(getcwd())
    this_file = cwd / 'directories.py'
    
    if not this_file.exists():
        print("""
        ############################################################################
                                        WARNING
        You are using an interactive environment - Make sure your working directory
        is set to the source directory (C:/Path/To/TBPS-Project/src on Windows).

        If you are using Spyder, you must also set the "Run" button to obey the 
        current working directory. Do this by checking 

        Preferences -> Run -> Working Directory Settings -> The current working
        directory
        ############################################################################

        """)

    project = cwd.parent
    data = project / 'data'
    plots = project / 'plots'
    code = project / 'src'

if __name__ == "__main__":
    print('Project dir: ' + str(project))
    print('Data dir: ' + str(data))
    print('Plots dir: ' + str(plots))
    print('Source (code) dir: ' + str(code))