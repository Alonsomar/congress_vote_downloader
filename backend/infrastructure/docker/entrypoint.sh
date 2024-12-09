#!/bin/bash

# Esperar a que MongoDB esté disponible
echo "Esperando a MongoDB..."
while ! nc -z mongo 27017; do
    sleep 1
done
echo "MongoDB está disponible"

# Aplicar migraciones
echo "Aplicando migraciones..."
python manage.py migrate --noinput

# Iniciar el servidor
echo "Iniciando servidor..."
exec python manage.py runserver 0.0.0.0:8000 