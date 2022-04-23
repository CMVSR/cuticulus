"""Global message module."""


def not_considered(iid: int):
    """Message for NA or non-considered images.

    Args:
        iid (int): Image ID.

    Returns:
        str: Message.
    """
    return str(
        'Image {0} is NA or not considered in this version.'.format(iid),
    )
