from django import forms
from django.forms import Textarea
from .models import Listings, Bid, Category

choices= Category.objects.all().values_list('field', 'field')

choice_list= []

for item in choices:
    choice_list.append(item)

class ListingsForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields=[
            "product_name",
            "image",
            "description",
            'category',
            "price"
        ]
        widgets = {
            
        }
        
        widgets={
            'category':forms.Select(choices= choice_list, attrs={'class': 'form-control', 'cols': 40}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']