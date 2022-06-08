"""Dataset utility functions."""

import uuid

import numpy as np
from beartype import beartype
from PIL import Image, ImageDraw


@beartype
def autocrop(image: np.ndarray) -> np.ndarray:
    """Automatically crop image to square based on the middle of the image.

    Args:
        image (np.ndarray): The image to crop.

    Returns:
        np.ndarray: The cropped image.
    """
    rows, cols = image.shape[0], image.shape[1]
    center = (rows // 2, cols // 2)
    length = min(rows, cols) // 2 - 1
    return image[
        center[0] - length:center[0] + length,
        center[1] - length:center[1] + length,
        :,
    ]


@beartype
def shape_to_mask(
    img_shape: tuple,
    points: list,
    shape_type: str = None,
) -> np.ndarray:
    """Create a mask from a set of points.

    Args:
        img_shape (tuple): The shape of the image.
        points (list): The points to create the mask from.
        shape_type (str): The type of shape to create (polygon).

    Returns:
        np.ndarray: The mask.
    """
    mask = np.zeros(img_shape[:2], dtype=np.uint8)
    mask = Image.fromarray(mask)
    draw = ImageDraw.Draw(mask)
    xy = [tuple(point) for point in points]

    if shape_type != 'polygon':
        raise NotImplementedError

    if len(xy) < 3:
        raise ValueError('Polygon shape expects 3+ points')
    draw.polygon(xy=xy, outline=1, fill=1)

    return np.array(mask, dtype=bool)


@beartype
def shapes_to_label(
    img_shape: tuple,
    shapes: list,
    label_map: dict,
) -> tuple:
    """Create a label mask array from a list of shapes.

    Args:
        img_shape (tuple): The shape of the image.
        shapes (list): The shapes to create the label mask from.
        label_map (dict): The label map to use.

    Returns:
        tuple: The label mask array and the label map.
    """
    arr = np.zeros(img_shape[:2], dtype=np.int32)
    ins = np.zeros_like(arr)
    instances = []
    for shape in shapes:
        points = shape['points']
        label = shape['label']
        group_id = shape.get('group_id')
        if group_id is None:
            group_id = uuid.uuid1()
        shape_type = shape.get('shape_type', None)

        instance = (label, group_id)

        if instance not in instances:
            instances.append(instance)
        ins_id = instances.index(instance) + 1
        cls_id = label_map[label]

        mask = shape_to_mask(img_shape[:2], points, shape_type)
        arr[mask] = cls_id
        ins[mask] = ins_id

    return arr, ins
