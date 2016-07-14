from django.db.models import Q
from django.shortcuts import render

from uks.models import Issue
from uks.models import Project


def home(request, template_name='index.html'):
    print("actual user " + request.user.username)
    owned_projs = list(Project.objects.filter(Q(owner=request.user.id)))
    contributed_projs_db = Project.objects.exclude(owner=request.user.id)

    for proj in contributed_projs_db:
        for con_user in proj.contributors.all():
            if con_user.id == request.user.id:
                owned_projs.append(proj)

    return render(request, template_name,
                  {'projects': owned_projs,
                   'issues_assigned_to_me': Issue.objects.filter(
                       assigned_to_id=request.user.id),
                   'issues_create_by_me': Issue.objects.filter(reporter_id=request.user.id)
                   })
