# Usa una imagen base de Python
FROM python:3.10-alpine

# Establecer el directorio de trabajo en el contenedor
WORKDIR /workspace

# Copiar los archivos del proyecto al contenedor
#COPY . /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que el servicio escuchará (si se necesita)
EXPOSE 8000

# Comando para correr el servicio
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
