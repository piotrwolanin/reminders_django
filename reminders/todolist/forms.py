from . import models
from django.forms import ModelForm, Textarea


class CommonInfo(ModelForm):
    class Meta:
        abstract = True
        exclude = ["created", "modified", "completed"]
        widgets = {"description": Textarea(attrs={"rows": 5})}
        help_texts = {
            "description": "Maximum 200 characters.",
        }


class ToDoItemModelForm(CommonInfo):
    class Meta(CommonInfo.Meta):
        model = models.ToDoItem
