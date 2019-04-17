import os
import json

from PIL import Image

next_id = 1
image_list = {}

image_template = {
    'id': next_id,
    'file': 'origfilename_1.png',
    'img': Image.Image()
}


def get_as_json():
    def blank(obj):
        return 'unserializable'
    return json.dumps(
        {
            'next_id': next_id,
            'images': image_list
        },
        default=blank
    )


def restore_from_loaded_json(data):
    global next_id
    global image_list

    data = json.loads(data)
    next_id = data['next_id']
    image_list = data['images']
    image_list = {int(k): v for k, v in image_list.items()}


def clear():
    global next_id
    global image_list

    next_id = 1
    image_list = {}


def add_image(img, file):
    global next_id
    global image_list

    base = os.path.basename(file)
    base = os.path.splitext(base)[0]
    base = '{}_{}.png'.format(base, next_id)

    image_list[next_id] = {
        'id': next_id,
        'file': base,
        'img': img
    }
    next_id += 1
    return next_id - 1


def get_image(image_id):
    image_id = int(image_id)
    if type(image_id) is int:
        if image_id in image_list.keys():
            return image_list[image_id]['img']
        return None
    for k, img in image_list.items():
        if img['file'] == image_id:
            return img['img']
    return None


def remove_image(image_id):
    if image_id in image_list.keys():
        del image_list[image_id]
