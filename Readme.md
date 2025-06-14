# 🏋️‍♀️ Fitness Class Booking API

A Django REST API for managing and booking fitness classes.

#### Postman collection for this project is avaialable [here](https://www.postman.com/interstellar-desert-4342-1/workspace/fitness-class-booking/request/7249639-308d35c6-a782-40f6-a074-21e3b11d7994?action=share&creator=7249639&ctx=documentation)

---

## ⚙️ Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/karan-ksrk/fitness-booking-api.git
cd fitness-booking-api
```

2. **Create and activate virtual environment**

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Apply migrations**

```bash
python manage.py migrate
```

5. **Load sample data**

```bash
python manage.py add_sample_data
```

6. **Run the development server**

```bash
python manage.py runserver
```

---

## 🚀 Endpoints

### 1. List Available Classes

**GET** `/classes/?tz=Asia/Kolkata`  
Lists upcoming classes with optional timezone adjustment.

### 2. Book a Class

**POST** `/book/`  
Book a class by sending `class_id`, `client_name`, and `client_email`.

### 3. List Bookings by Email

**GET** `/bookings/?email=your@email.com`  
Retrieve all bookings made by a client.

---

## 🛠️ Sample data using Management Command

### `add_sample_data`

Custom Django management command that seeds the database with demo fitness classes.

**Location:** `\booking_api\management\commands\add_sample_data.py`

**Example:**

```bash
python manage.py add_sample_data
```

---

## ✅ Testing

To run all unit tests:

```bash
python manage.py test
```

---
