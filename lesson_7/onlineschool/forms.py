from django import forms
from django.forms.widgets import TextInput

from .models import Category, Course, Schedule


class CategoryFormAdmin(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'})
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('slug',)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'color': TextInput(attrs={'type': 'color'}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('slug',)

        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'teachers': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'reviews': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        exclude = ('slug',)

        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'students': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': 'form-control'}),
        }
