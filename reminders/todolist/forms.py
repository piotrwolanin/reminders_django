from . import models
from django.forms import ModelForm, Textarea


class ToDoItemModelForm(ModelForm):
    class Meta:
        model = models.ToDoItem
        fields = ["description", "priority"]
        widgets = {"description": Textarea(attrs={"rows": 2})}
        help_texts = {
            "description": "Maximum 200 characters.",
        }
