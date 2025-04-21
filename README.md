# Hamshiralar Monitoring Tizimi (Backend)

![Django](https://img.shields.io/badge/Django-4.2.11-brightgreen.svg)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.15.1-blue.svg)

Ushbu loyiha **Hamshiralar Monitoring Tizimi**ning backend qismidir. Bu tizim hamshiralarga oilalarni patronaj qilish, tashriflarni boshqarish va monitoring ma'lumotlarini saqlash imkonini beradi. Backend Django framework’i va Django REST Framework yordamida qurilgan bo‘lib, API xizmatlarini taqdim etadi.

## 📋 Loyiha haqida

- **Framework**: Django 4.2.11
- **API**: Django REST Framework 3.15.1
- **Ma'lumotlar bazasi**: SQLite (standart, PostgreSQL bilan almashtirish mumkin)
- **CORS**: Frontend bilan muloqot qilish uchun `django-cors-headers` ishlatiladi.

## 🛠 O‘rnatish va ishga tushirish qadamlari

### 1-qadam: Kerakli dasturlarni o‘rnatish
Loyiha ishga tushishi uchun quyidagi dasturlar o‘rnatilgan bo‘lishi kerak:
- **Python 3.8+**: Python o‘rnatilganligini tekshirish uchun terminalda quyidagi buyruqni bajaring:
  ```bash
  python3 --version
Agar o‘rnatilmagan bo‘lsa, rasmiy saytdan yuklab o‘rnating.

Git: Git o‘rnatilganligini tekshirish uchun:
bash

Copy
git --version
Agar o‘rnatilmagan bo‘lsa, rasmiy saytdan o‘rnating.
2-qadam: Repozitoriyani klon qilish
Loyihani mahalliy kompyuteringizga yuklab oling:

bash

Copy
git clone https://github.com/Jaxongir-Qarshiboyev/patronage.git
cd patronage
3-qadam: Virtual muhitni yaratish va faollashtirish
Python virtual muhitini yaratib, faollashtiring:

bash

Copy
python3 -m venv venv
source venv/bin/activate  # Linux/MacOS uchun
# Windows uchun: venv\Scripts\activate
Virtual muhit faollashganda terminalda (venv) belgisini ko‘rasiz.

4-qadam: Kerakli paketlarni o‘rnatish
requirements.txt faylidagi paketlarni o‘rnating:

bash

Copy
pip install -r requirements.txt
Agar o‘rnatishda xato chiqsa, pip ni yangilang:

bash

Copy
pip install --upgrade pip
5-qadam: Ma'lumotlar bazasini sozlash
Django migratsiyalarini ishga tushiring:

bash

Copy
python manage.py makemigrations
python manage.py migrate
Bu SQLite ma'lumotlar bazasini yaratadi va kerakli jadvallarni sozlaydi.

6-qadam: Admin foydalanuvchi yaratish (ixtiyoriy)
Agar admin panelidan foydalanmoqchi bo‘lsangiz, superuser yarating:

bash

Copy
python manage.py createsuperuser
Foydalanuvchi nomi, email va parolni kiriting (email ixtiyoriy).
7-qadam: Serverni ishga tushirish
Django serverini ishga tushiring:

bash

Copy
python manage.py runserver
Server ishga tushganda quyidagi xabarni ko‘rasiz:

text

Copy
Starting development server at http://127.0.0.1:8000/
8-qadam: API’ni sinab ko‘rish
Server ishlayotgan bo‘lsa, quyidagi manzillarni brauzer yoki Postman orqali sinab ko‘ring:

Oilalar ro‘yxati: http://127.0.0.1:8000/api/families/
Patronajlar ro‘yxati: http://127.0.0.1:8000/api/household-patronages/
Admin panel: http://127.0.0.1:8000/admin/ (superuser hisobi bilan kiring).
📦 Foydalanilgan paketlar
Django==4.2.11
djangorestframework==3.15.1
django-cors-headers==4.3.1
🔧 Qo‘shimcha sozlamalar
PostgreSQL bilan ishlash:
requirements.txt ga psycopg2-binary ni qo‘shing:
text

Copy
psycopg2-binary==2.9.9
settings.py faylida ma'lumotlar bazasi sozlamalarini PostgreSQL’ga o‘zgartiring:
python

Copy
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
Qayta migratsiya qiling: python manage.py migrate.
CORS sozlamalari: Frontend bilan muammosiz muloqot qilish uchun settings.py dagi CORS_ALLOWED_ORIGINS ga frontend manzilini qo‘shing:
python

Copy
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
📄 Loyiha tuzilishi
api/: API uchun view’lar va serializer’lar.
patronage/: Asosiy loyiha sozlamalari (settings.py, urls.py).
models.py: Ma'lumotlar bazasi modellari (oilalar, patronajlar va boshqalar).
🤝 Hissadorlik
Loyiha ochiq manba sifatida taqdim etiladi. Agar o‘zgarishlar kiritmoqchi bo‘lsangiz:

Repozitoriyani fork qiling.
O‘zgarishlarni kiritib, commit qiling.
Pull request yuboring.
📞 Aloqa
Savollar yoki takliflar bo‘lsa, Jaxongir Qarshiboyev bilan bog‘laning.

© 2025 Hamshiralar Monitoring Tizimi loyihasi