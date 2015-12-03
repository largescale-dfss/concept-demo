# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from dfss.demo.models import Resume
from dfss.demo.forms import ResumeForm


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Resume(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the Resume list after POST
            return HttpResponseRedirect(reverse('dfss.demo.views.list'))
    else:
        form = ResumeForm()  # A empty, unbound form

    # Load Resumes for the list page
    Resumes = Resume.objects.all()

    # Render list page with the Resumes and the form
    return render_to_response(
        'list.html',
        {'Resumes': Resumes, 'form': form},
        context_instance=RequestContext(request)
    )
