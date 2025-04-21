from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class District(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Polyclinic(models.Model):
    name = models.CharField(max_length=100, default="Unknown")
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    polyclinic = models.ForeignKey(Polyclinic, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.specialty}"

class Family(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=50, default='Active')
    polyclinic = models.ForeignKey(Polyclinic, on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class FamilyMember(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.family.name}"

class Patronage(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True)
    visit_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=50, default='Scheduled')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Patronage for {self.family.name} on {self.visit_date}"

class HouseholdPatronage(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True)
    visit_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=50, default='Scheduled')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Household Patronage for {self.family.name} on {self.visit_date}"

class Newborn(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - Newborn"

class DisabledPerson(models.Model):
    name = models.CharField(max_length=100)
    disability_id = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - Disabled"