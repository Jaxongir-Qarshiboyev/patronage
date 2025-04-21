from django.contrib import admin
from .models import District, Polyclinic, Doctor, Family, FamilyMember, Patronage, HouseholdPatronage, Newborn, DisabledPerson

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')

@admin.register(Polyclinic)
class PolyclinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'address', 'phone')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'polyclinic')

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'status', 'polyclinic')

@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'family', 'birth_date', 'gender')

@admin.register(Patronage)
class PatronageAdmin(admin.ModelAdmin):
    list_display = ('family', 'visit_date', 'status', 'doctor')

@admin.register(HouseholdPatronage)
class HouseholdPatronageAdmin(admin.ModelAdmin):
    list_display = ('family', 'visit_date', 'status')

@admin.register(Newborn)
class NewbornAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'family')

@admin.register(DisabledPerson)
class DisabledPersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'disability_id', 'family')