# Generated by Django 4.2.16 on 2024-11-21 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_remove_news_id_alter_news_article_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mediacompany',
            old_name='comapany_name',
            new_name='company_name',
        ),
    ]
