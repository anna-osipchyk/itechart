# Generated by Django 3.2.9 on 2021-12-04 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('web_site', models.URLField(verbose_name='website')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(upload_to='media/logos'),
        ),
        migrations.CreateModel(
            name='BankCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bank', to='mainapp.bank')),
                ('company_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company', to='mainapp.company')),
            ],
        ),
    ]