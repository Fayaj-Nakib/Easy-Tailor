from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'address', 'shop_name', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Text inputs
        text_fields = [
            ('username', 'Choose a username'),
            ('email', 'Email address'),
            ('first_name', 'First name'),
            ('last_name', 'Last name'),
            ('phone', 'Phone number'),
            ('shop_name', 'Shop name (optional)'),
        ]
        for name, placeholder in text_fields:
            if name in self.fields:
                self.fields[name].widget.attrs.update({'class': 'form-control', 'placeholder': placeholder})
        # Address as textarea for nicer placeholder and rows
        if 'address' in self.fields:
            self.fields['address'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'})
        # Role as select
        if 'role' in self.fields:
            self.fields['role'].widget.attrs.update({'class': 'form-select'})
        # Passwords
        for name, placeholder in [('password1', 'Create password'), ('password2', 'Confirm password')]:
            if name in self.fields:
                self.fields[name].widget.attrs.update({'class': 'form-control', 'placeholder': placeholder})

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'shop_name', 'default_regular_size', 'default_custom_measurements']
