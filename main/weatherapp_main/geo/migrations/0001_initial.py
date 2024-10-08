# Generated by Django 5.1.1 on 2024-10-07 07:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('latitude', models.DecimalField(decimal_places=5, max_digits=8)),
                ('longitude', models.DecimalField(decimal_places=5, max_digits=8)),
                ('is_default', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('user', 'name'), name='unique_user_name', nulls_distinct=False), models.UniqueConstraint(condition=models.Q(('is_default', True)), fields=('user', 'is_default'), name='unique_user_is_default', nulls_distinct=False)],
            },
        ),
    ]
