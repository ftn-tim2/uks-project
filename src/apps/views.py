from django.shortcuts import render, redirect, get_object_or_404
from uks.models import Project
from uks.models import Issue


def home(request, template_name='index.html'):
    print("actual user " + request.user.username)
    return render(request, template_name, {'projects': Project.objects.filter(user = request.user.id),
                                           'issues_assigned_to_me': Issue.objects.filter(assigned_to_id = request.user.id),
                                           'issues_create_by_me': Issue.objects.filter(reporter_id = request.user.id)
                                           })