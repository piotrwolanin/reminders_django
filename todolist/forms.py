from . import models
from django.forms import ModelForm, Textarea


class ToDoItemModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the colon from label name
        self.label_suffix = ""

    class Meta:
        model = models.ToDoItem
        fields = ["description", "priority"]
        widgets = {
            "description": Textarea(
                attrs={
                    "rows": 2,
                }
            ),
        }
        help_texts = {
            "description": "Maximum 200 characters.",
        }
