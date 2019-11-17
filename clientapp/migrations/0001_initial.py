# Generated by Django 2.2 on 2019-09-11 15:30

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('preview_descr', models.TextField()),
                ('preview_img', models.FileField(null=True, upload_to='images')),
                ('min_price', models.IntegerField()),
                ('coords', models.CharField(max_length=200, null=True)),
                ('activity_status', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(null=True)),
                ('preview_descr', models.TextField()),
                ('preview_img', models.FileField(null=True, upload_to='images')),
                ('coords', models.CharField(max_length=200, null=True)),
                ('activity_status', models.BooleanField()),
                ('min_price', models.IntegerField()),
                ('show_on_main_status', models.BooleanField()),
                ('header_place', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='placee', to='clientapp.Place')),
            ],
        ),
        migrations.CreateModel(
            name='Publications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('preview_descr', models.TextField()),
                ('allText', models.TextField()),
                ('preview_img', models.FileField(null=True, upload_to='images')),
                ('img', models.FileField(null=True, upload_to='images')),
                ('activity_status', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('img', models.FileField(null=True, upload_to='images')),
                ('show_on_main_status', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('position', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('img', models.FileField(null=True, upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('url', models.CharField(max_length=200)),
                ('number_of_days', models.IntegerField()),
                ('min_price', models.IntegerField()),
                ('preview_descr', models.TextField()),
                ('preview_img', models.FileField(blank=True, null=True, upload_to='images')),
                ('activity_status', models.BooleanField()),
                ('show_on_main_status', models.BooleanField()),
                ('places', models.ManyToManyField(blank=True, null=True, to='clientapp.Place')),
                ('slider', models.ManyToManyField(blank=True, null=True, to='clientapp.Slider')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TourInTimetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('date', models.DateField()),
                ('capacity', models.IntegerField()),
                ('hotels', models.ManyToManyField(to='clientapp.Hotel')),
                ('tourID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientapp.Tour')),
            ],
        ),
        migrations.AddField(
            model_name='place',
            name='slider',
            field=models.ManyToManyField(to='clientapp.Slider'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientapp.Place'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='slider',
            field=models.ManyToManyField(blank=True, null=True, to='clientapp.Slider'),
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=200)),
                ('number', models.IntegerField()),
                ('description', models.TextField()),
                ('img', models.FileField(null=True, upload_to='images')),
                ('tourID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientapp.Tour')),
            ],
        ),
        migrations.CreateModel(
            name='BookingTour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=200)),
                ('payment', models.IntegerField()),
                ('tourInT', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientapp.TourInTimetable')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
