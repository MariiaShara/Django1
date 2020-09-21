from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django import forms
from authapp.models import ShopUser
from mainapp.models import ClothingCategory, Clothing


class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.help_text = ''


class AdminUserCreateForm(FormControlMixin, UserCreationForm):
    class Meta:
        model = ShopUser
        fields = (
            'username', 'first_name', 'last_name', 'is_superuser', 'is_staff',
            'email', 'password1', 'password2', 'avatar', 'age')

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("You're too young!")
        return data


class AdminUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = (
            'username', 'first_name', 'last_name', 'email',
            'password', 'is_active', 'is_superuser', 'is_staff', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("You're too young!")
        return data


class AdminClothingCategoryCreateForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = ClothingCategory
        fields = '__all__'


class AdminClothingEditForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Clothing
        fields = '__all__'


class AdminClothingEditForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Clothing
        fields = '__all__'