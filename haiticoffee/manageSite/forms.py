from django import forms

class ChangeProductForm(forms.Form):
    productName = forms.CharField(label='Product Name', max_length=250, required=True)
    productDescription = forms.CharField(label='Product Description', required=True)
    productPrice = forms.DecimalField(label='Product Price', max_digits=5, decimal_places=2, required=True)
    productCollection = forms.CharField(label='Product Collection', max_length=250)

class AddImageForm(forms.Form):
    newImage = forms.ImageField(label='image', required=False)

class CreateProductForm(forms.Form):
    productName = forms.CharField(label='Product Name', max_length=250, required=True)
    productDescription = forms.CharField(label='Product Description', required=True)
    productPrice = forms.DecimalField(label='Product Price', max_digits=5, decimal_places=2, required=True)
    productImage = forms.ImageField(label='image', required=False)
    productCollection = forms.CharField(label='Product Collection', max_length=250)

class CreateCollectionForm(forms.Form):
    collectionName = forms.CharField(label='Collection Name', max_length=250, required=True)
    collectionDescription = forms.CharField(label='Collection Description', max_length=500, required=True)

class UpdateOrderForm(forms.Form):
    status = forms.CharField(label="Order Status", max_length=250, required=True)