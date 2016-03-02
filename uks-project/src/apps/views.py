from django.shortcuts import render, redirect, get_object_or_404


def home(request, template_name='index.html'):

    return render(request, template_name, {})