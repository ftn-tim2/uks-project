from django.contrib import admin
from uks.models import Project
from uks.models import IssueType
from uks.models import Priority
from uks.models import Status
from uks.models import Milestone
from uks.models import Issue
from uks.models import Comment
from uks.models import Commit
# Handle the signal sent by user_login
from registration.signals import user_registered
from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission


def user_registered_handler(sender, **kwargs):
    """signal intercept for user_registered"""
    request = kwargs['request']
    new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
    view_permissions = ['view_project', 'view_issuetype', 'view_priority', 'view_status', 'view_milestone', 'view_issue', 'view_comment', 'view_commit', ]
    for v_perm in view_permissions:
        permission = Permission.objects.get(codename=v_perm)
        if permission:
            new_user.user_permissions.add(permission)

user_registered.connect(user_registered_handler)
admin.site.register(Project)
admin.site.register(IssueType)
admin.site.register(Priority)
admin.site.register(Status)
admin.site.register(Milestone)
admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(Commit)
