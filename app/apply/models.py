from django.db import models
from django.conf import settings

class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to="resumes/")
    text_extracted = models.TextField()  # raw text extraction
    created_at = models.DateTimeField(auto_now_add=True)


class Experience(models.Model):
    resume = models.ForeignKey(Resume, related_name="experiences", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    achievements = models.TextField(blank=True)


class Education(models.Model):
    resume = models.ForeignKey(Resume, related_name="educations", on_delete=models.CASCADE)
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)


class Skill(models.Model):
    resume = models.ForeignKey(Resume, related_name="skills", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class LanguageProficiency(models.Model):
    resume = models.ForeignKey(Resume, related_name="languages", on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    level = models.CharField(max_length=50, blank=True)  # e.g., 'Native', 'B2'


class Certification(models.Model):
    resume = models.ForeignKey(Resume, related_name="certifications", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255, blank=True)
    date_obtained = models.DateField(null=True, blank=True)


class Project(models.Model):
    resume = models.ForeignKey(Resume, related_name="projects", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    url = models.URLField(blank=True)
    technologies = models.TextField(blank=True)
    role = models.CharField(max_length=255, blank=True)
    achievements = models.TextField(blank=True)