from betterforms.multiform import MultiModelForm
from django.forms import ModelForm, Form

from .models import Certificate, Bundle, Key


class BundleForm(ModelForm):
    class Meta:
        model = Bundle
        fields = ['bundle_file']


class KeyForm(ModelForm):
    class Meta:
        model = Key
        fields = ['key_file']


class CertificateForm(ModelForm):
    class Meta:
        model = Certificate
        fields = ['cert_name']


class CertificateMultiForm(MultiModelForm, Form):
    form_classes = {
        'Certificate': CertificateForm,
        'Key': KeyForm,
        'Bundle': BundleForm
    }

# class CertificateForm(ModelForm):
#     class Meta:
#         model = Certificate
#         fields = ['cert_name', 'bundle_upload', 'key_upload']
#
#     def __init__(self, *args, **kwargs):
#         super(CertificateForm, self).__init__(*args, **kwargs)
#         self.fields['bundle_upload'].required = False
#         self.fields['key_upload'].required = False
#         data = kwargs.get('data')
#         self.bundle_form = BundleForm(instance=self.instance and self.instance.bundle_upload, prefix=self.prefix, data=data)
#         self.key_form = KeyForm(instance=self.instance and self.instance.key_upload, prefix=self.prefix, data=data)
#
#     def clean(self):
#         if not self.bundle_form.is_valid():
#             raise ValidationError('Bundle file not valid')
#         if not self.key_form.is_valid():
#             raise ValidationError('Key file is not valid')
#
#     def save(self, commit=True):
#         obj = super(CertificateForm, self).save(commit=commit)
#         obj.bundle_upload = self.bundle_form.save()
#         obj.key_upload = self.key_form.save()
#         obj.save()
