from io import BytesIO
from django.core.files import File
from PIL import Image


# def make_thumbnail(image, size=(600, 600)):
#     """
#     Uses PIL to generate thumbnail.
#     Checks for file type and converts it accordingly.
#     The image gallery can then use a lightweight thumbnail to
#     display the images and renders the full size image only when the
#     user clicks on the thumbnail, reducing loading time dramatically.
#     """

#     im = Image.open(image)
#     if im.format == "JPEG":
#         im.convert("RGB")
#         im.thumbnail(size)
#         thumb_io = BytesIO()
#         im.save(thumb_io, "JPEG", quality=85)
#         image = File(thumb_io, name=image.name)
#     else:
#         im.convert("RGBA")
#         im.thumbnail(size)
#         thumb_io = BytesIO()
#         im.save(thumb_io, "PNG", quality=85)
#         image = File(thumb_io, name=image.name)
#     return image


def make_thumbnail(image, size=(600, 600)):
    """
    Uses PIL to generate thumbnail.
    Checks for file type and converts it accordingly.
    The image gallery can then use a lightweight thumbnail to
    display the images and renders the full size image only when the
    user clicks on the thumbnail, reducing loading time dramatically.
    """

    with Image.open(image) as im:
        if im.format == "JPEG":
            exif = im._getexif()

            im.convert("RGB")
            im.thumbnail(size)
            thumb_io = BytesIO()
            orientation_key = 274
            if exif and orientation_key in exif:
                orientation = exif[orientation_key]
                rotate_values = {
                    3: Image.ROTATE_180,
                    6: Image.ROTATE_270,
                    8: Image.ROTATE_90,
                }

                if orientation in rotate_values:
                    im = im.transpose(rotate_values[orientation])
            im.save(thumb_io, "JPEG", quality=85)
            image = File(thumb_io, name=image.name)
        else:
            im.convert("RGBA")
            im.thumbnail(size)
            thumb_io = BytesIO()
            im.save(thumb_io, "PNG", quality=85)
            image = File(thumb_io, name=image.name)
        return image
