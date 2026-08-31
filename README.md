<div align="center">

  <h1>🚀 Proyecta Fintech</h1>
  <p><strong>El sistema inteligente para la gestión y control de tus finanzas personales</strong></p>
  <p>Basado en la regla de oro: <i>50% Esenciales, 30% No Esenciales, 20% Ahorro e Inversión</i>.</p>
  
  <br />
  
  [![Python Version](https://img.shields.io/badge/Python-3.14+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![Django](https://img.shields.io/badge/Django-6.1-092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
  [![Bootstrap](https://img.shields.io/badge/Bootstrap_5-7952B3.svg?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)

</div>

<hr />

## ✨ ¿Qué es Proyecta Fintech?
Proyecta Fintech es una plataforma web moderna diseñada para tomar el control absoluto de tu dinero. Destaca por su interfaz atractiva *(Glassmorphism)* con **Modo Oscuro/Claro inteligente** y una organización de gastos enfocada en prevenir el sobreendeudamiento y erradicar los *gastos hormiga*.

### 💎 Funcionalidades
- 📊 **Dashboard Interactivo:** Monitoreo mensual de ingresos, gastos, ahorros y créditos en tiempo real.
- 🐜 **Caza-Hormigas:** Control del presupuesto de gastos pequeños e imperceptibles (Límite dinámico del 5% de tus ingresos).
- ⚖️ **Regla 50-30-20:** Distribución automática del dinero para priorizar calidad de vida y ahorro.
- 🌍 **Multi-Moneda Dinámica:** Configuración de perfil (USD, EUR, COP) que ajusta toda tu contabilidad al instante.
- 🌙 **Modo Oscuro/Claro:** Adaptación total de la interfaz a tus preferencias visuales.

<br>

---

## 🛠️ Requisitos Previos (Pre-requisitos)
Antes de comenzar, asegúrate de tener instalados los siguientes programas en tu computadora:

1. 🐍 **Python 3.10 o superior**: [Descargar aquí](https://www.python.org/downloads/) *(Recuerda marcar la casilla "Add Python to PATH" durante la instalación).*
2. 🐘 **PostgreSQL**: [Descargar aquí](https://www.postgresql.org/download/) *(El gestor de base de datos).*
3. 🐙 **Git**: [Descargar aquí](https://git-scm.com/downloads/) *(Opcional, para clonar el repositorio).*

<br>

---

## 🚀 Instalación y Despliegue Local

Sigue estos sencillos pasos para levantar el servidor en tu propia máquina:

### 1. Clonar el Repositorio
Abre tu terminal (Símbolo del sistema, PowerShell o Git Bash) y ejecuta:
```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
```
*(Si descargaste el archivo .zip, simplemente descomprímelo y abre tu terminal dentro de la carpeta principal).*

### 2. Configurar la Base de Datos (PostgreSQL)
Abre *pgAdmin* (o la consola de PostgreSQL) y crea una base de datos con los siguientes datos:
- **Nombre de la base de datos:** `bd_contadora`
- **Usuario:** `postgres`
- **Contraseña:** `Teojhoanig12*` *(Asegúrate de que coincida con tus variables, o actualízala en el archivo `settings.py`).*

### 3. Crear y Activar el Entorno Virtual
Para no mezclar las dependencias de este proyecto con tu sistema operativo, creamos un entorno virtual:

**En Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**En Mac / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```
*(Verás que la terminal ahora inicia con un `(venv)`).*

### 4. Instalar las Dependencias
Con el entorno virtual activado, instala todas las librerías necesarias ejecutando:
```bash
pip install -r requirements.txt
```

### 5. Migraciones de la Base de Datos
Prepara y construye las tablas en tu base de datos PostgreSQL:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. ¡Encender el Servidor! 🔥
Finalmente, arranca la plataforma con:
```bash
python manage.py runserver
```

<br>

<div align="center">
  <h3>¡Todo Listo! 🎉</h3>
  <p>Abre tu navegador favorito y dirígete a:</p>
  <code>👉 http://localhost:8000/ o http://127.0.0.1:8000/</code>
</div>

---

<div align="center">
  <p>Construido con ❤️ para mejorar la salud financiera de todos.</p>
</div>
