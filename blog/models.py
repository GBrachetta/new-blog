from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from .make_thumbnail import make_thumbnail


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="blog_photos/%Y/%m/%d/",
        blank=True,
        validators=[FileExtensionValidator(["jpeg", "jpg", "png"])],
    )

    def save(self, *args, **kwargs):
        if self.image:
            self.image = make_thumbnail(self.image, size=(800, 800))
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """URL"""

        return reverse("post-detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    body = models.TextField(max_length=300)
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-date_posted",)

    def __str__(self):
        return f"Comment by {self.user} on {self.date_posted}"
