# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.utils.dateformat import format
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.utils.timezone import now
from django.core.files.base import ContentFile
from dfss.demo.models import Resume, UserProfile
from dfss.demo.forms import ResumeForm, UserForm, UserProfileForm


def build_filename(user_id, resume_id, epoch_time):
    return str(user_id + '/resume/resume@' + epoch_time)


@login_required
def get_resume(request, epoc_time=0):
    newdoc = Resume.objects.all().filter(user=request.user)
    if len(newdoc) > 0:
        resume = newdoc[0]
        split_name = resume.docfile.name.split("@")
        resume.docfile.name = split_name[0] + "@" + epoc_time
        print resume.docfile.name
        return HttpResponse(ContentFile(resume.docfile.read()), content_type='attachment')
    return HttpResponse({}, content_type='application/json')


@login_required
def resumes(request):
    # Handle file upload
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Resume.objects.all().filter(user=request.user)
            current_time = now()
            epoch_time = str(format(now(), 'U'))
            current_time = str(current_time)
            if len(newdoc) is 0:
                newdoc = Resume(user=request.user,
                                docfile=request.FILES['docfile'],
                                timestamp=epoch_time)

            else:
                newdoc = newdoc[0]
                newdoc.docfile = request.FILES['docfile']
                newdoc.latest_timestamp = current_time
                newdoc.timestamp = epoch_time + ',' + newdoc.timestamp
            newdoc.docfile.name = build_filename(
                str(request.user.id), str(newdoc.id), epoch_time)
            newdoc.save()
            # Redirect to the Resume resumes after POST
            return HttpResponseRedirect(reverse('dfss.demo.views.resumes'))
    else:
        form = ResumeForm()  # A empty, unbound form

    # Load Resumes for the resumes page
    Resumes = Resume.objects.all().filter(user=request.user)
    one_resume = None
    timestamps = []
    if len(Resumes) > 0:
        one_resume = Resumes[0]
        timestamps = one_resume.timestamp.split(',')
        for i in range(0, len(timestamps)):
            timestamps[i] = {'datetime': datetime.datetime.fromtimestamp(
                int(timestamps[i])), 'unixtime': timestamps[i]}
        one_resume.unix_timestamp = timestamps[0]['unixtime']
        timestamps = timestamps[1:]

    # Render resumes page with the Resumes and the form
    return render_to_response(
        'resumes.html',
        {'Resume': one_resume, 'timestamps': timestamps, 'form': form},
        context_instance=RequestContext(request)
    )


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration
    # succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity
            # problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the
            # UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was
            # successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
        'register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context)


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/demo/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your DFSS account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)

# Use the login_required() decorator to ensure only those logged in can
# access the view.


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/demo/')
