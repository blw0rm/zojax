### -*- coding: utf-8 -*- ####################################################

from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.mail.message import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def default_upload_to(instance, file_name):
    """Provide default uploads path"""

    app_label, model = ContentType.objects.get_for_model(instance).natural_key()

    return 'uploads/%s/%s/%s_%s' % (app_label, model,
                                    instance.pk or '0', file_name)


def send_message(to_email, body_template, subject_template,
                      from_email=settings.DEFAULT_FROM_EMAIL,
                      reply_to=None, sender=None, content_type="html",
                      extra_context=None):
    """ Send a message using a given body and subject templates for email.
    """

    if type(from_email) in (tuple, list):
        # Use the first email if list or tuple provided
        from_email = from_email[0].encode('utf-8')

    context = {
        'sender': sender,
    }

    headers = {'Reply-To': reply_to}

    context.update(extra_context or {})

    msg = EmailMessage(render_to_string(subject_template, context),
                       render_to_string(body_template, context),
                       from_email, # from
                       (to_email,), # to
                       headers=headers)
    msg.content_subtype = content_type  # Main content is now text/html

    msg.send()

def get_absolute_uri(relative_path, secure=False, short=False):
    """
    Build absolute URI from relative path.

    **short** - True when schema should be ommited;

    **secure** - True when URL is secure and uses https schema otherwise False;

    """
    current_site = Site.objects.get_current()
    if secure:
        prefix = "https"
    else:
        prefix = "http"

    if short:
        return "%s%s" % (current_site.domain, relative_path)

    return "%s://%s%s" % (prefix, current_site.domain, relative_path)