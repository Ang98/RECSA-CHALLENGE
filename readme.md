# RECSA Challenge - Medical Chatbot Assistant

Este proyecto consiste en un sistema completo (Full Stack) para la gestión de citas médicas asistida por Inteligencia Artificial. Utiliza un **Chatbot potenciado por OpenAI** capaz de agendar, modificar, listar y cancelar citas mediante lenguaje natural, interactuando directamente con una base de datos PostgreSQL.

## 🚀 Tecnologías

* **Backend:** Python, Django REST Framework, SimpleJWT.
* **AI:** OpenAI API (GPT-4o-mini/GPT-3.5) + Tool Calling.
* **Frontend:** React, TypeScript, Vite, TailwindCSS, TanStack Query.
* **Infraestructura:** Docker, Docker Compose, PostgreSQL, Redis, Celery.

## 📋 Pre-requisitos

Asegúrate de tener instalado en tu máquina:
* [Docker Engine](https://docs.docker.com/engine/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [Make](https://www.gnu.org/software/make/) (Opcional, pero recomendado para usar los comandos rápidos).

## ⚙️ Configuración de Entorno

Antes de iniciar, es necesario configurar la API Key de OpenAI para que el cerebro del Chatbot funcione.

1.  Ve a la carpeta de variables de entorno del backend (o donde hayas configurado `OPENAI_API_KEY`, usualmente en `.envs/.local/.django` o `settings.py`).
2.  Asegúrate de que la variable `OPENAI_API_KEY` esté definida con una clave válida que empiece por `sk-...`.

## 🛠️ Instalación y Despliegue

El proyecto incluye un `Makefile` para simplificar las tareas comunes. Sigue estos pasos en orden:

### 1. Construir los contenedores
Descarga las imágenes y compila el frontend y backend.
```bash
make build
```
### 2. Levantar la aplicación
Inicia todos los servicios (Django, Postgres, Redis, Frontend, Workers).
```bash
make run
```
Nota: La primera vez puede tardar unos segundos en iniciar la base de datos y aplicar migraciones.

### 3. Crear Usuario Administrador
Para acceder al sistema, necesitas crear un superusuario. Ejecuta el siguiente comando y sigue las instrucciones:
```bash
make createsuperuser
```

### Credenciales sugeridas para la prueba:
* **Username::** `admin`
* **Email::** `admin@recsa.com`
* **Password::** `recsa`


## 🖥️ Guía de Uso

Una vez levantado el sistema:

1.  **Frontend:** Abre tu navegador en [http://localhost:5173](http://localhost:5173).
2.  **Login:** Ingresa con las credenciales creadas en el paso anterior (`admin` / `recsa`).
3.  **Chatbot:** Interactúa con el asistente para gestionar citas.

### Ejemplos de Interacción (Prompts)

El bot es capaz de entender el contexto y manejar fechas relativas (mañana, el próximo lunes, etc.).

* **Crear Cita:**
    > "Hola, quiero agendar una cita para Juan Pérez mañana a las 10:00 AM por dolor de cabeza."

* **Listar Citas:**
    > "¿Qué citas tengo programadas?"
    > "¿Tengo citas para el 2025-12-01?"

* **Modificar Cita (Update):**
    > "Cambia la hora de la cita de Juan para las 2:00 PM."

* **Cancelar Cita:**
    > "Cancela la cita de Juan Pérez."

## 🔧 Comandos Útiles (Makefile)

| Comando | Descripción |
| :--- | :--- |
| `make build` | Construye las imágenes de Docker. |
| `make run` | Levanta todo el entorno en primer plano (logs visibles). |
| `make run-d` | Levanta el entorno en modo "detach" (segundo plano). |
| `make down` | Detiene y remueve los contenedores. |
| `make down-volumes` | **¡Cuidado!** Detiene todo y borra la base de datos (Volúmenes). |
| `make build-no-cache`| Reconstrucción forzada (útil si agregas librerías nuevas). |

---

## 🧪 Notas Técnicas

* **Arquitectura:** El frontend se comunica con el backend únicamente a través de API REST protegida con JWT.
* **OpenAI:** Se utiliza la capacidad de "Function Calling" (Tools) para que el modelo ejecute acciones reales en la base de datos de manera estructurada y segura.
* **CORS:** Configurado para aceptar peticiones desde `localhost:5173`.

---
**RECSA Challenge**