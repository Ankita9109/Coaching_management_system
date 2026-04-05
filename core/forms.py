from django import forms
from .models import Student,Course
import re


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ["name", "phone", "course"]

    def clean_name(self):
        name = self.cleaned_data["name"]

        if not name.replace(" ", "").isalpha():
            raise forms.ValidationError(
                "Name should contain only letters"
            )

        return name


    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if not re.fullmatch(r"\d{10}", phone):
            raise forms.ValidationError(
                "Phone number must be exactly 10 digits"
            )

        return phone
    
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'fee']