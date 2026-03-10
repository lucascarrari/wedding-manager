from django import forms
from .models import Expense, Guest


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = "__all__"

    def clean_value(self):
        value = self.cleaned_data["value"]

        if isinstance(value, str):
            value = value.replace(",", ".")

        return float(value)


class RSVPForm(forms.Form):
    name = forms.CharField(label="Seu nome", max_length=100)
    email = forms.EmailField(label="Seu e-mail", required=False)
    companions_count = forms.IntegerField(
        label="Quantas pessoas vão com você?",
        min_value=0,
        max_value=10,
        initial=0
    )

    companion_1 = forms.CharField(label="Nome do acompanhante 1", max_length=100, required=False)
    companion_2 = forms.CharField(label="Nome do acompanhante 2", max_length=100, required=False)
    companion_3 = forms.CharField(label="Nome do acompanhante 3", max_length=100, required=False)
    companion_4 = forms.CharField(label="Nome do acompanhante 4", max_length=100, required=False)
    companion_5 = forms.CharField(label="Nome do acompanhante 5", max_length=100, required=False)
    companion_6 = forms.CharField(label="Nome do acompanhante 6", max_length=100, required=False)
    companion_7 = forms.CharField(label="Nome do acompanhante 7", max_length=100, required=False)
    companion_8 = forms.CharField(label="Nome do acompanhante 8", max_length=100, required=False)
    companion_9 = forms.CharField(label="Nome do acompanhante 9", max_length=100, required=False)
    companion_10 = forms.CharField(label="Nome do acompanhante 10", max_length=100, required=False)


class GuestCreateForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = [
            "name",
            "email",
            "phone",
            "guest_type",
            "invited_by",
            "notes",
        ]
        labels = {
            "name": "Nome",
            "email": "E-mail",
            "phone": "Telefone",
            "guest_type": "Tipo",
            "invited_by": "Convidado por",
            "notes": "Observações",
        }
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class GuestEditForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = [
            "name",
            "email",
            "phone",
            "guest_type",
            "invited_by",
            "confirmed",
            "notes",
        ]
        labels = {
            "name": "Nome",
            "email": "E-mail",
            "phone": "Telefone",
            "guest_type": "Tipo",
            "invited_by": "Convidado por",
            "confirmed": "Confirmado",
            "notes": "Observações",
        }
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }