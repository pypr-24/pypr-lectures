import pandas as pd

def read_data():
    '''
    Download and/or read data file.
    '''

    if file_exists_in_my_folder:
        cat_info = pd.read_csv('cats_uk_reference.csv')
    else:
        print('Downloading the file...')
        cat_info = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-01-31/cats_uk_reference.csv')

        # Save the file
        cat_info.to_csv('cats_uk_reference.csv')
    
    return cat_info
