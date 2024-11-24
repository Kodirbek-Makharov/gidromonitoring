from django import forms
from django.forms import ModelForm
from .models import Viloyat, Dalolatnoma, DalolatnomaRasm, Noqonuniy_holat_turi
import datetime

class DalolatnomaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            # if myField!='noqonuniy_holat_turi':# or True:
            self.fields[myField].widget.attrs['class'] = 'form-control'
        self.fields['korsatma_sana'].initial = datetime.datetime.today
        self.fields['amal_qilish_muddati'].initial = datetime.datetime.today() + datetime.timedelta(days=14)
        self.fields['huquqbuzar_stir'].widget.attrs['oninput'] = "this.value = this.value.replace(/\D+/g, '')"
        self.fields['huquqbuzar_stir'].widget.attrs['inputmode'] = "numeric"

    # noqonuniy_holat_turi = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Noqonuniy_holat_turi.objects.all())
    viloyat = forms.ModelChoiceField(widget=forms.Select(attrs={"class":"form-control"}),required=False, queryset=Viloyat.objects.all())
    # thumbnail = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control"}))
    # description = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder":"Product's description"}))
    # price = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Product's price"}))
    class Meta:
        model = Dalolatnoma
        exclude = ['inspektor', 'created_at', 'updated_at', 'bartaraf_etilganligi', 'bartaraf_etilganligi_hujjati', 
                   'bartaraf_etilganligi_hujjati_sana', 'bartaraf_etilganligi_sana']
        widgets = {
            'korsatma_sana':forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'type': 'datetime-local'}),
            'amal_qilish_muddati':forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }

# class DalolatnomaRasmForm(ModelForm):

#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     #     for myField in self.fields:
#     #         self.fields[myField].widget.attrs['class'] = 'form-control'

#     rasm = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control", "multiple":True}))
#     class Meta:
#         model = DalolatnomaRasm
#         fields = ['rasm']