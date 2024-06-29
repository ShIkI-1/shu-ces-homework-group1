# Generated by Django 4.2.11 on 2024-06-27 06:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('aiPlatformImplement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='aiEngine',
            fields=[
                ('id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('name', models.CharField(default='默认对话Ai引擎', max_length=32)),
                ('subname', models.CharField(default='默认提供，免费使用的轻量Ai引擎', max_length=88)),
            ],
        ),
        migrations.CreateModel(
            name='chatHistoryIndex',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('engineID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aiPlatformImplement.aiengine')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aiPlatformImplement.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='chatHistoryContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.BooleanField(default=False)),
                ('chatContent', models.TextField()),
                ('messageID', models.IntegerField(default=0)),
                ('indexID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aiPlatformImplement.chathistoryindex')),
            ],
        ),
        migrations.AddConstraint(
            model_name='chathistorycontent',
            constraint=models.UniqueConstraint(fields=('indexID', 'messageID'), name='unique_indexID_messageID'),
        ),
    ]
