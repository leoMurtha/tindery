from pathlib import Path
from PIL import Image

import os
import random
from scipy import ndarray

# image processing library
import skimage as sk
from skimage import transform
from skimage import util
from skimage import io


def random_rotation(image_array: ndarray):
    # pick a random degree of rotation between 25% on the left and 25% on the right
    random_degree = random.uniform(-25, 25)
    return sk.transform.rotate(image_array, random_degree)


def random_noise(image_array: ndarray):
    # add random noise to the image
    return sk.util.random_noise(image_array)


def horizontal_flip(image_array: ndarray):
    # horizontal flip doesn't need skimage, it's easy as flipping the image array of pixels !
    return image_array[:, ::-1]


# dictionary of the transformations we defined earlier
available_transformations = {
    'rotate': random_rotation,
    'noise': random_noise,
    'horizontal_flip': horizontal_flip
}


def check_image(image_path):
    try:
        im = Image.open(image_path)
        im.verify()  # I perform also verify, don't know if he sees other types o defects
        im.close()  # reopen is necessary in my case
        im = Image.open(image_path)
        im.transpose(Image.FLIP_LEFT_RIGHT)
        im.close()
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    images = list(Path('images').rglob('*.jpeg'))

    total = len(images)

    for i, image_path in enumerate(images):
        image_path = str(image_path)
        image_name, ext = image_path.split('.')
        current_image = Image.open(image_path)
        if check_image(image_path):
            current_image.save(image_path)
            # Overwrite image as JPEG
            current_image.close()

            current_image = sk.io.imread(image_path)

            for tranformation, func in available_transformations.items():
                if tranformation in image_name:
                    break
                sk.io.imsave('%s_%s.%s' %
                             (image_name, tranformation, ext), func(current_image))

        print('Processing image %d of %d.' % (i + 1, total))
