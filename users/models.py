from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from blog.make_thumbnail import make_thumbnail
from PIL import Image
from io import BytesIO
from django.core.files import File


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="default.jpg",
        upload_to="profile_pics/",
        validators=[FileExtensionValidator(["jpeg", "jpg", "png"])],
    )
    is_resized = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        if self.image and not self.is_resized:
            self.is_resized = True
            # self.image = make_thumbnail(self.image, size=(200, 200))
            self.image = make_new_thumbnail(self.image, size=(200, 200))
        super().save(*args, **kwargs)


def make_new_thumbnail(image, size=(600, 600)):
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
