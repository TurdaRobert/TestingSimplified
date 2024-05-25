# Generated by Django 5.0.1 on 2024-04-14 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appLicenta', '0002_alter_user_email_alter_user_password_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('status', models.IntegerField()),
                ('priority', models.TextField()),
                ('description', models.TextField()),
                ('steps', models.TextField()),
                ('impact', models.TextField()),
            ],
            options={
                'db_table': 'bug',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Bugcontent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.BinaryField(blank=True, null=True)),
                ('link', models.TextField()),
            ],
            options={
                'db_table': 'bugcontent',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'project',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('status', models.IntegerField()),
                ('prerequisites', models.TextField()),
                ('priority', models.TextField()),
                ('description', models.TextField()),
                ('steps', models.TextField()),
                ('results', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'test',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Testcontent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.TextField()),
                ('content', models.BinaryField(blank=True, null=True)),
            ],
            options={
                'db_table': 'testcontent',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User2Bug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'user2bug',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User2Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'user2project',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User2Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'user2test',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'managed': False},
        ),
    ]
