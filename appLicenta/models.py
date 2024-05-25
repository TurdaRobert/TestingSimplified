from django.db import models


# Create your models here.
class Bug(models.Model):
    title = models.TextField()
    priority = models.TextField()
    description = models.TextField()
    steps = models.TextField()
    impact = models.TextField()
    project = models.ForeignKey('Project', models.DO_NOTHING, to_field=None)
    location = models.TextField()

    class Meta:
        managed = False
        db_table = 'bug'


class BugStatus(models.Model):
    detected_1 = models.BooleanField(db_default=False)
    detected_2 = models.BooleanField(db_default=False)
    detected_3 = models.BooleanField(db_default=False)
    located_1 = models.BooleanField(db_default=False)
    located_2 = models.BooleanField(db_default=False)
    located_3 = models.BooleanField(db_default=False)
    located_4 = models.BooleanField(db_default=False)
    fixed_1 = models.BooleanField(db_default=False)
    fixed_2 = models.BooleanField(db_default=False)
    fixed_3 = models.BooleanField(db_default=False)
    closed_1 = models.BooleanField(db_default=False)
    closed_2 = models.BooleanField(db_default=False)
    bug = models.ForeignKey(Bug, models.DO_NOTHING, to_field=None)

    class Meta:
        managed = False
        db_table = 'bug_status'


class Bugcontent(models.Model):
    content = models.ImageField(blank=True, null=True, upload_to='images/')
    link = models.TextField()
    bug = models.ForeignKey(Bug, models.DO_NOTHING, to_field=None)

    class Meta:
        managed = False
        db_table = 'bugcontent'


class Project(models.Model):
    title = models.TextField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project'


class Test(models.Model):
    title = models.TextField()
    prerequisites = models.TextField()
    priority = models.TextField(db_default='MINOR')
    description = models.TextField()
    steps = models.TextField()
    results = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, models.DO_NOTHING, to_field=None)
    outcome = models.TextField(blank=True, null=True, db_default='-')

    class Meta:
        managed = False
        db_table = 'test'


class TestStatus(models.Model):
    defined_1 = models.BooleanField(db_default=False)
    defined_2 = models.BooleanField(db_default=False)
    defined_3 = models.BooleanField(db_default=False)
    defined_4 = models.BooleanField(db_default=False)
    specified_1 = models.BooleanField(db_default=False)
    specified_2 = models.BooleanField(db_default=False)
    specified_3 = models.BooleanField(db_default=False)
    specified_4 = models.BooleanField(db_default=False)
    specified_5 = models.BooleanField(db_default=False)
    specified_6 = models.BooleanField(db_default=False)
    executed_1 = models.BooleanField(db_default=False)
    executed_2 = models.BooleanField(db_default=False)
    evaluated_1 = models.BooleanField(db_default=False)
    evaluated_2 = models.BooleanField(db_default=False)
    evaluated_3 = models.BooleanField(db_default=False)
    test = models.ForeignKey(Test, models.DO_NOTHING, to_field=None)

    class Meta:
        managed = False
        db_table = 'test_status'


class Testcontent(models.Model):
    link = models.TextField(db_default='-')
    content = models.ImageField(blank=True, null=True, upload_to='images/')
    test = models.ForeignKey(Test, models.DO_NOTHING, to_field=None)

    class Meta:
        managed = False
        db_table = 'testcontent'


class User(models.Model):
    username = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='images/')

    logged_in = models.BooleanField(db_default=False)

    class Meta:
        managed = False
        db_table = 'user'


class User2Bug(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, to_field=None)
    bug = models.ForeignKey(Bug, models.DO_NOTHING, to_field=None)

    class Meta:
        managed = False
        db_table = 'user2bug'


class User2Project(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, to_field=None)
    project_field = models.ForeignKey(Project, models.DO_NOTHING, db_column='project__id', to_field=None)  # Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'user2project'


class User2Test(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, to_field=None)
    test = models.ForeignKey(Test, models.DO_NOTHING, to_field=None)

    class Meta:
        managed = False
        db_table = 'user2test'
