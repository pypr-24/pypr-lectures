import pandas as pd
import os

def read_data(filename):
    '''
    Download and/or read data file.
    '''

    if os.path.exists(filename):
        cat_info = pd.read_csv(filename)
    else:
        print('Downloading the file...')
        url = f'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-01-31/{filename}'
        cat_info = pd.read_csv(url)

        # Save the file
        cat_info.to_csv(filename)
    
    return cat_info
