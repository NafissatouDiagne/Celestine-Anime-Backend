# Generated by Django 4.1.5 on 2023-11-21 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mikey', '0007_alter_comment_disliked_by_alter_comment_liked_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='disliked_by',
            field=models.ManyToManyField(blank=True, related_name='disliked_comments', to='mikey.register'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='liked_by',
            field=models.ManyToManyField(blank=True, related_name='liked_comments', to='mikey.register'),
        ),
    ]
