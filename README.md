# IRCTC Clone

This is a Django-based IRCTC Clone project that requires a MySQL database connection.

## Prerequisites

Ensure you have the following installed before setting up the project:

- Python (>=3.8)
- Django (Check `requirements.txt` for the version)
- MySQL Server
- pip (Python package manager)
- Virtual environment (`venv`)

## Installation and Setup

### 1. Clone the Repository

```sh
git clone <repository-url>
cd irctc_clone
```

### 2. Create a Virtual Environment

```sh
python -m venv venv
```

Activate the virtual environment:

- On Windows:
  ```sh
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```sh
  source venv/bin/activate
  ```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Configure MySQL Database

1. Create a MySQL database:
   ```sql
   CREATE DATABASE irctc_clone;
   ```

2. Update `settings.py` with your MySQL credentials:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'irctc_clone',
           'USER': 'root',
           'PASSWORD': '<your-mysql-password>',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

### 5. Apply Migrations

```sh
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Optional)

```sh
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

### 7. Run the Development Server

```sh
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.
