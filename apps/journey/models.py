from django.db import models


class Journey(models.Model):
    choices = (("SMALL", "S"), ("MEDIUM", "M"), ("LARGE", "L"))
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=100, blank=True, null=True)
    user_id = models.ForeignKey("user.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    size = models.CharField(max_length=100, choices=choices, default="S")
