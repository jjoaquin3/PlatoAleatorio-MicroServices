# Usar Python como base
FROM python:3.10-alpine

# Establecer el directorio de trabajo
WORKDIR /workspace

# Compiar init que inicializará la DB tablas y contenido
COPY init.py .
COPY requirements.txt .
COPY dataset/ ./dataset/
COPY scripts/ ./scripts/

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar el init.py
CMD ["python", "init.py"]
