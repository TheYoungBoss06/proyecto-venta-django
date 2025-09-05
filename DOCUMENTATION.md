# Documentación del Proyecto: Tienda de Muebles

## Saludo
Hola, mi nombre es Wilson Espinal y esto es un proyecto de entrega para Infotep al profesor Elvis Garcia.

## 1. Descripción del Proyecto
Este proyecto es una aplicación web de comercio electrónico desarrollada con Django, diseñada para la venta de muebles. Incluye funcionalidades para la gestión de productos, carritos de compras, promociones, pedidos, facturación y un sistema de despacho.

## 2. Características Principales
*   **Gestión de Usuarios:** Registro, inicio de sesión y cierre de sesión.
*   **Catálogo de Productos:** Visualización de productos por categorías, detalles de productos y búsqueda.
*   **Carrito de Compras:** Añadir, ver y eliminar productos del carrito.
*   **Promociones y Cupones:** Aplicación de descuentos con un límite del 20%.
*   **Proceso de Pago:** Integración con pasarela de pago, (aunque se puede adaptar).
*   **Gestión de Pedidos:** Creación de órdenes, seguimiento de estado (PROCESANDO, DESPACHADO).
*   **Facturación:** Generación y visualización de facturas.
*   **Panel de Almacén:** Listado y despacho de órdenes para personal autorizado.
*   **Blog:** Sección para publicaciones de blog.

## 3. Tecnologías Utilizadas
*   **Backend:** Python, Django (Framework web)
*   **Base de Datos:** SQLite (por defecto, configurable a PostgreSQL)
*   **Frontend:** HTML, CSS (Bootstrap), JavaScript, jQuery
*   **Control de Versiones:** Git

## 4. Requisitos Previos
Antes de instalar y ejecutar el proyecto, asegúrate de tener lo siguiente instalado en tu sistema:

*   **Python 3.x:** Se recomienda Python 3.8 o superior.
*   **pip:** El gestor de paquetes de Python (normalmente viene con Python).
*   **Git:** Para clonar el repositorio.

## 5. Instalación del Proyecto

Sigue estos pasos para configurar el proyecto en tu entorno local:

1.  **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/TheYoungBoss06/proyecto-venta-django.git
    cd proyecto-venta-django
    ```

2.  **Crear y Activar un Entorno Virtual:**
    Es una buena práctica usar entornos virtuales para aislar las dependencias del proyecto.
    ```bash
    python -m venv entornovirtual
    # En Windows:
    .\entornovirtual\Scripts\activate
    # En macOS/Linux:
    source entornovirtual/bin/activate
    ```

3.  **Instalar Dependencias:**
    Instala todas las librerías necesarias listadas en `requirements.txt` (si existe, de lo contrario, instala Django y otras manualmente). Asumo que no hay un `requirements.txt` por lo que instalaré las que se ven en el `environment_details`.
    ```bash
    pip install Django==5.2.5 asgiref==3.9.1 sqlparse==0.5.3
    ```
    *(Nota: Si hay un archivo `requirements.txt` en el proyecto, el comando sería `pip install -r requirements.txt`)*

4.  **Configurar la Base de Datos:**
    El proyecto utiliza SQLite por defecto. Necesitas aplicar las migraciones para crear las tablas de la base de datos.
    ```bash
    python manage.py migrate
    ```

5.  **Crear un Superusuario (Administrador):**
    Esto te permitirá acceder al panel de administración de Django.
    ```bash
    python manage.py createsuperuser
    ```
    Sigue las instrucciones para crear un nombre de usuario, correo electrónico y contraseña.

## 6. Ejecución del Proyecto

Una vez que el proyecto esté instalado y configurado, puedes ejecutar el servidor de desarrollo:

```bash
python manage.py runserver
```

El servidor estará disponible en `http://127.0.0.1:8000/`.

## 7. Estructura del Proyecto (Resumen)

*   `furniture/`: Directorio principal del proyecto Django (configuración global).
    *   `settings.py`: Configuración del proyecto (base de datos, aplicaciones, plantillas, etc.).
    *   `urls.py`: Rutas URL principales del proyecto.
*   `myapp/`: Aplicación principal de Django.
    *   `models.py`: Definición de los modelos de la base de datos.
    *   `views.py`: Lógica de las vistas (manejo de solicitudes HTTP).
    *   `urls.py`: Rutas URL específicas de la aplicación `myapp`.
    *   `forms.py`: Formularios de Django.
*   `template/`: Contiene las plantillas HTML del proyecto.
    *   `base.html`: Plantilla base para la estructura común de las páginas.
    *   `index.html`, `product.html`, `shop-cart.html`, etc.: Plantillas específicas de cada página.
*   `static/`: Contiene archivos estáticos (CSS, JavaScript, imágenes).
*   `media/`: Contiene archivos multimedia subidos por los usuarios (imágenes de productos, etc.).
*   `db.sqlite3`: Archivo de la base de datos SQLite (generado después de las migraciones).
*   `manage.py`: Utilidad de línea de comandos para tareas administrativas de Django.
*   `README.md`: Información general del proyecto.
*   `DOCUMENTATION.md`: Este archivo de documentación.
