# Generated by Django 5.1.5 on 2025-03-13 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ChatMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "session_key",
                    models.CharField(
                        help_text="Unique session identifier for the conversation.",
                        max_length=40,
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[("user", "User"), ("ai", "AI")],
                        help_text="Indicates whether the message is from the user or the AI.",
                        max_length=10,
                    ),
                ),
                (
                    "message",
                    models.TextField(help_text="The content of the chat message."),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="The date and time when the message was created.",
                    ),
                ),
            ],
        ),
    ]
