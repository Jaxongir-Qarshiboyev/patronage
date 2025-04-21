from rest_framework import serializers
from .models import District, Polyclinic, Doctor, Family, FamilyMember, Patronage, HouseholdPatronage, Newborn, DisabledPerson

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name', 'region']

class PolyclinicSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.name', read_only=True)

    class Meta:
        model = Polyclinic
        fields = ['id', 'name', 'district', 'district_name', 'address', 'phone']

class DoctorSerializer(serializers.ModelSerializer):
    polyclinic_name = serializers.CharField(source='polyclinic.name', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialty', 'polyclinic', 'polyclinic_name']

class FamilySerializer(serializers.ModelSerializer):
    polyclinic_name = serializers.CharField(source='polyclinic.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)

    class Meta:
        model = Family
        fields = ['id', 'name', 'phone', 'status', 'polyclinic', 'polyclinic_name', 'district', 'district_name']

class FamilyMemberSerializer(serializers.ModelSerializer):
    family_name = serializers.CharField(source='family.name', read_only=True)

    class Meta:
        model = FamilyMember
        fields = ['id', 'family', 'family_name', 'name', 'birth_date', 'gender', 'address']

class PatronageSerializer(serializers.ModelSerializer):
    family_name = serializers.CharField(source='family.name', read_only=True)

    class Meta:
        model = Patronage
        fields = ['id', 'family', 'family_name', 'visit_date', 'status', 'doctor']

class HouseholdPatronageSerializer(serializers.ModelSerializer):
    family_name = serializers.CharField(source='family.name', read_only=True)

    class Meta:
        model = HouseholdPatronage
        fields = ['id', 'family', 'family_name', 'visit_date', 'status', 'notes']

class NewbornSerializer(serializers.ModelSerializer):
    family_name = serializers.CharField(source='family.name', read_only=True)

    class Meta:
        model = Newborn
        fields = ['id', 'name', 'birth_date', 'gender', 'family', 'family_name']

class DisabledPersonSerializer(serializers.ModelSerializer):
    family_name = serializers.CharField(source='family.name', read_only=True)

    class Meta:
        model = DisabledPerson
        fields = ['id', 'name', 'disability_id', 'address', 'family', 'family_name']