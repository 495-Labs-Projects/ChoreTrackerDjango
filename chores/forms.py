from django import forms
from chores.models import *

class ChildForm(forms.ModelForm):

    class Meta:
        model = Child
        fields = ["first_name", "last_name", "active"] 

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ["name", "points", "active"] 


class ChoreForm(forms.ModelForm):
    
    class Meta:
        model = Chore
        fields = ["child", "task", "due_on", "completed"] 
        widgets = {
            'due_on': forms.SelectDateWidget(),
        }
