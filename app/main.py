import os
import random
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
        iris_list = []
        for filename in os.listdir(subfolder):
            file_path = os.path.join(subfolder, filename)
            if os.path.isfile(file_path) and os.path.splitext(filename)[1].lower() in ('.png'):
                with open(file_path, 'rb') as image_file:
                    value = image_file.read()
                    item = Item(path=file_path, folder_name=folder, bin_value=value, type='idle')
                    iris_list.append(item)
        list.append(iris_list)
    return list

def load_data():
    db_path = root_path + '/database/'
    grayscale_path = db_path + 'grayscale'

    # verifying if grayscale exists
    if not os.path.exists(grayscale_path):
        # convert origin images to grey scales
        convert_images_to_grayscale(directory=db_path + 'raw', output_path=grayscale_path)

    grayscale_folders = get_folder_list(directory=grayscale_path)
    return read_images_in_folders(directory=grayscale_path, folder_list=grayscale_folders)

# CHOOSE ONE RANDOM IMAGE FROM EACH FOLDER TO BE VALIDATION DATA AND THE REST TO BE TRAINING DATA
def split_data(data):
    # [ 
    #     [ { folder_name, path, type, bin_value }, { folder_name, path, type, bin_value }, ... ] , 
    #     [ { ... }, { ... }, ... ] 
    # ]
    training_data = []
    validation_data = []
    n_files_in_folder = len(data[0])
    for idx, iris in enumerate(data):
        iris_training_data = []
        iris_validation_data = []
        random_number = random.randint(0, (n_files_in_folder - 1))
        # DEBUG
        # print('idx', idx)
        for index, item in enumerate(iris):
            if index == random_number or (index == (len(iris) - 1) and len(iris_validation_data) == 0):
                item.type = 'validation'
                iris_validation_data.append(item)
                # DEBUG 
                # print('validation', item.path, ' ' ,index) 
            else:
                item.type = 'training'
                iris_training_data.append(item)
                # DEBUG 
                # print('training', item.path, ' ' ,index)

        training_data.append(iris_training_data)
        validation_data.append(iris_validation_data)
    return training_data, validation_data

def main():
    # [ 
    #     [ { folder_name, path, type, bin_value }, { folder_name, path, type, bin_value }, ... ] ,     # each item is an iris's folder
    #     [ { ... }, { ... }, ... ] 
    # ]
    data = load_data() 
    training, validation = split_data(data)

    print('training', len(training), training)
    print('validation', len(validation), validation)

    ###### TODO: split the list array between training (N - 1) and validation (1) for each class (IRIS)
    print(data[0][0].folder_name)
    print(data[0][0].path)
    print(data[0][0].type)
    # print(data[0][0].bin_value)

main()