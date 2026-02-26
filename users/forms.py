from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms
from users.models import User, Basket


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control py-4', 'placeholder':'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control py-4', 'placeholder':'Введите фамилию'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control py-4', 'placeholder': 'Введите имя пользователя'}), required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control py-4', 'placeholder': 'Введите адрес эл. почты'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control py-4', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control py-4', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control py-4', 'placeholder':'Введите имя пользователя'}), required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control py-4', 'placeholder':'Введите пароль'}))
    email = forms.EmailField(widget=forms.EmailInput({'class':'form-control py-4', 'placeholder':'Введите email'}))

    class Meta:
        model = User
        fields = ('username', 'password')

class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'custom-file-input'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'image', 'username')