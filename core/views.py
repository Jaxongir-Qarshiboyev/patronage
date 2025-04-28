from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import Count
from django.db.models.functions import TruncMonth
from collections import defaultdict
from django.utils import timezone
from .models import District, Polyclinic, Doctor, Family, FamilyMember, Patronage, HouseholdPatronage, Newborn, DisabledPerson
from .serializers import DistrictSerializer, PolyclinicSerializer, DoctorSerializer, FamilySerializer, FamilyMemberSerializer, PatronageSerializer, HouseholdPatronageSerializer, NewbornSerializer, DisabledPersonSerializer

# ModelViewSet’lar
class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]

class PolyclinicViewSet(viewsets.ModelViewSet):
    queryset = Polyclinic.objects.all()
    serializer_class = PolyclinicSerializer
    permission_classes = [IsAuthenticated]

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [IsAuthenticated]

class FamilyMemberViewSet(viewsets.ModelViewSet):
    queryset = FamilyMember.objects.all()
    serializer_class = FamilyMemberSerializer
    permission_classes = [IsAuthenticated]

class PatronageViewSet(viewsets.ModelViewSet):
    queryset = Patronage.objects.all()
    serializer_class = PatronageSerializer
    permission_classes = [IsAuthenticated]

class HouseholdPatronageViewSet(viewsets.ModelViewSet):
    queryset = HouseholdPatronage.objects.all()
    serializer_class = HouseholdPatronageSerializer
    permission_classes = [IsAuthenticated]

class NewbornViewSet(viewsets.ModelViewSet):
    queryset = Newborn.objects.all()
    serializer_class = NewbornSerializer
    permission_classes = [IsAuthenticated]

class DisabledPersonViewSet(viewsets.ModelViewSet):
    queryset = DisabledPerson.objects.all()
    serializer_class = DisabledPersonSerializer
    permission_classes = [IsAuthenticated]

# Statistik ma'lumotlar uchun endpoint
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stats(request):
    year = request.query_params.get('year', None)
    district = request.query_params.get('district', None)
    filters = {}
    if year:
        filters['visit_date__year'] = year
    if district:
        filters['family__district__name'] = district

    # 1. Umumiy statistika
    total_families = Family.objects.filter(**filters).count()
    total_patronages = Patronage.objects.filter(**filters).count()
    total_newborns = Newborn.objects.filter(**filters).count()

    summary = {
        'total_families': total_families,
        'total_patronages': total_patronages,
        'total_newborns': total_newborns,
    }

    # 2. Oylar bo‘yicha patronajlar trendi (Line Chart uchun)
    patronages_by_month = Patronage.objects.filter(**filters).annotate(
        month=TruncMonth('visit_date')
    ).values('month', 'status').annotate(count=Count('id')).order_by('month')

    monthly_trend = defaultdict(lambda: {'Scheduled': 0, 'Completed': 0, 'Cancelled': 0})
    for entry in patronages_by_month:
        month_str = entry['month'].strftime('%Y-%m') if entry['month'] else 'Unknown'
        monthly_trend[month_str][entry['status']] = entry['count']

    monthly_trend_data = [
        {'month': month, 'Scheduled': data['Scheduled'], 'Completed': data['Completed'], 'Cancelled': data['Cancelled']}
        for month, data in monthly_trend.items()
    ]

    # 3. Jins bo'yicha statistika (Pie Chart uchun)
    gender_stats = FamilyMember.objects.filter(**filters).values('gender').annotate(count=Count('id'))
    gender_data = {
        'male': next((item['count'] for item in gender_stats if item['gender'] == 'M'), 0),
        'female': next((item['count'] for item in gender_stats if item['gender'] == 'F'), 0),
    }

    # 4. Yosh guruhlari bo'yicha statistika (Bar Chart uchun)
    age_groups = {
        'under_15': FamilyMember.objects.filter(birth_date__gte=timezone.now() - timezone.timedelta(days=15*365)).count(),
        '15_30': FamilyMember.objects.filter(birth_date__lte=timezone.now() - timezone.timedelta(days=15*365),
                                             birth_date__gte=timezone.now() - timezone.timedelta(days=30*365)).count(),
        '30_50': FamilyMember.objects.filter(birth_date__lte=timezone.now() - timezone.timedelta(days=30*365),
                                             birth_date__gte=timezone.now() - timezone.timedelta(days=50*365)).count(),
        'over_50': FamilyMember.objects.filter(birth_date__lte=timezone.now() - timezone.timedelta(days=50*365)).count(),
    }
    total_age_members = sum(age_groups.values())
    age_percentages = {
        'under_15': (age_groups['under_15'] / total_age_members * 100) if total_age_members > 0 else 0,
        '15_30': (age_groups['15_30'] / total_age_members * 100) if total_age_members > 0 else 0,
        '30_50': (age_groups['30_50'] / total_age_members * 100) if total_age_members > 0 else 0,
        'over_50': (age_groups['over_50'] / total_age_members * 100) if total_age_members > 0 else 0,
    }

    # 5. Patronaj turlari bo‘yicha taqsimot (Pie Chart uchun)
    household_patronages = HouseholdPatronage.objects.filter(**filters).count()
    total_patronages_count = Patronage.objects.filter(**filters).count()
    other_patronages = total_patronages_count - household_patronages
    patronage_types = {
        'household': household_patronages,
        'other': other_patronages,
    }

    # 6. Tumanlar bo‘yicha oilalar soni (Bar Chart uchun)
    families_by_district = Family.objects.filter(**filters).values('district__name').annotate(count=Count('id')).order_by('-count')
    district_families_data = [
        {'name': item['district__name'] if item['district__name'] else 'Nomalum', 'count': item['count']}
        for item in families_by_district
    ]

    # 7. Poliklinikalar bo‘yicha patronajlar soni (Bar Chart uchun)
    patronages_by_polyclinic = Patronage.objects.filter(**filters).values('family__polyclinic__name').annotate(count=Count('id')).order_by('-count')
    polyclinic_data = [
        {'name': item['family__polyclinic__name'] if item['family__polyclinic__name'] else 'Nomalum', 'count': item['count']}
        for item in patronages_by_polyclinic
    ]

    # 8. Shifokorlar bo‘yicha patronajlar taqsimoti (Pie Chart uchun)
    doctor_patronages = Patronage.objects.filter(**filters).values('doctor__user__username').annotate(count=Count('id')).order_by('-count')
    doctor_data = [
        {'name': item['doctor__user__username'] if item['doctor__user__username'] else 'Nomalum', 'count': item['count']}
        for item in doctor_patronages
    ]

    # 9. Oylar bo‘yicha yangi tug‘ilgan chaqaloqlar trendi (Line Chart uchun)
    newborns_by_month = Newborn.objects.filter(**filters).annotate(
        month=TruncMonth('birth_date')
    ).values('month').annotate(count=Count('id')).order_by('month')

    newborn_trend = defaultdict(int)
    for entry in newborns_by_month:
        month_str = entry['month'].strftime('%Y-%m') if entry['month'] else 'Unknown'
        newborn_trend[month_str] = entry['count']

    newborn_trend_data = [
        {'month': month, 'count': count}
        for month, count in newborn_trend.items()
    ]

    # 10. Nogironlar bo‘yicha statistika (tumanlar bo‘yicha, Bar Chart uchun)
    disabled_by_district = DisabledPerson.objects.filter(**filters).values('family__district__name').annotate(count=Count('id')).order_by('-count')
    disabled_data = [
        {'name': item['family__district__name'] if item['family__district__name'] else 'Nomalum', 'count': item['count']}
        for item in disabled_by_district
    ]

    return Response({
        'summary': summary,
        'monthly_trend': monthly_trend_data,
        'gender_data': gender_data,
        'age_data': {
            'counts': age_groups,
            'percentages': age_percentages,
        },
        'patronage_types': patronage_types,
        'district_families_data': district_families_data,
        'polyclinic_data': polyclinic_data,
        'doctor_data': doctor_data,
        'newborn_trend': newborn_trend_data,
        'disabled_data': disabled_data,
    })

# Oilalar qo‘shish uchun endpoint
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_family(request):
    serializer = FamilySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Patronaj qo‘shish uchun endpoint
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_patronage(request):
    serializer = PatronageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Foydalanuvchi login qilishi uchun endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
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
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)