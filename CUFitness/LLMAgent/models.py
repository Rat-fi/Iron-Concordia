from django.db import models
from django.conf import settings  

class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('ai', 'AI'),
    ]
    session_key = models.CharField(
        max_length=40,
        help_text="Unique session identifier for the conversation."
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE
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


class FitnessPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan_content = models.TextField("Generated Fitness Plan")
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Plan - {'✔️ Confirmed' if self.confirmed else '❌ Pending'}"