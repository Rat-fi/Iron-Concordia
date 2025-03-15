from django.db import models

class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('ai', 'AI'),
    ]
    session_key = models.CharField(
        max_length=40,
        help_text="Unique session identifier for the conversation."
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        help_text="Indicates whether the message is from the user or the AI."
    )
    message = models.TextField(
        help_text="The content of the chat message."
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the message was created."
    )

    def __str__(self):
        return f"{self.session_key} - {self.role}: {self.message[:50]}"
