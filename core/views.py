from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import Count
from .models import District, Polyclinic, Doctor, Family, FamilyMember, Patronage, HouseholdPatronage, Newborn, DisabledPerson
from .serializers import DistrictSerializer, PolyclinicSerializer, DoctorSerializer, FamilySerializer, FamilyMemberSerializer, PatronageSerializer, HouseholdPatronageSerializer, NewbornSerializer, DisabledPersonSerializer

# ModelViewSet’lar
class DistrictViewSet(viewsets.ModelViewSet):
    """Tumanlar uchun API endpoint"""
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]

class PolyclinicViewSet(viewsets.ModelViewSet):
    """Poliklinikalar uchun API endpoint"""
    queryset = Polyclinic.objects.all()
    serializer_class = PolyclinicSerializer
    permission_classes = [IsAuthenticated]

class DoctorViewSet(viewsets.ModelViewSet):
    """Shifokorlar uchun API endpoint"""
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

class FamilyViewSet(viewsets.ModelViewSet):
    """Oilalar uchun API endpoint"""
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [IsAuthenticated]

class FamilyMemberViewSet(viewsets.ModelViewSet):
    """Oila a'zolari uchun API endpoint"""
    queryset = FamilyMember.objects.all()
    serializer_class = FamilyMemberSerializer
    permission_classes = [IsAuthenticated]

class PatronageViewSet(viewsets.ModelViewSet):
    """Patronajlar uchun API endpoint"""
    queryset = Patronage.objects.all()
    serializer_class = PatronageSerializer
    permission_classes = [IsAuthenticated]

class HouseholdPatronageViewSet(viewsets.ModelViewSet):
    """Uy patronajlari uchun API endpoint"""
    queryset = HouseholdPatronage.objects.all()
    serializer_class = HouseholdPatronageSerializer
    permission_classes = [IsAuthenticated]

class NewbornViewSet(viewsets.ModelViewSet):
    """Yangi tug‘ilganlar uchun API endpoint"""
    queryset = Newborn.objects.all()
    serializer_class = NewbornSerializer
    permission_classes = [IsAuthenticated]

class DisabledPersonViewSet(viewsets.ModelViewSet):
    """Nogiron shaxslar uchun API endpoint"""
    queryset = DisabledPerson.objects.all()
    serializer_class = DisabledPersonSerializer
    permission_classes = [IsAuthenticated]

# Statistik ma'lumotlar uchun yagona endpoint
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stats(request):
    """Umumiy statistika va tumanlar bo‘yicha statistik ma'lumotlarni qaytaradi"""
    total_families = Family.objects.count()
    total_patronages = Patronage.objects.count()
    total_newborns = Newborn.objects.count()
    total_disabled_persons = DisabledPerson.objects.count()
    family_stats = Family.objects.values('polyclinic__district__name').annotate(total=Count('id'))
    patronage_stats = Patronage.objects.values('family__polyclinic__district__name').annotate(total=Count('id'))

    return Response({
        'total_families': total_families,
        'total_patronages': total_patronages,
        'total_newborns': total_newborns,
        'total_disabled_persons': total_disabled_persons,
        'family_stats': family_stats,
        'patronage_stats': patronage_stats,
    })

# Oilalar qo‘shish uchun endpoint
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_family(request):
    """Yangi oila qo‘shish"""
    serializer = FamilySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Patronaj qo‘shish uchun endpoint
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_patronage(request):
    """Yangi patronaj qo‘shish"""
    serializer = PatronageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Foydalanuvchi login qilishi uchun endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """Foydalanuvchi autentifikatsiyasi va token yaratish"""
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Foydalanuvchi logout qilishi uchun endpoint
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """Foydalanuvchi tokenini o‘chirish orqali tizimdan chiqish"""
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    