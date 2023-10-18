from django.db import models


class ToDoItem(models.Model):
    description = models.TextField("description", max_length=200)
    created = models.DateTimeField("created", auto_now_add=True)
    modified = models.DateTimeField("modified", auto_now=True)
    priority = models.BooleanField("priority", default=False)
    completed = models.BooleanField("completed", default=False)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.description
