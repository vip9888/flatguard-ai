from django.db import models
from django.utils import timezone

# Create your models here.

class Alert(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='alerts/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']
