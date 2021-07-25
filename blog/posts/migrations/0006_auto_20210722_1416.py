# Generated by Django 3.2.5 on 2021-07-22 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_remove_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('D', 'Draft'), ('P', 'Published'), ('R', 'Rejected')], default='D', max_length=2),
        ),
        migrations.AlterField(
            model_name='postcategories',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_categories', to='posts.post'),
        ),
    ]
