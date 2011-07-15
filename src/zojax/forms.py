### -*- coding: utf-8 -*- ####################################################

from django.contrib.auth.models import User
from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _

from annoying.functions import get_object_or_None
from annoying.decorators import autostrip
from publicauth.models import PublicID

from zojax.models import Document


class DocumentForm(forms.ModelForm):
    """ Document form used to upload files by user """

    class Meta:
        model = Document
        fields = ('title', 'file')


class ShareForm(forms.Form):
    """ Share form used for sharing documents via email"""
    email = forms.EmailField(label=_(u"Recipient email"))
    message = forms.CharField(widget=forms.Textarea,
                              required=False, label=_(u"Message"))



class ExtraForm(forms.Form):
    """ Extra form used for extra data requesting from user with OpenID, OAuth"""
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_object_or_None(User, email=email):
            raise forms.ValidationError(_(u'User with this email already exists.'))
        return email

    def save(self, request, identity, provider):
        user = User.objects.create(username=self.cleaned_data['email'],
                                   first_name=self.cleaned_data['first_name'],
                                   last_name=self.cleaned_data['last_name'],
                                   email=self.cleaned_data['email'])
        if settings.PUBLICAUTH_ACTIVATION_REQUIRED:
            user.is_active = False

        PublicID.objects.create(user=user, identity=identity,
                                provider=provider)
        return user

ExtraForm = autostrip(ExtraForm)