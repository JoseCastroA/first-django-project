# Usar Python 3.11 como imagen base
FROM python:3.11-slim

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el proyecto
COPY . /app/

# Crear directorio para archivos estáticos
RUN mkdir -p /app/staticfiles

# Exponer el puerto 8000
EXPOSE 8000

# Comando por defecto
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "blog.wsgi:application"]
