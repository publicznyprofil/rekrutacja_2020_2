import os

from django.db import models


class Dataset(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField()

    class Meta:
        ordering = ['-id']

    def filename(self):
        return os.path.basename(self.file.name)
