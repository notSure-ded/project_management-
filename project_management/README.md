# Project & Task Management Application

A Django-based project and task management application with REST API, Celery integration, and Django Admin customization.  
This application demonstrates professional Django practices including abstract base models, RESTful API design, background task processing, and containerized deployment.

---

## Table of Contents
- [Features](#features)  
- [Technology Stack](#technology-stack)  
- [Project Structure](#project-structure)  
- [Setup Instructions](#setup-instructions)  
- [Local Development](#local-development)  
- [Docker Deployment](#docker-deployment)  
- [API Documentation](#api-documentation)  
- [Authentication](#authentication)  
- [Project Endpoints](#project-endpoints)  
- [Development Task Endpoints](#development-task-endpoints)  
- [Design Task Endpoints](#design-task-endpoints)  
- [Testing](#testing)  
- [Usage Examples](#usage-examples)  
- [Contributing](#contributing)  

---

## Features
- **Abstract Base Models**: Reusable `TimeStampedModel` for common fields  
- **Project Management**: Create, read, update, and delete projects  
- **Task Management**: Two types of tasks (Development and Design) with custom fields  
- **RESTful API**: Full CRUD operations with filtering, searching, and pagination  
- **Background Tasks**: Celery integration for periodic tasks (marking overdue tasks)  
- **Django Admin**: Customized admin interface with inline task editing, filters, and bulk actions  
- **Signal Handlers**: Automated notifications for task creation  
- **Authentication**: JWT-based authentication for API access  
- **Sample Data**: Management command to populate the database with test data  
- **Containerization**: Docker Compose setup for easy deployment  
- **Comprehensive Testing**: Unit tests for models, API endpoints, and signal handlers  

---

## Technology Stack
- **Backend**: Django 4.1.7  
- **API Framework**: Django REST Framework 3.14.0  
- **Database**: PostgreSQL 17 
- **Task Queue**: Celery 5.2.7 with Redis  
- **Authentication**: Simple JWT  
- **Containerization**: Docker & Docker Compose  
- **Testing**: Django Test Framework  

---

## Project Structure
```
project_management/
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── management/
│   │   └── commands/
│   │       └── sample_data.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── models.py
│   ├── serializers.py
│   ├── signals.py
│   ├── tasks.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── project_management/
│   ├── __init__.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

---

## Setup Instructions

### Prerequisites
- Python 3.9+  
- PostgreSQL 13  
- Redis  
- Docker (optional)  
- Docker Compose (optional)  

---

## Local Development

```bash

git clone <repository-url>
cd project_management

python -m venv venv
source venv/bin/activate  
venv\Scripts\activate     


pip install -r requirements.txt
```

### Environment Variables  
Create a `.env` file in the project root:  

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=project_management
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
DEFAULT_FROM_EMAIL=noreply@example.com
```

### Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### Superuser
```bash
python manage.py createsuperuser
```

### Sample Data (Optional)
```bash
python manage.py sample_data
```

### Run Services
```bash
# Redis
redis-server

# Celery worker
celery -A project_management worker -l info

# Celery beat
celery -A project_management beat -l info

# Django server
python manage.py runserver
```

Access:  
- Web app: http://localhost:8000  
- Admin: http://localhost:8000/admin/  
- API: http://localhost:8000/api/  

---

## Docker Deployment
```bash
# Clone and run
git clone <repository-url>
cd project_management
docker-compose up --build
```

Run migrations:  
```bash
docker-compose exec web python manage.py migrate
```

Create superuser (optional):  
```bash
docker-compose exec web python manage.py createsuperuser
```

Load sample data (optional):  
```bash
docker-compose exec web python manage.py sample_data
```

Access:  
- Web app: http://localhost:8000  
- Admin: http://localhost:8000/admin/  
- API: http://localhost:8000/api/  

---

## API Documentation

### Authentication
- Obtain token: `POST /api/token/`  
- Refresh token: `POST /api/token/refresh/`  

Header:  
```
Authorization: Bearer your_access_token
```

### Project Endpoints
- List Projects: `GET /api/projects/`  
- Create Project: `POST /api/projects/`  
- Retrieve Project: `GET /api/projects/{id}/`  
- Update Project: `PUT /api/projects/{id}/`  
- Delete Project: `DELETE /api/projects/{id}/`  

### Development Task Endpoints
- List Tasks: `GET /api/development-tasks/`  
- Create Task: `POST /api/development-tasks/`  
- Retrieve Task: `GET /api/development-tasks/{id}/`  
- Update Task: `PUT /api/development-tasks/{id}/`  
- Delete Task: `DELETE /api/development-tasks/{id}/`  

Query params:  
`status, due_date, due_date__gte, due_date__lte, project, search, ordering`  

### Design Task Endpoints
- List Tasks: `GET /api/design-tasks/`  
- Create Task: `POST /api/design-tasks/`  
- Retrieve Task: `GET /api/design-tasks/{id}/`  
- Update Task: `PUT /api/design-tasks/{id}/`  
- Delete Task: `DELETE /api/design-tasks/{id}/`  

---

## Testing
Run tests:  
```bash
python manage.py test
```

Coverage includes:  
- Models  
- API endpoints  
- Signals  
- Celery tasks  

---

## Usage Examples

### curl
```bash
# Get a token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# List projects
curl -X GET http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer your_access_token"
```

### Postman
- Set `base_url=http://localhost:8000/api`  
- Login request sets `access_token`  
- Use Bearer Token for project and task requests  

---

## Contributing
- Fork repository  
- Create feature branch  
- Add changes + tests  
- Run tests: `python manage.py test`  
- Commit + push  
- Open PR  

