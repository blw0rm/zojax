### -*- coding: utf-8 -*- ####################################################

from django.utils import simplejson
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.generic.create_update import apply_extra_context
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings

from zojax.models import Document
from zojax.forms import DocumentForm, ShareForm
from zojax.utils import send_message


def index(request, template="index.html",
          queryset = Document.objects.all(), form_class = DocumentForm,
          extra_context=None):
    """Home page. Show list of user's files and process file upload."""

    form = form_class(request.POST or None, request.FILES or None)
    document = None

    if request.user.is_authenticated():
        # Show documents for owner. Anonymous users cant use system.
        documents = queryset.filter(user=request.user)

        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            form = form_class()

    else:
        documents = queryset.none()

    context = {
        "documents": documents,
        "form": form,
        "d": document,
    }
    apply_extra_context(extra_context or {}, context)
#    import ipdb; ipdb.set_trace()

    if request.POST:
        context["visible"] = True
        response = {
            "form":render_to_string("upload_form.html",
                                    context_instance=RequestContext(
                                                            request,
                                                            context)
                                    )
                    }
        if document is not None:
            response["document"] = render_to_string("document.html",
                                             context_instance=RequestContext(
                                                                    request,
                                                                    context)
                                                    )
        return HttpResponse('<textarea>%s</textarea>' % simplejson.dumps(
                                                                    response))

    if request.is_ajax():
        # For ajax request we need to send only parts of page.
        response = {
            "account": render_to_string("ajax/account_info.html",
                                        context_instance=RequestContext(
                                                                    request,
                                                                    context)
                                        ),
            "content": render_to_string("ajax/index_content.html",
                                        context_instance=RequestContext(
                                                                    request,
                                                                    context)
                                        ),
        }
        return HttpResponse(simplejson.dumps(response),
                            content_type="application/json; charset=utf-8")

    return TemplateResponse(request, template, context)

@login_required
def remove_document(request, object_id):
    """Remove document object by id when authorized user is owner"""

    document = get_object_or_404(Document, id=object_id, user=request.user)
    try:
        document.delete()
    except Exception:
        deleted = False
    else:
        deleted = True

    if request.is_ajax():
        # For ajax requests only json reponse will be showed
        return HttpResponse(simplejson.dumps(deleted),
                            content_type="application/json; charset=utf-8")
    else:
        # Otherwise redirecting user to index page
        return redirect("index")

@login_required
def share_document(request, object_id, template="share_form.html",
                   form_class = ShareForm,
                   extra_context=None):
    """Share document by id when with other people"""

    document = get_object_or_404(Document, id=object_id, user=request.user)

    form = form_class(request.POST or None, request.FILES or None)

    if form.is_valid():
        send_message(form.cleaned_data["email"],
                     "email/share.html","email/share_subject.txt",
                     sender=request.user,
                     extra_context={"document": document,
                                    "message": form.cleaned_data["message"]})

        return TemplateResponse(request, template, {"success": True,})

    context = {
        "form": form,
        "document": document
    }

    apply_extra_context(extra_context or {}, context)

    return TemplateResponse(request, template, context)


def view_document(request, object_id, template="document_view.html",
                   extra_context=None):
    """View document object by id: preview or download"""

    document = get_object_or_404(Document, id=object_id)


    context = {
        "d": document
    }

    apply_extra_context(extra_context or {}, context)

    return TemplateResponse(request, template, context)

@login_required
def auth_success(request, template="publicauth/popup.html",
                   extra_context=None):
    """View required for authentication processing.
        When user comes first time we need filling extra form
        and redirecting to LOGIN_REDIRECT_URL otherwise we have
        popup which should close itself.
    """

    if request.session.has_key("extra"):
        # Filling extra form finished. Need redirect.
        return redirect(getattr(settings, "LOGIN_REDIRECT_URL", "/"))
    context = {}
    apply_extra_context(extra_context or {}, context)

    return TemplateResponse(request, template, context)
