from django import forms
from shop.models import Product

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control mb-3 mt-1 validate',}), max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mt-1  validate',}), label="Password")
    
class ProductForm(forms.ModelForm):
    class Meta:
         model = Product
         fields = ['product_name', 'slug', 'description', 'price', 'image_1', 'image_2', 'image_3', 'image_4', 'stock',
                      'is_available', 'is_featured', 'category', 'sub_category']
        
    def __init__(self, *args, **kwargs):
        super(ProductForm,self).__init__(*args, **kwargs)
        for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'