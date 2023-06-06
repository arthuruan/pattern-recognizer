import os
from PIL import Image

root_path = os.getcwd()

### transform all the images in grey scale if it's the first run
def convert_images_to_grayscale(directory, output_path):
    # Create the output folder if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    for folder in os.listdir(directory):
        path = os.path.join(directory, folder)
        if os.path.isdir(path):
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
######

def load_data():
    db_path = root_path + '/database/'
    grayscale_fold_name = 'grayscale'

    # verifying if grayscale exists
    if not os.path.exists(db_path + grayscale_fold_name):
        # convert origin images to grey scales
        convert_images_to_grayscale(directory=db_path + 'raw', output_path=db_path + grayscale_fold_name)

    return 'data'

def main():
    data = load_data()

    print(data)

main()