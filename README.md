# 📊 Backend Progress Service

Servicio encargado de:
- Historial de ejercicios (records).
- Intentos (attempts) con tiempos, errores, min/max, etc.

Link del repositorio en GitHub: https://github.com/Creative-Craft-UPC/backend-progress-service

## Clonar el Repositorio

```bash
git clone https://github.com/Creative-Craft-UPC/backend-progress-service.git
cd social_fun
```

---

## 🧱 Stack

- Python 3.11
- FastAPI
- MongoDB (Motor)
- PyJWT
- Docker + Cloud Run
- python-dotenv

---

## 📁 Estructura básica

- `main.py` → punto de entrada FastAPI
- `routes/` → rutas HTTP
- `auth/internal_dep.py` → validación de token interno (JWT RS256)
- `requirements.txt` → dependencias de Python
- `Dockerfile` → build de imagen
- `schemas` → Esquemas principales del servicio 

---

## ⚙ Variables de entorno

```env
MONGODB_URI=mongodb+srv://...

PUBLIC_KEY_PATH=/app/secrets/bff_public.pem
```

## Ejecución:
### 🚀 Ejecutar en local (sin Docker)

1. Crear entorno virtual y activalo:

    python -m venv progressContext

    progressContext/Scripts/activate ---> Windows

    source progressContext/bin/activate ---> Linux/Mac

2. Instalar dependencias:

    pip install -r requirements.txt

3. Ejecutar:

    uvicorn main:app --reload --port 8004

### 🐳 Ejecutar con Docker
#### Build

    docker build -t backend-progress-service .

#### Run

    docker run -p 8004:8004 \
    -e MONGODB_URI=... \
    -e PUBLIC_KEY_PATH=/app/secrets/bff_public.pem \
    -v ./secrets:/app/secrets \
    backend-progress-service