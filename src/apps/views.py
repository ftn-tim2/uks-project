from django.shortcuts import render, redirect, get_object_or_404
from uks.models import Project


def home(request, template_name='index.html'):

    return render(request, template_name, {'projects': Project.objects.all()
                                           })