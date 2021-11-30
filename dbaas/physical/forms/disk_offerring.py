from django import forms
from django.core.validators import MinValueValidator
from ..models import DiskOffering

class DiskOfferingForm(forms.ModelForm):

    size_gb = forms.FloatField(
        label='Size GB', validators=[MinValueValidator(0.1)]
    )

    class Meta:
        model = DiskOffering
        fields = ("name", "size_gb", "environments")

    def __init__(self, *args, **kwargs):
        super(DiskOfferingForm, self).__init__(*args, **kwargs)
        self.initial['size_gb'] = self.instance.size_gb()
