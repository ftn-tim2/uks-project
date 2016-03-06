from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class IssueType(models.Model):
    name = models.TextField()
    key = models.CharField(primary_key=True, unique=True, max_length=10)
    color = models.TextField()

    class Meta:
        permissions = (
            ("view_issuetype", "Can view the IssueType"),
        )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('uks:issuetype_edit', kwargs={'pk': self.pk})


class Priority(models.Model):
    name = models.TextField()
    key = models.CharField(primary_key=True, unique=True, max_length=10)

    class Meta:
        permissions = (
            ("view_priority", "Can view the Priority"),
        )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('uks:priority_edit', kwargs={'pk': self.pk})


class Status(models.Model):
    name = models.TextField()
    key = models.CharField(unique=True, primary_key=True, max_length=10)

    class Meta:
        permissions = (
            ("view_status", "Can view the Status"),
        )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('uks:status_edit', kwargs={'pk': self.pk})


class Project(models.Model):
    name = models.TextField()
    key = models.CharField(unique=True, primary_key=True, max_length=10)
    status = models.ForeignKey(Status)
    issueType = models.ForeignKey(IssueType)
    priority = models.ForeignKey(Priority)

    class Meta:
        permissions = (
            ("view_project", "Can view the Project"),
        )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('uks:project_edit', kwargs={'pk': self.pk})


class Milestone(models.Model):
    name = models.TextField()
    key = models.CharField(primary_key=True, unique=True, max_length=10)
    project = models.ForeignKey(Project)

    class Meta:
        permissions = (
            ("view_milestone", "Can view the Milestone"),
        )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('uks:milestone_edit', kwargs={'pk': self.pk})


# class PortalUser(User):
#     class Meta:
#         permissions = (
#             ("view_portaluser", "Can view the PortalUser"),
#         )

#     def __unicode__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse('uks:portaluser_edit', kwargs={'pk': self.pk})


class Issue(models.Model):
    project = models.ForeignKey(Project)
    title = models.TextField()
    description = models.TextField()
    attribute = models.ImageField()
    reporter = models.ForeignKey(User, related_name="reporter")
    assigned_to = models.ForeignKey(User)
    status = models.ForeignKey(Status)
    milestone = models.ForeignKey(Milestone)
    issueType = models.ForeignKey(IssueType)
    priority = models.ForeignKey(Priority)

    class Meta:
        permissions = (
            ("view_issue", "Can view the Issue"),
        )

    def __unicode__(self):
        return self.project

    def get_absolute_url(self):
        return reverse('uks:issue_edit', kwargs={'pk': self.pk})


class Comment(models.Model):
    message = models.TextField()
    dateTime = models.DateTimeField()
    author = models.ForeignKey(User)
    issue = models.ForeignKey(Issue)

    class Meta:
        permissions = (
            ("view_comment", "Can view the Comment"),
        )

    def __unicode__(self):
        return self.message

    def get_absolute_url(self):
        return reverse('uks:comment_edit', kwargs={'pk': self.pk})


class Commit(models.Model):
    hashcode = models.CharField(unique=True, max_length=10)
    message = models.TextField()
    description = models.TextField()
    project = models.ForeignKey(Project)
    issue = models.ManyToManyField(Issue)

    class Meta:
        permissions = (
            ("view_commit", "Can view the Commit"),
        )

    def __unicode__(self):
        return self.hashcode

    def get_absolute_url(self):
        return reverse('uks:commit_edit', kwargs={'pk': self.pk})


