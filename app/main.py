import os
from PIL import Image

root_path = os.getcwd()

def get_folder_list(directory):
    folder_list = []
    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)):
            folder_list.append(item)
    return folder_list

### transform all the images in grey scale if it's the first run
def convert_images_to_grayscale(directory, output_path):
    # Create the output folder if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    folders = get_folder_list(directory)
    for folder in folders:
        path = os.path.join(directory, folder)
        # Get the list of image files in the current folder
        image_files = [file for file in os.listdir(path) if file.lower().endswith(('.png'))]
        # Create a subfolder in the output folder
        subfolder = os.path.join(output_path, folder)
        os.makedirs(subfolder, exist_ok=True)
        # Convert each image to grayscale and save in the subfolder
        for image_file in image_files:
            image_path = os.path.join(path, image_file)
            image = Image.open(image_path)
            grayscale_image = image.convert("L")
            grayscale_image.save(subfolder + '/' + image_file)

## TODO: rename this class
class Item:
    def __init__(self, path, folder_name, bin_value, type):
        self.path = path
        self.folder_name = folder_name
        self.bin_value = bin_value
        self.type = type # [idle, training, validation]

def read_images_in_folders(directory, folder_list):
    list = []
    for folder in folder_list:
        subfolder = os.path.join(directory, folder)
        for filename in os.listdir(subfolder):
            file_path = os.path.join(subfolder, filename)
            if os.path.isfile(file_path) and os.path.splitext(filename)[1].lower() in ('.png'):
                with open(file_path, 'rb') as image_file:
                    iris_list = []
                    value = image_file.read()
                    item = Item(path=file_path, folder_name=folder, bin_value=value, type='idle')
                    iris_list.append(item)
        list.append(iris_list)
    return list

def load_data():
    db_path = root_path + '/database/'
    grayscale_fold_name = 'grayscale'

    # verifying if grayscale exists
    if not os.path.exists(db_path + grayscale_fold_name):
        # convert origin images to grey scales
        convert_images_to_grayscale(directory=db_path + 'raw', output_path=db_path + grayscale_fold_name)

    grayscale_folders = get_folder_list(directory=db_path + grayscale_fold_name)

    return read_images_in_folders(directory=db_path + grayscale_fold_name, folder_list=grayscale_folders)

def main():
    list = load_data()

    ###### TODO: split the list array between training (N - 1) and validation (1) for each class (IRIS)
    print(list[0][0].folder_name)
    print(list[0][0].path)
    print(list[0][0].type)
    # print(list[0][0].bin_value)

main()