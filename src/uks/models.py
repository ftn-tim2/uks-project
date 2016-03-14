from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import json

SILVER = "default"
BLUE = "primary"
GREEN = "success"
LIGHT_BLUE = "info"
YELLOW = "warning"
RED = "danger"
MARKER_CHOICES = (
    (SILVER, 'silver'),
    (BLUE, 'blue'),
    (GREEN, 'green'),
    (LIGHT_BLUE, 'light blue'),
    (YELLOW, 'yellow'),
    (RED, 'red')
)

class Project(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(unique=True, max_length=10)
    git = models.CharField(max_length=100)
    user = models.ManyToManyField(to=User,null=False)
    description = models.TextField()

    class Meta:
        permissions = (
            ("view_project", "Can view the Project"),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('uks:project_edit', kwargs={'pk': self.pk})


class IssueType(models.Model):
    name = models.TextField()
    key = models.CharField(unique=True, max_length=10)
    marker = models.CharField(max_length=15, choices=MARKER_CHOICES, default=SILVER)
    project = models.ManyToManyField(to=Project, blank=True)

    class Meta:
        permissions = (
            ("view_issuetype", "Can view the IssueType"),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('uks:issuetype_edit', kwargs={'pk': self.pk})


class Priority(models.Model):
    name = models.TextField()
    key = models.CharField(unique=True, max_length=10)
    marker = models.CharField(max_length=15, choices=MARKER_CHOICES, default=SILVER)
    project = models.ManyToManyField(to=Project, blank=True)

    class Meta:
        permissions = (
            ("view_priority", "Can view the Priority"),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('uks:priority_edit', kwargs={'pk': self.pk})


class Status(models.Model):
    name = models.TextField()
    key = models.CharField(unique=True, max_length=10)
    marker = models.CharField(max_length=15, choices=MARKER_CHOICES, default=SILVER)
    project = models.ManyToManyField(to=Project, blank=True)

    class Meta:
        permissions = (
            ("view_status", "Can view the Status"),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('uks:status_edit', kwargs={'pk': self.pk})


class Milestone(models.Model):
    name = models.TextField()
    key = models.CharField(unique=True, max_length=10)
    marker = models.CharField(max_length=15, choices=MARKER_CHOICES, default=SILVER)
    project = models.ManyToManyField(to=Project, blank=True)

    class Meta:
        permissions = (
            ("view_milestone", "Can view the Milestone"),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('uks:milestone_edit', kwargs={'pk': self.pk})


class Issue(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    project = models.ForeignKey(to=Project, null=False)
    reporter = models.ForeignKey(to=User, null=False, related_name='reporter')
    assigned_to = models.ForeignKey(to=User, null=True, blank=True)
    status = models.ForeignKey(to=Status, null=False)
    milestone = models.ForeignKey(to=Milestone, null=True, blank=True)
    issueType = models.ForeignKey(to=IssueType, null=False, verbose_name='Issue type')
    priority = models.ForeignKey(to=Priority, null=True, blank=True)
    description = models.TextField()
    attribute = models.ImageField(blank=True, null=True)

    class Meta:
        permissions = (
            ("view_issue", "Can view the Issue"),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('uks:issue_edit', kwargs={'pk': self.pk})


class Comment(models.Model):
    message = models.TextField()
    dateTime = models.DateTimeField()
    author = models.ForeignKey(to=User, null=False)
    issue = models.ForeignKey(to=Issue, null=False)

    class Meta:
        permissions = (
            ("view_comment", "Can view the Comment"),
        )

    def __str__(self):
        return self.message

    def get_absolute_url(self):
        return reverse('uks:comment_edit', kwargs={'pk': self.pk})


class Commit(models.Model):
    hashcode = models.CharField(max_length=64,primary_key=True)
    message = models.TextField()
    dateTime = models.DateTimeField()
    project = models.ForeignKey(to=Project, null=False)
    issue = models.ManyToManyField(to=Issue, blank=True)
    user = models.TextField(null=False)
    
    class Meta:
        permissions = (
            ("view_commit", "Can view the Commit"),
        )

    def __str__(self):
        return self.hashcode

    def get_absolute_url(self):
        return reverse('uks:commit_edit', kwargs={'pk': self.pk})

    