# Pug or Ugh API v1

A dog adoption application that implements a "swipe-style" interface similar to Tinder, but for dog adoption. Built with Django REST Framework and React, this full-stack application allows users to browse adoptable dogs, set preferences, and make adoption decisions.

## Features

- **User Registration & Authentication** - Secure user accounts with token-based authentication
- **Dog Browsing** - Swipe-style interface for browsing adoptable dogs
- **User Preferences** - Set preferences for dog characteristics (age, gender, size)
- **Rating System** - Mark dogs as "liked", "disliked", or "undecided"
- **Filtered Results** - Dogs filtered based on user preferences
- **Interactive Frontend** - React-based UI with smooth user experience

## Technology Stack

### Backend
- **Framework**: Django 3.0.5
- **API**: Django REST Framework 3.11.0
- **Database**: SQLite3 (development)
- **Authentication**: Token Authentication (DRF)
- **Password Security**: Django's built-in password hashing

### Frontend
- **Framework**: React 0.14.7 with React DOM
- **Build Tools**: JSX transpilation via Babel
- **Styling**: Custom CSS
- **DOM Manipulation**: jQuery

### Development Tools
- **Debugging**: Django Debug Toolbar 2.2
- **Testing**: Coverage 5.0.4
- **Code Quality**: autopep8 1.5

## Installation & Setup

### Prerequisites
- Python 3.6+ (compatible with Django 3.0.5)
- pip (Python package manager)
- Virtual environment tool (virtualenv/venv)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/whiletrace/pug-or-ugh-apiv1.git
   cd pug-or-ugh-apiv1
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Load sample data (optional):**
   ```bash
   python manage.py loaddata pugorugh/fixtures/dogs.json
   ```
   Or use the data import script:
   ```bash
   python pugorugh/scripts/data_import.py
   ```

6. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   - Frontend: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/
   - API endpoints: http://127.0.0.1:8000/api/

## API Documentation

### Authentication
- **Method**: Token Authentication
- **Login**: `POST /api/user/login/` (returns auth token)
- **Registration**: `POST /api/user/`

### Core Endpoints

#### User Management
- `POST /api/user/` - User registration
- `POST /api/user/login/` - User authentication (get token)

#### Dog Browsing
- `GET /api/dog/<pk>/liked/next/` - Get next liked dog
- `GET /api/dog/<pk>/disliked/next/` - Get next disliked dog
- `GET /api/dog/<pk>/undecided/next/` - Get next undecided dog

#### Dog Status Updates
- `PUT /api/dog/<pk>/liked/` - Mark dog as liked
- `PUT /api/dog/<pk>/disliked/` - Mark dog as disliked
- `PUT /api/dog/<pk>/undecided/` - Mark dog as undecided

#### User Preferences
- `GET /api/user/preferences/` - Get user preferences
- `PUT /api/user/preferences/` - Update user preferences

### Request/Response Formats

#### Dog Response
```json
{
  "id": 1,
  "name": "Francesca",
  "image_filename": "1.jpg",
  "breed": "Labrador",
  "age": 72,
  "gender": "f",
  "size": "l"
}
```

#### User Preferences
```json
{
  "age": "b,y,a",
  "gender": "m,f",
  "size": "s,m,l"
}
```

## Project Structure

```
pug-or-ugh-apiv1/
├── backend/                 # Django project configuration
│   ├── settings.py         # Main Django settings
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI application entry point
├── pugorugh/              # Main Django application
│   ├── models.py          # Database models (Dog, UserDog, UserPref)
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views and business logic
│   ├── urls.py            # Application URL patterns
│   ├── signals.py         # Django signals
│   ├── converter.py       # Custom URL converter
│   ├── fixtures/          # Sample data
│   ├── static/            # Frontend assets
│   └── templates/         # HTML templates
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Database Models

### Dog Model
- `name`: CharField (max 50 chars)
- `image_filename`: CharField (max 100 chars)
- `breed`: CharField (max 50 chars)
- `age`: IntegerField (age in months)
- `gender`: CharField with choices (m/f/u)
- `size`: CharField with choices (s/m/l/xl/u)

### UserDog Model (Many-to-Many through model)
- `user`: ForeignKey to User
- `dog`: ForeignKey to Dog
- `status`: CharField (l/d/u for liked/disliked/undecided)

### UserPref Model
- `user`: ForeignKey to User
- `age`: CharField (comma-separated: b,y,a,s)
- `gender`: CharField (comma-separated: m,f,u)
- `size`: CharField (comma-separated: s,m,l,xl,u)

## Dog Categories

### Age Categories
- **Baby**: 1-18 months
- **Young**: 19-36 months
- **Adult**: 37-56 months
- **Senior**: 57+ months

### Size Categories
- **Small** (s)
- **Medium** (m)
- **Large** (l)
- **Extra Large** (xl)
- **Unknown** (u)

### Gender Options
- **Male** (m)
- **Female** (f)
- **Unknown** (u)

## Development

### Running Tests
```bash
python manage.py test
```

### Code Coverage
```bash
coverage run --source='.' manage.py test
coverage report
```

### Code Formatting
```bash
autopep8 --in-place --aggressive --aggressive <filename>
```

## Dependencies

### Core Dependencies
- Django==3.0.5
- djangorestframework==3.11.0
- requests==2.23.0

### Development Dependencies
- django-debug-toolbar==2.2
- coverage==5.0.4
- autopep8==1.5

### Frontend Dependencies
- React 0.14.7
- jQuery (for DOM manipulation)

## Configuration

### Environment Variables
Currently uses hardcoded settings. For production deployment, consider:
- Database configuration
- Secret key management
- Debug mode settings
- Allowed hosts configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure functionality
5. Submit a pull request

## License

This project is available under standard open source license terms.

## Author

Trace Harris

---

*A full-stack dog adoption application demonstrating Django REST Framework, React integration, and modern web development practices.*