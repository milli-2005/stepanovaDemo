import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import CourseApplication, Profile, Review


class RegisterForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=6)
    password = forms.CharField(label='Пароль', min_length=8, widget=forms.PasswordInput)
    full_name = forms.CharField(label='ФИО', max_length=120)
    phone = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(
            attrs={
                'placeholder': '8(XXX)XXX-XX-XX',
                'inputmode': 'numeric',
                'autocomplete': 'tel',
                'data-phone-mask': 'true',
            }
        ),
    )
    email = forms.EmailField(label='Электронная почта')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.fullmatch(r'[A-Za-z0-9]{1,6}', username):
            raise ValidationError('Только латиница и цифры, максимум 6 символов.')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Такой логин уже занят.')
        return username

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name'].strip()
        if not re.fullmatch(r'[А-Яа-яЁё ]+', full_name):
            raise ValidationError('Используйте только кириллицу и пробелы.')
        return full_name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.fullmatch(r'8\(\d{3}\)\d{3}-\d{2}-\d{2}', phone):
            raise ValidationError('Формат: 8(XXX)XXX-XX-XX.')
        return phone

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
        )
        Profile.objects.create(
            user=user,
            full_name=self.cleaned_data['full_name'],
            phone=self.cleaned_data['phone'],
        )
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get('username')
        password = cleaned.get('password')
        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise ValidationError('Неверный логин или пароль.')
        return cleaned


class ApplicationForm(forms.ModelForm):
    start_date = forms.DateField(
        label='Желаемая дата начала',
        input_formats=['%d.%m.%Y'],
        widget=forms.TextInput(
            attrs={
                'placeholder': 'ДД.ММ.ГГГГ',
                'inputmode': 'numeric',
                'data-date-mask': 'true',
            }
        ),
    )

    class Meta:
        model = CourseApplication
        fields = ['course', 'start_date', 'payment_method']

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date < timezone.localdate():
            raise ValidationError('Нельзя выбрать прошедшую дату.')
        return start_date


class AdminApplicationForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        label='Пользователь',
        queryset=User.objects.select_related('profile').order_by('username'),
        empty_label='Выберите пользователя',
    )
    start_date = forms.DateField(
        label='Дата начала',
        input_formats=['%d.%m.%Y'],
        widget=forms.TextInput(
            attrs={
                'placeholder': 'ДД.ММ.ГГГГ',
                'inputmode': 'numeric',
                'data-date-mask': 'true',
            }
        ),
    )

    class Meta:
        model = CourseApplication
        fields = ['user', 'course', 'start_date', 'payment_method', 'status']

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date < timezone.localdate():
            raise ValidationError('Нельзя выбрать прошедшую дату.')
        return start_date


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Поделитесь впечатлениями о курсе'})}
