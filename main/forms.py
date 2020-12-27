from django import forms


class add_courier(forms.Form):
    name = forms.CharField(widget=forms.TextInput(), required="")
    phone = forms.CharField(widget=forms.TextInput(), required="")


class generate(forms.Form):
    client = forms.CharField(widget=forms.TextInput(), required="")
    addres = forms.CharField(widget=forms.TextInput(), required="")
    date_time = forms.DateTimeField(widget=forms.DateTimeInput(), required="")


class search(forms.Form):
    hash = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required="")
