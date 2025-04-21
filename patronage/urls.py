from django.urls import path, include
from django.contrib import admin  # Admin uchun import qo‘shildi
from rest_framework.routers import DefaultRouter
from core.views import DistrictViewSet, PolyclinicViewSet, DoctorViewSet, FamilyViewSet, FamilyMemberViewSet, PatronageViewSet, HouseholdPatronageViewSet, NewbornViewSet, DisabledPersonViewSet, stats, add_family, add_patronage, user_login, user_logout

router = DefaultRouter()
router.register(r'districts', DistrictViewSet)
router.register(r'polyclinics', PolyclinicViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'families', FamilyViewSet)
router.register(r'family-members', FamilyMemberViewSet)
router.register(r'patronages', PatronageViewSet)
router.register(r'household-patronages', HouseholdPatronageViewSet)
router.register(r'newborns', NewbornViewSet)
router.register(r'disabled-persons', DisabledPersonViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin paneli uchun yo‘l qo‘shildi
    path('api/', include(router.urls)),
    path('api/stats/', stats, name='stats'),
    path('api/add-family/', add_family, name='add-family'),
    path('api/add-patronage/', add_patronage, name='add-patronage'),
    path('api/login/', user_login, name='login'),
    path('api/logout/', user_logout, name='logout'),
]