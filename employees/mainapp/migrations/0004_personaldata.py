# Generated by Django 3.2.9 on 2021-12-04 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20211204_2120'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalData',
            fields=[
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='data', serialize=False, to='mainapp.employee')),
                ('date_of_birth', models.DateField(verbose_name='date of birth')),
                ('home_address', models.CharField(max_length=150, verbose_name='address')),
                ('salary', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
    ]
