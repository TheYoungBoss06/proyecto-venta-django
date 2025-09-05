from django import forms

class ShippingForm(forms.Form):
    shipping_name = forms.CharField(label='Nombre Completo', max_length=255)
    shipping_address = forms.CharField(label='Dirección de Envío', widget=forms.Textarea)
    shipping_phone = forms.CharField(label='Número de Teléfono', max_length=20)
