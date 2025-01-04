from djongo import models

class Evidence(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='evidence_files/')

    def __str__(self):
        return self.title
