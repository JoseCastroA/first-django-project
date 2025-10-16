# Django Blog - Dockerized Project

This is a fully dockerized Django project with PostgreSQL as the database.

## 📋 Prerequisites

- Docker installed on your system
- Docker Compose installed

## 🚀 How to Start the Project

### 1. Build and start the containers

```bash
docker-compose up --build
```

This command will:
- Build the Docker image
- Start PostgreSQL
- Run migrations
- Collect static files
- Start the Django server at http://localhost:8000

### 2. Access the application

Once the containers are running, access:
- **Application**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin

### 3. Create a superuser

To access the Django admin, you need to create a superuser:

```bash
docker-compose exec web python manage.py createsuperuser
```

## 🛠️ Useful Commands

### Stop the containers
```bash
docker-compose down
```

### Stop and remove volumes (including the database)
```bash
docker-compose down -v
```

### View logs
```bash
docker-compose logs -f
```

### Execute Django commands
```bash
docker-compose exec web python manage.py <command>
```

Examples:
```bash
# Create migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate

# Access Django shell
docker-compose exec web python manage.py shell
```

### Access PostgreSQL
```bash
docker-compose exec db psql -U blog_user -d blog_db
```

### Restart only the web service
```bash
docker-compose restart web
```

## 📁 Project Structure

```
blog/
├── blog/              # Django project configuration
├── manage.py          # Django management script
├── requirements.txt   # Python dependencies
├── Dockerfile         # Instructions to build the image
├── docker-compose.yml # Services configuration
├── .dockerignore      # Files to ignore in the image
└── .env.example       # Environment variables example
```

## 🔧 Environment Variables

Environment variables are defined in `docker-compose.yml`. For production, consider using a `.env` file:

```env
DEBUG=False
SECRET_KEY=your-very-secure-secret-key
ALLOWED_HOSTS=yourdomain.com
DATABASE_NAME=blog_db
DATABASE_USER=blog_user
DATABASE_PASSWORD=secure-password
DATABASE_HOST=db
DATABASE_PORT=5432
```

## 📝 Notes

- The PostgreSQL database persists in a Docker volume called `postgres_data`
- Static files are collected in the `static_volume` volume
- In development, code changes are automatically reflected thanks to the mounted volume

## 🐛 Troubleshooting

### Port 8000 is already in use
```bash
# Change the port in docker-compose.yml
ports:
  - "8080:8000"  # Use port 8080 instead of 8000
```

### Database errors
```bash
# Restart the database
docker-compose down -v
docker-compose up --build
```

### View detailed errors
```bash
docker-compose logs web
```
