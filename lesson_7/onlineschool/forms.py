from django import forms
from django.forms.widgets import TextInput

from .models import Category, Course, Schedule, Teacher, Student


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
    teachers = forms.ModelMultipleChoiceField(
        queryset=Teacher.objects.prefetch_related('user'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Course
        exclude = ('slug',)

        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'reviews': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ScheduleForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.prefetch_related('user', 'wishlist'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Schedule
        exclude = ('slug',)

        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date', 'class': 'form-control'}),
        }


class ContactForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'class': 'form-control'}))
