import os
from PIL import Image

root_path = os.getcwd()

# transform all the images in grey scale if it's the first run

def get_folder_list(directory):
    folder_list = []
    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)):
            folder_list.append(item)
    return folder_list

def load_data():
    db_path = root_path + '/database/'
    grey_scale_fold_name = 'grey_scale'

    # verifying if grey_scale exists
    if not os.path.exists(db_path + grey_scale_fold_name):
        # convert origin images to grey scales
        folders = get_folder_list(db_path + 'raw')
        for folder in folders:
            print(folder)
        print('false')

    return 'data'

def main():
    data = load_data()

    print(data)

main()