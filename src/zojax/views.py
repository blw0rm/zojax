### -*- coding: utf-8 -*- ####################################################

from django.utils import simplejson
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic.create_update import apply_extra_context
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from zojax.models import Document
from zojax.forms import DocumentForm, ShareForm


def index(request, template="index.html", ajax_template="upload_form.html",
          queryset = Document.objects.all(), form_class = DocumentForm,
          extra_context=None):
    """Home page."""

    form = form_class(request.POST or None, request.FILES or None)

    if request.user.is_authenticated():
        # Show documents for owner. Anonymous users cant use system.
        documents = queryset.filter(user=request.user)
        document = None

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

    if request.is_ajax():
        return TemplateResponse(request, template, context)

    return TemplateResponse(request, template, context)

@login_required
def remove_document(request, object_id):
    """Remove document object by id when authorized user is owner.."""

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
    """Remove document object by id when authorized user is owner.."""

    document = get_object_or_404(Document, id=object_id, user=request.user)

    form = form_class(request.POST or None, request.FILES or None)

    if form.is_valid():
        pass
#        document = form.save(commit=False)
#        document.user = request.user
#        document.save()
#        form = form_class()
        return TemplateResponse(request, template, {"success": True,})

    context = {
        "form": form,
        "document": document
    }

    apply_extra_context(extra_context or {}, context)

    return TemplateResponse(request, template, context)

