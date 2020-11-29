import os
import uuid
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from blog.make_thumbnail import make_thumbnail


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

    # def save(self, *args, **kwargs):
    #     if self.image:
    #         self.image = make_thumbnail(self.image, size=(200, 200))
    #         image_name = self.image.name
    #         ext = image_name.split(".")[-1]
    #         filename = "%s.%s" % (uuid.uuid4(), ext)
    #         clean_name = os.path.join("", filename)
    #         self.image.name = clean_name
    #         super().save(*args, **kwargs)
    #     else:
    #         super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if self.image:
    #         self.image = make_thumbnail(self.image, size=(200, 200))
    #         super().save(*args, **kwargs)
    #     else:
    #         super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.image and not self.is_resized:
            self.is_resized = True
            self.image = make_thumbnail(self.image, size=(200, 200))
        super().save(*args, **kwargs)
