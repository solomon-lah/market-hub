from django import  forms
from django.utils.translation import ugettext_lazy as _
class initialRegistrationForm(forms.Form):
    form_owner = forms.CharField(widget=forms.HiddenInput(),initial='initialForm', label ='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'textField', 'placeholder': 'Email here'}),required=True)
    passcode = forms.CharField(widget=forms.PasswordInput(attrs={'class':'textField', 'placeholder': 'Password here'}),max_length=30,
                               min_length=5)
    confirm_Passcode = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'textField', 'placeholder': 'Confirm Password here'}),
                                       max_length=30,min_length=5)
    def clean_confirm_Passcode(self):
        data = self.cleaned_data['confirm_Passcode']
        password = self.cleaned_data['passcode']
        if data != password:
            raise forms.ValidationError(_('Password and Confirm Password Mismatched'))
class finalRegistrationForm(forms.Form):
    form_owner = forms.CharField(widget=forms.HiddenInput(), initial='finalForm', label='')
    email = forms.CharField(widget=forms.HiddenInput(),label='')
    passcode = forms.CharField(widget=forms.HiddenInput(),label='')
    surname = forms.CharField(widget=forms.TextInput(attrs={'class': 'textField', 'placeholder': 'Surname'}),
                               max_length=20,
                               min_length=3)
    firstname = forms.CharField(widget=forms.TextInput(attrs={'class': 'textField', 'placeholder': 'Firstname'}),
                              max_length=20,
                              min_length=3)
    Male = 'Male'
    Female = 'Female'
    Select = ''
    gender_choices =[
        (Select,'Select a gender'),
        (Male, 'Male'),
        (Female,'Female')
    ]
    gender = forms.ChoiceField(widget=forms.Select(attrs={'class': 'selectField'}),choices=gender_choices)
    phoneNumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'textField', 'placeholder': 'phone Number'}),
                              max_length=11,
                              min_length=11)
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'textField', 'placeholder': 'Address'}),
                              max_length=300)
    image = forms.FileField()
class loginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'textField', 'placeholder': 'Your Email here'}))
    passcode = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'textField', 'placeholder': 'Firstname'}),max_length=30)
class upLoadForm(forms.Form):
    itemName = forms.CharField(widget=forms.Textarea({'class':'textField','placeholder':'Item Name here'}),max_length=100,label='Item Name')
    itemPrice = forms.IntegerField(widget=forms.TextInput(attrs={'class':'textField','placeholder':'Item Price here'}),label='Item Price')
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'textArea','placeholder':'Item Description here'}))
    phone = 'Phone'
    phoneAccessories = 'Phone Accessories'
    laptop = 'Laptop'
    laptopAccessories = 'Phone Accessories'
    clothing = 'Clothing'
    foods = 'Foods'
    services = 'Services'
    others = 'Others'
    select = ''
    categoryChoices = [
        (select, 'Select a category'),
        (phone, 'Phone'),
        (phoneAccessories, 'Phone Accessories'),
        (laptop, 'Laptop'),
        (laptopAccessories, 'Laptop Accessories'),
        (clothing, 'Clothing'),
        (foods, 'Foods'),
        (services, 'Services'),
        (others, 'Others')
    ]
    category = forms.ChoiceField(widget=forms.Select(attrs={'class':'selectField'}),choices=categoryChoices)
    img_1 = forms.FileField(label='Image 1')
    img_2 = forms.FileField(label='Image 2')

class chatForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'messageTextField','placehoder':'Message here'}), max_length=3000)
    img = forms.FileField(label='Include Image (optional)', required= False)
class editForm (forms.Form):
    itemName = forms.CharField(widget=forms.Textarea({'class': 'textField', 'placeholder': 'Item Name here'}),
                               max_length=100, label='Item Name')
    itemPrice = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'textField', 'placeholder': 'Item Price here'}), label='Item Price')
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'textArea', 'placeholder': 'Item Description here'}))
class editProfileForm(forms.Form):
    surname = forms.CharField(widget=forms.TextInput(attrs={'class': 'textField', 'placeholder': 'Surname'}),
                              max_length=20,
                              min_length=3)
    firstname = forms.CharField(widget=forms.TextInput(attrs={'class': 'textField', 'placeholder': 'Firstname'}),
                                max_length=20,
                                min_length=3)
    phoneNumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'textField', 'placeholder': 'phone Number'}),
                                  max_length=11,
                                  min_length=11, label ='Phone Number')
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'textField', 'placeholder': 'Address'}),
                              max_length=300)

class changeProfilePicForm(forms.Form):
    img = forms.FileField(label = 'Change Profile Pics')
