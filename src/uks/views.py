from uks.models import Project
from uks.models import IssueType
from uks.models import Priority
from uks.models import Status
from uks.models import Milestone
from uks.models import Issue
from uks.models import Comment
from uks.models import Commit
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
import os
import json
from collections import namedtuple
import datetime
import subprocess
from django.utils import timezone




class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'key', 'git', 'user', 'description']


@permission_required('uks.view_project')
@login_required
def project_list(request, template_name='uks/project_list.html'):
    project = Project.objects.all()
    data = {'object_list': project}
    return render(request, template_name, data)

@permission_required('uks.view_project')
@login_required
def project_view(request, pk, template_name='uks/project_view.html'):
    project = get_object_or_404(Project, pk=pk)
    src = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(src, os.pardir))
    spath = os.path.abspath(os.path.join(path, os.pardir))
    dpath = os.path.abspath(os.path.join(spath, os.pardir))

#    os.mkdir(base+"\\"+project.key)
#    os.chdir(base+"\\"+project.key)
        

    os.chdir(dpath)
    git = project.git
    reversed = git[::-1]
    index = reversed.find('/')
    r1 = reversed[4:index]
    src_path = os.path.join(dpath,r1[::-1])

    if not os.path.exists(src_path):
        os.system('git clone '+project.git)
        os.chdir(src_path)
    else:
        os.chdir(src_path)
        os.system('git pull')

  
    os.system(os.path.join(src,'git-log2json.sh'))

    def _json_object_hook(d): 
       return namedtuple('X', d.keys())(*d.values())
    def json2obj(data): 
       return json.loads(data, object_hook=_json_object_hook)

    
    commits= []
    
    with open('log.json') as data_file:
        for line in data_file:    
            data = x = json2obj(line)
            commit = Commit()                
            commit.hashcode = data.commit
            commit.user = data.author
            date = datetime.datetime.strptime(data.date, '%Y-%m-%d %H:%M:%S')
            commit.dateTime = timezone.make_aware(date, timezone.get_current_timezone())
            commit.project = project
            commit.message = data.message.replace("-"," ")
            if not Commit.objects.filter(hashcode=data.commit).exists():
                commit.save()
            commit.hashcode = commit.hashcode[:10]    
            commits.append(commit)
    
    issuesDB = Issue.objects.all()
    issues = []
    
    for issue in issuesDB:
        if issue.project == project:
            issues.append(issue)
    
    os.chdir(path)

    return render(request, template_name, {'project': project, 'commits':commits, 'issues':issues})


@permission_required('uks.add_project')
@login_required
def project_create(request, template_name='uks/project_form.html'):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))
    return render(request, template_name, {'form': form, 'form_type': 'Create'})


@permission_required('uks.change_project')
@login_required
def project_update(request, pk, template_name='uks/project_form.html'):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('uks:project_list')
    return render(request, template_name, {'form': form, 'form_type': 'Update'})


@permission_required('uks.delete_project')
@login_required
def project_delete(request, pk, template_name='uks/project_confirm_delete.html'):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('uks:project_list')
    return render(request, template_name, {'object': project, 'form_type': 'Delete'})


class IssueTypeForm(ModelForm):
    class Meta:
        model = IssueType
        fields = ['name', 'key', 'marker', 'project']


@permission_required('uks.view_issuetype')
@login_required
def issuetype_list(request, template_name='uks/issuetype_list.html'):
    issuetype = IssueType.objects.all()
    data = {'object_list': issuetype}
    return render(request, template_name, data)


@permission_required('uks.add_issuetype')
@login_required
def issuetype_create(request, template_name='uks/issuetype_form.html'):
    form = IssueTypeForm(request.POST or None)
    if form.is_valid():
        issuetype = form.save(commit=False)
        issuetype.user = request.user
        issuetype.save()
        return redirect('uks:issuetype_list')
    return render(request, template_name, {'form': form, 'form_type': 'Create'})


@permission_required('uks.change_issuetype')
@login_required
def issuetype_update(request, pk, template_name='uks/issuetype_form.html'):
    issuetype = get_object_or_404(IssueType, pk=pk)
    form = IssueTypeForm(request.POST or None, instance=issuetype)
    if form.is_valid():
        form.save()
        return redirect('uks:issuetype_list')
    return render(request, template_name, {'form': form, 'form_type': 'Update'})


@permission_required('uks.delete_issuetype')
@login_required
def issuetype_delete(request, pk, template_name='uks/issuetype_confirm_delete.html'):
    issuetype = get_object_or_404(IssueType, pk=pk)
    if request.method == 'POST':
        issuetype.delete()
        return redirect('uks:issuetype_list')
    return render(request, template_name, {'object': issuetype, 'form_type': 'Delete'})


class PriorityForm(ModelForm):
    class Meta:
        model = Priority
        fields = ['name', 'key', 'marker', 'project']


@permission_required('uks.view_priority')
@login_required
def priority_list(request, template_name='uks/priority_list.html'):
    priority = Priority.objects.all()
    data = {'object_list': priority}
    return render(request, template_name, data)


@permission_required('uks.add_priority')
@login_required
def priority_create(request, template_name='uks/priority_form.html'):
    form = PriorityForm(request.POST or None)
    if form.is_valid():
        priority = form.save(commit=False)
        priority.user = request.user
        priority.save()
        return redirect('uks:priority_list')
    return render(request, template_name, {'form': form, 'form_type': 'Create'})


@permission_required('uks.change_priority')
@login_required
def priority_update(request, pk, template_name='uks/priority_form.html'):
    priority = get_object_or_404(Priority, pk=pk)
    form = PriorityForm(request.POST or None, instance=priority)
    if form.is_valid():
        form.save()
        return redirect('uks:priority_list')
    return render(request, template_name, {'form': form, 'form_type': 'Update'})


@permission_required('uks.delete_priority')
@login_required
def priority_delete(request, pk, template_name='uks/priority_confirm_delete.html'):
    priority = get_object_or_404(Priority, pk=pk)
    if request.method == 'POST':
        priority.delete()
        return redirect('uks:priority_list')
    return render(request, template_name, {'object': priority, 'form_type': 'Delete'})


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ['name', 'key', 'marker', 'project']


@permission_required('uks.view_status')
@login_required
def status_list(request, template_name='uks/status_list.html'):
    status = Status.objects.all()
    data = {'object_list': status}
    return render(request, template_name, data)


@permission_required('uks.add_status')
@login_required
def status_create(request, template_name='uks/status_form.html'):
    form = StatusForm(request.POST or None)
    if form.is_valid():
        status = form.save(commit=False)
        status.user = request.user
        status.save()
        return redirect('uks:status_list')
    return render(request, template_name, {'form': form, 'form_type': 'Create'})


@permission_required('uks.change_status')
@login_required
def status_update(request, pk, template_name='uks/status_form.html'):
    status = get_object_or_404(Status, pk=pk)
    form = StatusForm(request.POST or None, instance=status)
    if form.is_valid():
        form.save()
        return redirect('uks:status_list')
    return render(request, template_name, {'form': form, 'form_type': 'Update'})


@permission_required('uks.delete_status')
@login_required
def status_delete(request, pk, template_name='uks/status_confirm_delete.html'):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        status.delete()
        return redirect('uks:status_list')
    return render(request, template_name, {'object': status, 'form_type': 'Delete'})


class MilestoneForm(ModelForm):
    class Meta:
        model = Milestone
        fields = ['name', 'key', 'marker', 'project']


@permission_required('uks.view_milestone')
@login_required
def milestone_list(request, template_name='uks/milestone_list.html'):
    milestone = Milestone.objects.all()
    data = {'object_list': milestone}
    return render(request, template_name, data)


@permission_required('uks.add_milestone')
@login_required
def milestone_create(request, template_name='uks/milestone_form.html'):
    form = MilestoneForm(request.POST or None)
    if form.is_valid():
        milestone = form.save(commit=False)
        milestone.user = request.user
        milestone.save()
        return redirect('uks:milestone_list')
    return render(request, template_name, {'form': form, 'form_type': 'Create'})


@permission_required('uks.change_milestone')
@login_required
def milestone_update(request, pk, template_name='uks/milestone_form.html'):
    milestone = get_object_or_404(Milestone, pk=pk)
    form = MilestoneForm(request.POST or None, instance=milestone)
    if form.is_valid():
        form.save()
        return redirect('uks:milestone_list')
    return render(request, template_name, {'form': form, 'form_type': 'Update'})


@permission_required('uks.delete_milestone')
@login_required
def milestone_delete(request, pk, template_name='uks/milestone_confirm_delete.html'):
    milestone = get_object_or_404(Milestone, pk=pk)
    if request.method == 'POST':
        milestone.delete()
        return redirect('uks:milestone_list')
    return render(request, template_name, {'object': milestone, 'form_type': 'Delete'})


class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'attribute', 'project', 'reporter', 'assigned_to', 'status', 'milestone', 'issueType', 'priority']


@permission_required('uks.view_issue')
@login_required
def issue_list(request, template_name='uks/issue_list.html'):
    issue = Issue.objects.all()
    data = {'object_list': issue}
    return render(request, template_name, data)


@permission_required('uks.add_issue')
@login_required
def issue_create(request, template_name='uks/issue_form.html'):
    form = IssueForm(request.POST or None)
    if form.is_valid():
        issue = form.save(commit=False)
        issue.user = request.user
        issue.date = datetime.datetime.now()
        issue.save()
        return redirect('uks:issue_list')
    return render(request, template_name, {'form': form, 'form_type': 'Create'})


@permission_required('uks.change_issue')
@login_required
def issue_update(request, pk, template_name='uks/issue_form.html'):
    issue = get_object_or_404(Issue, pk=pk)
    form = IssueForm(request.POST or None, instance=issue)
    if form.is_valid():
        form.save()
        return redirect('uks:issue_list')
    return render(request, template_name, {'form': form, 'form_type': 'Update'})


@permission_required('uks.delete_issue')
@login_required
def issue_delete(request, pk, template_name='uks/issue_confirm_delete.html'):
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == 'POST':
        issue.delete()
        return redirect('uks:issue_list')
    return render(request, template_name, {'object': issue, 'form_type': 'Delete'})


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['message', 'dateTime', 'author', 'issue']


@permission_required('uks.view_comment')
@login_required
def comment_list(request, template_name='uks/comment_list.html'):
    comment = Comment.objects.all()
    data = {'object_list': comment}
    return render(request, template_name, data)


@permission_required('uks.add_comment')
@login_required
def comment_create(request, template_name='uks/comment_form.html'):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.save()
        return redirect('uks:comment_list')
    return render(request, template_name, {'form': form, 'form_type': 'Create'})


@permission_required('uks.change_comment')
@login_required
def comment_update(request, pk, template_name='uks/comment_form.html'):
    comment = get_object_or_404(Comment, pk=pk)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('uks:comment_list')
    return render(request, template_name, {'form': form, 'form_type': 'Update'})


@permission_required('uks.delete_comment')
@login_required
def comment_delete(request, pk, template_name='uks/comment_confirm_delete.html'):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('uks:comment_list')
    return render(request, template_name, {'object': comment, 'form_type': 'Delete'})


class CommitForm(ModelForm):
    class Meta:
        model = Commit
        fields = ['hashcode', 'message', 'user', 'project', 'issue']


@permission_required('uks.view_commit')
@login_required
def commit_list(request, template_name='uks/commit_list.html'):
    commit = Commit.objects.all()
    data = {'object_list': commit}
    return render(request, template_name, data)


@permission_required('uks.add_commit')
@login_required
def commit_create(request, template_name='uks/commit_form.html'):
    form = CommitForm(request.POST or None)
    if form.is_valid():
        commit = form.save(commit=False)
        commit.user = request.user
        commit.save()
        return redirect('uks:commit_list')
    return render(request, template_name, {'form': form, 'form_type': 'Create'})


@permission_required('uks.change_commit')
@login_required
def commit_update(request, pk, template_name='uks/commit_form.html'):
    commit = get_object_or_404(Commit, pk=pk)
    form = CommitForm(request.POST or None, instance=commit)
    if form.is_valid():
        form.save()
        return redirect('uks:commit_list')
    return render(request, template_name, {'form': form, 'form_type': 'Update'})


@permission_required('uks.delete_commit')
@login_required
def commit_delete(request, pk, template_name='uks/commit_confirm_delete.html'):
    commit = get_object_or_404(Commit, pk=pk)
    if request.method == 'POST':
        commit.delete()
        return redirect('uks:commit_list')
    return render(request, template_name, {'object': commit, 'form_type': 'Delete'})
