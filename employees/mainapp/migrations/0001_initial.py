# Generated by Django 3.2.9 on 2021-12-04 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('web_site', models.URLField(verbose_name='website')),
                ('email', models.EmailField(max_length=254)),
                ('logo', models.ImageField(upload_to='logos')),
                ('post_index', models.IntegerField(verbose_name='post index')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=20)),
                ('job_position', models.CharField(max_length=40, verbose_name='job position')),
                ('is_manager', models.BooleanField(default=False, verbose_name='is manager')),
                ('is_admin', models.BooleanField(default=False, verbose_name='is admin')),
                ('phone_number', models.CharField(max_length=30, verbose_name='phone number')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='mainapp.company')),
            ],
        ),
        migrations.AddIndex(
            model_name='employee',
            index=models.Index(fields=['name', 'surname'], name='mainapp_emp_name_0fdfed_idx'),
        ),
    ]
