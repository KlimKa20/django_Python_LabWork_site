# Generated by Django 3.0.4 on 2020-04-24 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_reply_capt', models.CharField(blank=True, max_length=500, verbose_name='Заголовок ответа на e-mail')),
                ('email_reply_text', models.TextField(blank=True, null=True, verbose_name='Текст ответа на e-mail')),
            ],
        ),
    ]