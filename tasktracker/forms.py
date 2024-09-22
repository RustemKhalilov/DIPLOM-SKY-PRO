from django import forms
from .models import Task


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class TaskForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ('Executor', 'name', 'description', 'end_time', 'related_task', 'status')



