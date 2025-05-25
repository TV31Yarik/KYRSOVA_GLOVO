from django import forms

class CheckoutForm(forms.Form):
    delivery_name = forms.CharField(label='Ваше Ім’я', max_length=255)
    delivery_address = forms.CharField(label='Адреса доставки', widget=forms.Textarea)
    phone = forms.CharField(label='Номер телефону', max_length=20)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        if user:
            self.fields['delivery_name'].widget.attrs.update({
                'placeholder': user.first_name or 'Ім’я'
            })
            self.fields['phone'].widget.attrs.update({
                'placeholder': '+380 00 000 0000'
            })
            self.fields['delivery_address'].widget.attrs.update({
                'placeholder': 'Місто, вулиця, номер будинку, квартира'
            })