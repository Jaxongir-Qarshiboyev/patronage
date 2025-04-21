# 🏥 Hamshiralar Monitoring Tizimi (Backend)

![Django](https://img.shields.io/badge/Django-4.2.11-brightgreen.svg)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.15.1-blue.svg)

**Hamshiralar Monitoring Tizimi** — bu backend loyihasi bo‘lib, hamshiralarga oilalarni patronaj qilish, tashriflarni boshqarish va monitoring ma'lumotlarini saqlash imkonini beradi. Django va Django REST Framework asosida qurilgan bo‘lib, frontend uchun kuchli API xizmatlarini taqdim etadi.

---

## 📋 Loyiha haqida

- **Framework**: Django 4.2.11  
- **API**: Django REST Framework 3.15.1  
- **Ma'lumotlar bazasi**: SQLite (standart, PostgreSQL bilan almashtirish mumkin)  
- **CORS**: `django-cors-headers` orqali frontend bilan muloqot

---

## 🛠 O‘rnatish va ishga tushirish

### 1-qadam: Dasturlarni o‘rnatish

Quyidagilar o‘rnatilgan bo‘lishi kerak:

- **Python 3.8+**  
  ```bash
  python3 --version
  ```
- **Git**  
  ```bash
  git --version
  ```

### 2-qadam: Repozitoriyani klon qilish

```bash
git clone https://github.com/Jaxongir-Qarshiboyev/patronage.git
cd patronage
```

### 3-qadam: Virtual muhitni yaratish va faollashtirish

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/MacOS
# Windows: venv\Scripts\activate
```

### 4-qadam: Kerakli paketlarni o‘rnatish

```bash
pip install -r requirements.txt
# Agar xato chiqsa:
pip install --upgrade pip
```

### 5-qadam: Ma'lumotlar bazasini sozlash

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6-qadam: Admin foydalanuvchi yaratish (ixtiyoriy)

```bash
python manage.py createsuperuser
```

### 7-qadam: Serverni ishga tushirish

```bash
python manage.py runserver
```

**Natija:**
```
Starting development server at http://127.0.0.1:8000/
```

---

## 🔌 API’ni sinab ko‘rish

- Oilalar ro‘yxati: [http://127.0.0.1:8000/api/families/](http://127.0.0.1:8000/api/families/)  
- Patronajlar ro‘yxati: [http://127.0.0.1:8000/api/household-patronages/](http://127.0.0.1:8000/api/household-patronages/)  
- Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 📦 Foydalanilgan paketlar

```text
Django==4.2.11
djangorestframework==3.15.1
django-cors-headers==4.3.1
```

---

## 🔧 Qo‘shimcha sozlamalar

### PostgreSQL bilan ishlash

1. `requirements.txt` fayliga quyidagini qo‘shing:

```text
psycopg2-binary==2.9.9
```

2. `settings.py` faylida:

```python
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
```

3. Migratsiya qiling:
```bash
python manage.py migrate
```

### CORS sozlamalari

Frontend bilan to‘g‘ri ishlashi uchun `settings.py` faylida:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

---

## 📁 Loyiha tuzilishi

- `api/`: API view’lar va serializer’lar  
- `patronage/`: Asosiy loyiha konfiguratsiyasi (`settings.py`, `urls.py`)  
- `models.py`: Ma'lumotlar bazasi modellari (oilalar, patronajlar va boshqalar)

---

## 🤝 Hissadorlik

Loyiha ochiq manbali. Hissa qo‘shmoqchi bo‘lsangiz:

1. Repozitoriyani `fork` qiling  
2. O‘zgarishlarni kiritib, `commit` qiling  
3. `Pull request` yuboring

---

## 📞 Aloqa

Savollar yoki takliflar uchun bog‘laning: **Jaxongir Qarshiboyev**

© 2025 Hamshiralar Monitoring Tizimi loyihasi
