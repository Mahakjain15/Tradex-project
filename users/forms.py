from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password  = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        min_length=8,
        help_text='Minimum 8 characters.'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}),
        label='Confirm Password'
    )

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'placeholder': 'Last Name',  'class': 'form-control'}),
            'username':   forms.TextInput(attrs={'placeholder': 'Username',   'class': 'form-control'}),
            'email':      forms.EmailInput(attrs={'placeholder': 'Email',     'class': 'form-control'}),
            'bio':        forms.Textarea(attrs={'placeholder': 'Short bio (optional)', 'class': 'form-control', 'rows': 3}),
            'avatar':     forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get('password'), cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email address', 'class': 'form-control', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )


class PostCreateForm(forms.ModelForm):
    class Meta:
        model  = Post
        fields = ['text', 'image']
        widgets = {
            'text':  forms.Textarea(attrs={
                'placeholder': "What's on your mind?",
                'class': 'form-control',
                'rows': 4,
                'maxlength': 2000,
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'text':  'Post Content',
            'image': 'Attach Image (optional)',
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'bio', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'bio':        forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'avatar':     forms.FileInput(attrs={'class': 'form-control'}),
        }
