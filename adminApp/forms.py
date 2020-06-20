from django import forms

class loginForm(forms.Form):
    adminId = forms.CharField(widget=forms.TextInput(attrs={'class': 'textField', 'placeholder': 'Admin Id here'}), max_length= 20,
                              label = ' Admin Id here')
    passcode = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'textField', 'placeholder': 'passcode here'}),max_length=30)
