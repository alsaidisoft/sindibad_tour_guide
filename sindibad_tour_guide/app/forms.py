from django import forms
from app.models import Countries,Cities,Categories,SubCategories,Users

class CountryForm(forms.ModelForm):
    class Meta:
        model=Countries
        fields=['name','description','profile','active','created_by','created_date','updated_by','updated_date']
        widgets = {
            'name': forms.TextInput(attrs={'class':'input-box'}),
            'description': forms.Textarea(attrs={'class':'input-box'}),
            'profile': forms.FileInput(attrs={'class':'input-box'}),
            }

class CityForm(forms.ModelForm):
   
    class Meta:
        model=Cities
        fields=['country','name','description','active','created_by','created_date','updated_by','updated_date']
        widgets = {
            'name': forms.TextInput(attrs={'class':'input-box'}),
            'description': forms.Textarea(attrs={'class':'input-box'}),
            }
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Categories
        fields=['name','description','icon','active','created_by','created_date','updated_by','updated_date']
        widgets = {
            'name': forms.TextInput(attrs={'class':'input-box'}),
            'description': forms.Textarea(attrs={'class':'input-box'}),
            'icon': forms.FileInput(attrs={'class':'input-box'}),
            }
        
class SubCatForm(forms.ModelForm):
    class Meta:
        model=SubCategories
        fields=['city','cat','name','description','sub_cat_image','phone','website','direction','active','created_by','created_date','updated_by','updated_date']
        widgets = {
            'name': forms.TextInput(attrs={'class':'input-box'}),
            'phone': forms.TextInput(attrs={'class':'input-box'}),
            'website': forms.TextInput(attrs={'class':'input-box'}),
            'direction': forms.TextInput(attrs={'class':'input-box'}),
            'description': forms.Textarea(attrs={'class':'input-box'}),
            'sub_cat_image': forms.FileInput(attrs={'class':'input-box'}),
            }
        
class UserForm(forms.ModelForm):
   
    class Meta:
        model=Users
        fields=['role','name','email','phone','username','password','active','created_by','created_date','updated_by','updated_date']
        widgets = {
            'name': forms.TextInput(attrs={'class':'input-box'}),
            'email': forms.TextInput(attrs={'class':'input-box'}),
            'phone': forms.TextInput(attrs={'class':'input-box'}),
            'username': forms.TextInput(attrs={'class':'input-box'}),
            'password': forms.PasswordInput(attrs={'class':'input-box'}),
            }

        