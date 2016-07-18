import datetime
import json
import os
from collections import namedtuple

from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User

from uks.models import Project, IssueType, Priority, Status, Milestone, Issue, Comment, Commit


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'key', 'git', 'contributors', 'description']


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
    src_path = os.path.join(dpath, r1[::-1])

    if not os.path.exists(src_path):
        os.system('git clone ' + project.git)
        os.chdir(src_path)
    else:
        os.chdir(src_path)
        os.system('git pull')

    os.system(os.path.join(src, 'git-log2json.sh'))

    def _json_object_hook(d):
        return namedtuple('X', d.keys())(*d.values())

    def json2obj(data):
        return json.loads(data, object_hook=_json_object_hook)

    commits = []

    with open('log.json', mode='r', encoding='utf-8') as data_file:
        for line in data_file:
            data = x = json2obj(line)
            commit = Commit()
            commit.hashcode = data.commit
            commit.user = data.author.replace("<", " ")
            commit.user = commit.user.replace(">", " ")
            date = datetime.datetime.strptime(data.date, '%Y-%m-%d %H:%M:%S')
            commit.dateTime = timezone.make_aware(date, timezone.get_current_timezone())
            commit.project = project
            commit.message = data.message.replace("-", " ")
            if not Commit.objects.filter(hashcode=data.commit).exists():
                commit.save()
            commits.append(commit)

    issues = Issue.objects.filter(Q(project=project))
    
    openIssues = []
    closedIssues = []
    
    for issue in issues:
        if((issue.status.name == 'done') or (issue.status.name == 'closed')):
            closedIssues.append(issue)
        else:
            openIssues.append(issue)
   
    issueTypes = IssueType.objects.filter(Q(project=project))

    priorities = Priority.objects.filter(Q(project=project))

    milestones = Milestone.objects.filter(Q(project=project))

    statuses = Status.objects.filter(Q(project=project))

    is_owner = project.owner == request.user

    is_contributor = len(project.contributors.filter(pk=request.user.id)) > 0
    print("is_contributor: {0}, is_owner: {1}, project.owner: {2}", is_contributor, is_owner, project.owner)

    os.chdir(path)

    success_message = ""
    alert_message = ""
    if request.session.has_key('success_message'):
        success_message = request.session.get('success_message')
        del request.session['success_message']
    if request.session.has_key('alert_message'):
        alert_message = request.session.get('alert_message')
        del request.session['alert_message']

    return render(request, template_name, {'project': project, 'commits': commits, 'issues': openIssues, 'closedIssues':closedIssues,
                                           'issueTypes': issueTypes, 'priorities': priorities, 'milestones': milestones,
                                           'statuses': statuses, 'success_message': success_message,
                                           'alert_message': alert_message, 'is_contributor': is_contributor,
                                           'is_owner': is_owner})



@permission_required('uks.add_project')
@login_required
def project_create(request, template_name='uks/project_form.html'):
    def addInitialDataToProject(project):
        project.milestone_set.add(Milestone.objects.get(id=1))
        project.milestone_set.add(Milestone.objects.get(id=2))
        project.milestone_set.add(Milestone.objects.get(id=3))
        project.issuetype_set.add(IssueType.objects.get(id=1))
        project.issuetype_set.add(IssueType.objects.get(id=2))
        project.issuetype_set.add(IssueType.objects.get(id=3))
        project.issuetype_set.add(IssueType.objects.get(id=4))
        project.issuetype_set.add(IssueType.objects.get(id=5))
        project.status_set.add(Status.objects.get(id=1))
        project.status_set.add(Status.objects.get(id=2))
        project.status_set.add(Status.objects.get(id=3))
        project.status_set.add(Status.objects.get(id=4))
        project.priority_set.add(Priority.objects.get(id=1))
        project.priority_set.add(Priority.objects.get(id=2))
        project.priority_set.add(Priority.objects.get(id=3))


    form = ProjectForm(request.POST or None)
    form.fields['contributors'].queryset = User.objects.exclude(username=request.user)

    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        addInitialDataToProject(project)
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
        fields = ['name', 'key', 'marker']


@permission_required('uks.add_issuetype')
@login_required
def issuetype_create(request, project_id, template_name='uks/issuetype_form.html'):
    form = IssueTypeForm(request.POST or None)
    project = get_object_or_404(Project, pk=project_id)
    if form.is_valid():
        issuetype = form.save(commit=False)
        issuetype.user = request.user
        issuetype.save()
        issuetype.project.add(project)
        form.save_m2m()
        request.session['success_message'] = "Issue type successfully added to project."
        return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))
    return render(request, template_name, {'form': form, 'form_type': 'Create'})


@permission_required('uks.change_issuetype')
@login_required
def issuetype_update(request, project_id, issuetype_id, template_name='uks/issuetype_form.html'):
    issuetype = get_object_or_404(IssueType, pk=issuetype_id)
    project = get_object_or_404(Project, pk=project_id)
    form = IssueTypeForm(request.POST or None, instance=issuetype)
    if form.is_valid():
        form.save()
        request.session['success_message'] = "Issue type successfully updated."
        return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))
    return render(request, template_name, {'form': form, 'form_type': 'Update'})


@permission_required('uks.delete_issuetype')
@login_required
def issuetype_delete(request, project_id, issuetype_id, template_name='uks/issuetype_confirm_delete.html'):
    issuetype = get_object_or_404(IssueType, pk=issuetype_id)
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        issues = Issue.objects.filter(project_id=project.id, issueType_id=issuetype.id)
        if not issues:
            issuetype.project.remove(project)
            request.session[
                'success_message'] = "The issue type " + issuetype.name + " successfully deleted from the project."
            return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))
        else:
            request.session[
                'alert_message'] = "The issue type " + issuetype.name + " cannot be deleted from the project."
            return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))
    return render(request, template_name, {'object': issuetype, 'form_type': 'Delete'})


class PriorityForm(ModelForm):
    class Meta:
        model = Priority
        fields = ['name', 'key', 'marker']


@permission_required('uks.add_priority')
@login_required
def priority_create(request, project_id, template_name='uks/priority_form.html'):
    form = PriorityForm(request.POST or None)
    project = get_object_or_404(Project, pk=project_id)
    if form.is_valid():
        priority = form.save(commit=False)
        priority.user = request.user
        priority.save()
        priority.project.add(project)
        form.save_m2m()
        request.session['success_message'] = "Priority successfully added to project."
        return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))
    return render(request, template_name, {'form': form, 'form_type': 'Create'})


@permission_required('uks.change_priority')
@login_required
def priority_update(request, priority_id, project_id, template_name='uks/priority_form.html'):
    priority = get_object_or_404(Priority, pk=priority_id)
    project = get_object_or_404(Project, pk=project_id)
    form = PriorityForm(request.POST or None, instance=priority)
    if form.is_valid():
        form.save()
        request.session['success_message'] = "Priority successfully updated."
        return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))
    return render(request, template_name, {'form': form, 'form_type': 'Update'})


@permission_required('uks.delete_priority')
@login_required
def priority_delete(request, project_id, priority_id, template_name='uks/priority_confirm_delete.html'):
    priority = get_object_or_404(Priority, pk=priority_id)
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        issues = Issue.objects.filter(project_id=project.id, priority_id=priority.id)
        if not issues:
            priority.project.remove(project)
            request.session[
                'success_message'] = "The priority '" + priority.name + "' successfully deleted from the project."
            return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))
        else:
            request.session[
                'alert_message'] = "The priority '" + priority.name + "' cannot be deleted from the project."
            return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))
    return render(request, template_name, {'object': priority, 'form_type': 'Delete'})


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ['name', 'key', 'marker']


@permission_required('uks.add_status')
@login_required
def status_create(request, project_id, template_name='uks/status_form.html'):
    form = StatusForm(request.POST or None)
    project = get_object_or_404(Project, pk=project_id)
    if form.is_valid():
        status = form.save(commit=False)
        status.user = request.user
        status.save()
        status.project.add(project)
        form.save_m2m()
        request.session['success_message'] = "Status successfully added to project."
        return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))
    return render(request, template_name, {'form': form, 'form_type': 'Create'})


@permission_required('uks.change_status')
@login_required
def status_update(request, status_id, project_id, template_name='uks/status_form.html'):
    status = get_object_or_404(Status, pk=status_id)
    project = get_object_or_404(Project, pk=project_id)
    form = StatusForm(request.POST or None, instance=status)
    if form.is_valid():
        form.save()
        request.session['success_message'] = "Status successfully updated."
        return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))
    return render(request, template_name, {'form': form, 'form_type': 'Update'})


@permission_required('uks.delete_status')
@login_required
def status_delete(request, project_id, status_id, template_name='uks/status_confirm_delete.html'):
    status = get_object_or_404(Status, pk=status_id)
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        issues = Issue.objects.filter(project_id=project.id, status_id=status.id)
        if not issues:
            status.project.remove(project)
            request.session[
                'success_message'] = "The status '" + status.name + "' successfully deleted from the project."
            return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))
        else:
            request.session['alert_message'] = "The status '" + status.name + "' cannot be deleted from the project."
            return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))
    return render(request, template_name, {'object': status, 'form_type': 'Delete'})


class MilestoneForm(ModelForm):
    class Meta:
        model = Milestone
        fields = ['name', 'key', 'marker']


@permission_required('uks.add_milestone')
@login_required
def milestone_create(request, project_id, template_name='uks/milestone_form.html'):
    form = MilestoneForm(request.POST or None)
    project = get_object_or_404(Project, pk=project_id)
    if form.is_valid():
        milestone = form.save(commit=False)
        milestone.user = request.user
        milestone.save()
        milestone.project.add(project)
        form.save_m2m()
        request.session['success_message'] = "Milestone successfully added to project."
        return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))
    return render(request, template_name, {'form': form, 'form_type': 'Create'})


@permission_required('uks.change_milestone')
@login_required
def milestone_update(request, milestone_id, project_id, template_name='uks/milestone_form.html'):
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    project = get_object_or_404(Project, pk=project_id)
    form = MilestoneForm(request.POST or None, instance=milestone)
    if form.is_valid():
        form.save()
        request.session['success_message'] = "Milestone successfully updated."
        return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))
    return render(request, template_name, {'form': form, 'form_type': 'Update'})


@permission_required('uks.delete_milestone')
@login_required
def milestone_delete(request, project_id, milestone_id, template_name='uks/milestone_confirm_delete.html'):
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        issues = Issue.objects.filter(project_id=project.id, milestone_id=milestone.id)
        if not issues:
            milestone.project.remove(project)
            request.session[
                'success_message'] = "The milestone '" + milestone.name + "' successfully deleted from the project."
            return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))
        else:
            request.session[
                'alert_message'] = "The milestone '" + milestone.name + "' cannot be deleted from the project."
            return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))
    return render(request, template_name, {'object': milestone, 'form_type': 'Delete'})


class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'attribute', 'assigned_to', 'status', 'milestone',
                  'issueType', 'priority']


@permission_required('uks.view_issue')
@login_required
def issue_list(request, template_name='uks/issue_list.html'):
    issue = Issue.objects.all()
    data = {'object_list': issue}
    return render(request, template_name, data)

@permission_required('uks.view_issue')
@login_required
def issue_view(request, pk, template_name='uks/issue_view.html'):
    issue = get_object_or_404(Issue, pk=pk)
    form = IssueForm(request.POST or None, instance=issue)
    print(issue)

    comments = Comment.objects.filter(Q(issue=issue))

    return render(request, template_name, {'form': form, 'form_type': 'Update', 'comments': comments, 'issue': issue})


@permission_required('uks.add_issue')
@login_required
def issue_create(request, project_id, template_name='uks/issue_form.html'):
    form = IssueForm(request.POST or None)
    project = get_object_or_404(Project, pk=project_id)

    form.fields['assigned_to'].queryset = User.objects.filter(contributors=project)
    if form.is_valid():
        issue = form.save(commit=False)
        issue.reporter = request.user
        issue.date = datetime.datetime.now()
        issue.project = project
        issue.save()

        template_name = 'uks/project_view.html'
        return project_view(request, issue.project.id, template_name)
    else:
        return render(request, template_name,
                      {'form': form, 'form_type': 'Create'})


@permission_required('uks.change_issue')
@login_required
def issue_update(request, pk, template_name='uks/issue_form.html'):
    issue = get_object_or_404(Issue, pk=pk)
    form = IssueForm(request.POST or None, instance=issue)
    if form.is_valid():
        form.save()

        template_name = 'uks/project_view.html'
        return project_view(request, issue.project.id, template_name)
    else:
        return render(request, template_name, {'form': form, 'form_type': 'Update'})


@permission_required('uks.change_issue')
@login_required
def issue_status(request, pk, template_name='uks/issue_form.html'):
    issue = get_object_or_404(Issue, pk=pk)
    status = Status.objects.get(key='don')
    if status:
        issue.status = status
        issue.save()
        template_name = 'uks/project_view.html'
        return project_view(request, issue.project.id, template_name)
    return HttpResponseRedirect(reverse('uks:issue_view', kwargs={'pk': issue}))


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
        fields = ['message']


@permission_required('uks.view_comment')
@login_required
def comment_list(request, template_name='uks/comment_list.html'):
    comment = Comment.objects.all()
    data = {'object_list': comment}
    return render(request, template_name, data)


@permission_required('uks.add_comment')
@login_required
def comment_create(request, issue_id, template_name='uks/comment_form.html'):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.author = request.user
        now = datetime.datetime.now()
        comment.dateTime = now
        comment.issue = get_object_or_404(Issue, pk=issue_id)
        comment.save()
        return HttpResponseRedirect(reverse('uks:issue_view', kwargs={'pk': comment.issue.id}))
    else:
        return render(request, template_name, {'form': form, 'form_type': 'Create'})


@permission_required('uks.change_comment')
@login_required
def comment_update(request, pk, template_name='uks/comment_form.html'):
    comment = get_object_or_404(Comment, pk=pk)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        template_name = 'uks/issue_view.html'
        return issue_view(request, comment.issue.id, template_name)
    else:
        return render(request, template_name, {'form': form, 'form_type': 'Update'})


@permission_required('uks.delete_comment')
@login_required
def comment_delete(request, pk, template_name='uks/comment_confirm_delete.html'):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()
        return HttpResponseRedirect(reverse('uks:issue_view', kwargs={'pk': comment.issue.id}))
    else:
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


def link_commit(request, commit_id):
    commit1 = get_object_or_404(Commit, pk=commit_id)
    issues1 = Issue.objects.all()
    template_name = "uks/issue_list.html"
    return render(request, template_name, {'object_list': issues1, 'commit': commit1.hashcode})
    # return HttpResponseRedirect(reverse('uks:issue_list', kwargs={'object_list': issues1, 'commit': commit1.id}))

def link_ci(request, commit_id, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    commit = get_object_or_404(Commit, pk=commit_id)
    status = Status.objects.get(key='don')
    if status:
        issue.status = status
        commit.issue.add(issue)
        commit.save
        issue.save()
    return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': issue.project.id}))

def link_issue(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    commits = Commit.objects.filter(Q(assigned_to=issue.user))
    return HttpResponseRedirect(reverse('uks:commit_list', kwargs={'object_list': commits, 'issue': issue.id}))

def link_ic(request, commit_id, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    commit = get_object_or_404(Commit, pk=commit_id)
    status = Status.objects.get(key='don')
    if status:
        issue.status = status
        issue.commit = commit
        commit.save
        issue.save()
    return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': issue.project.id}))

def subscribe(request, pk):
    project = get_object_or_404(Project, pk=pk)
    user = request.user
    project.contributors.add(user)
    return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))


def unsubscribe(request, pk):
    project = get_object_or_404(Project, pk=pk)
    user = request.user
    project.contributors.remove(user)
    return HttpResponseRedirect(reverse('uks:project_view', kwargs={'pk': project.id}))
