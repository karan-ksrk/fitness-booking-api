# 🏋️‍♀️ Fitness Class Booking API

A Django REST API for managing and booking fitness classes.

#### Postman collection for this project is avaialable [here](https://www.postman.com/interstellar-desert-4342-1/workspace/fitness-class-booking/collection/7249639-b5fc3b05-b441-4590-bb85-b89137f3bc87?action=share&creator=7249639)

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

**GET** `/classes/`  
Lists upcoming classes

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

To run all api tests:

```bash
python manage.py test -v2
```

## Booking Test Cases Coverage

### 1. `test_get_classes`

- Verifies retrieval of available fitness classes.
- Checks that the returned class list contains the correct names ("Yoga", "Zumba", "HIIT").

### 2. `test_get_classes_with_timezone`

- Ensures class start times are correctly converted to different time zones.

### 3. `test_booking_success`

- Validates successful booking creation and slot decrement.

### 4. `test_booking_failure_missing_fields`

- Ensures booking fails when required fields (like `class_id`) are missing.

### 5. `test_booking_failure_existing_booking`

- Verifies booking fails if a client already has a reservation for the same class.

### 6. `test_booking_failure_no_available_slots`

- Ensures booking fails when there are no available slots in a class.

### 7. `test_booking_failure_class_not_found`

- Verifies booking fails when an invalid class ID is provided.

---
