# BACKEND - ANÁLISIS POLÍTICO DE CHILE

Este es un proyecto Django que proporciona una API REST para el análisis político de Chile, incluyendo información sobre diputados y proyectos de ley.

---

## REQUISITOS PREVIOS

- Python 3.11+
- MongoDB 4.4+
- Docker y Docker Compose (opcional)

---

## INICIO RÁPIDO

1. Clonar el repositorio y navegar al directorio:

    ```bash
    git clone [url-del-repo]
    cd backend
    ```

2. Crear y activar entorno virtual:

    ```bash
    python -m venv venv
    ```

    - **Windows:** `venv\Scripts\activate`
    - **Unix/MacOS:** `source venv/bin/activate`

3. Instalar dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. Configurar variables de entorno:

    - Copiar `infrastructure/env/example.env` a `infrastructure/env/dev.env`
    - Editar `dev.env` con las configuraciones necesarias

5. Ejecutar migraciones:

    ```bash
    python manage.py migrate
    ```

6. Crear superusuario:

    ```bash
    python manage.py createsuperuser
    ```

7. Iniciar servidor:

    ```bash
    python manage.py runserver
    ```

---

## USANDO DOCKER

1. Construir y ejecutar con docker-compose:

    ```bash
    docker-compose up -d
    ```

2. Verificar la instalación:

    ```bash
    curl http://localhost:8000/api/
    ```

---

## ENDPOINTS PRINCIPALES

### Diputados:

- **GET** `/api/diputados/`  
  **Parámetros:** `page`, `page_size`, `nombre`, `sexo`

- **GET** `/api/diputados/<dipid>/`

### Proyectos:

- **GET** `/api/proyectos/`  
  **Parámetros:** `page`, `page_size`

- **GET** `/api/proyectos/<boletin>/`

- **POST** `/api/proyectos/search/`  
  **Body:** `titulo`, `estado`, `fecha_desde`, `fecha_hasta`, `materias[]`, `autores[]`

---

## ESTRUCTURA DEL PROYECTO
```plaintext
backend/
├── political_analysis_api/
│   ├── api/
│   │   ├── views/
│   │   ├── serializers/
│   │   ├── utils/
│   │   └── urls.py
│   ├── settings.py
│   └── urls.py
├── requirements.txt
└── manage.py
```


---

## CONFIGURACIÓN DEL ENTORNO
```env
MONGO_URI=mongodb://root:example@mongo:27017/
DB_NAME=votaciones_chile
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## DEPENDENCIAS PRINCIPALES
```plaintext
asgiref==3.8.1
Django==5.1.4
django-cors-headers==4.6.0
django-redis==5.4.0
djangorestframework==3.15.2
dnspython==2.7.0
pymongo==4.10.1
python-dotenv==1.0.1
redis==5.2.1
```

---

## MONITOREO Y SOLUCIÓN DE PROBLEMAS

### Logs:

- **Desarrollo:** Consola de Django
- **Docker:** `docker-compose logs -f backend`

### Comandos útiles:

- Ver estado:  
  ```bash
  docker-compose ps
  ```

- Reiniciar backend:  
  ```bash
  docker-compose restart backend
  ```

- Ver logs:  
  ```bash
  docker-compose logs backend
  ```

---

## PROBLEMAS COMUNES

- **Error MongoDB:** Verificar conexión al puerto `27017` y credenciales
- **Error CORS:** Revisar `ALLOWED_HOSTS` en `settings.py`
- **Error de permisos:** Verificar usuario y permisos de archivos

---

## CONTRIBUCIÓN

1. Crear rama `feature/`
2. Realizar cambios
3. Ejecutar pruebas
4. Crear Pull Request

---

## LICENCIA

[LICENCIA]

---

## CONTACTO

[Tu información de contacto]

---

## NOTAS ADICIONALES

- La API utiliza paginación por defecto (50 items por página)
- Todas las respuestas están en formato JSON
- La documentación completa está disponible en `/docs/`
- La interfaz de administración está en `/admin/`
- Para más detalles sobre la implementación y uso, consultar la documentación en `/docs/` o contactar al equipo de desarrollo.
