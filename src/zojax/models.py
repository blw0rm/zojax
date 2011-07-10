### -*- coding: utf-8 -*- ####################################################

#import urllib2

from django.db import models
from django.core.files.storage import default_storage
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from zojax.utils import default_upload_to


class Document(models.Model):
    """Document models provide file and its title."""
    title = models.CharField(verbose_name=_('Document title'),
                             max_length=250, blank=True, null=True)
    user = models.ForeignKey("auth.user", related_name="documents")
    file = models.FileField(verbose_name=_('File'),
                            upload_to=default_upload_to)
    pub_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    @property
    def preview_url(self):
        """Build url for file preview with Google Doc Viewer"""
        FILE_PREVIEW_URL = getattr(settings, "FILE_PREVIEW_URL", None)
        if FILE_PREVIEW_URL is not None:
            return FILE_PREVIEW_URL+self.file.url
        else:
            return self.file.url
        
        

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.title.strip() and self.file:
            self.title = self.file.name
        return super(Document, self).save(force_insert=force_insert,
                                          force_update=force_update,
                                          using=using)

    class Meta:
        ordering = ('title',)
        verbose_name = _("document")
        verbose_name_plural = _("documents")