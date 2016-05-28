from django.db.models import Q
from django.shortcuts import render

from uks.models import Issue
from uks.models import Project


def home(request, template_name='index.html'):
    print("actual user " + request.user.username)
    return render(request, template_name,
                  {'projects': Project.objects.filter(Q(owner=request.user.id) | Q(contributors=request.user.id)),
                   'issues_assigned_to_me': Issue.objects.filter(
                       assigned_to_id=request.user.id),
                   'issues_create_by_me': Issue.objects.filter(reporter_id=request.user.id)
                   })
