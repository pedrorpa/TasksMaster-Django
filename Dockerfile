# Define la imagen base de Python adecuada para tu proyecto Django
FROM python:3.10.6


RUN apt update && apt install -y python3 python3-pip
# Establece el directorio de trabajo dentro del contenedor
RUN mkdir /app
WORKDIR /app

# Copia el archivo de requisitos (requirements.txt) al contenedor
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos del proyecto al contenedor
COPY . .

# Expone el puerto 8000 para acceder a la aplicación Django
EXPOSE 8000

# Ejecuta el comando para iniciar el servidor web de Django
CMD ["python3", "manage.py","runserver","0.0.0.0:8000"]