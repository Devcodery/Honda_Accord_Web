# 🚗 Honda Accord (2003 - 2005) - Web App ESM

Aplicación web moderna autónoma para consultar el **Manual Electrónico de Servicio (ESM)** del Honda Accord (años 2003, 2004 y 2005).

Diseñada con estilo **Neumorfismo (Soft UI)**, navegación 100% integrada (cero pestañas sueltas ni ventanas emergentes), buscador global en tiempo real y visor interactivo de esquemas con zoom.

---

## 🚀 Opciones de Despliegue

### Opción 1: Ejecución Rápida con Python (Sin instalar nada)
No requiere Docker ni servidores externos. Solo necesitas Python 3 (ya viene en la mayoría de sistemas Linux/Mac):

```bash
cd /ruta/a/Honda_Accord_Web
python3 server.py
```
Por defecto escuchará en el puerto `8080`. Puedes especificar un puerto o IP si lo deseas:
```bash
python3 server.py --port 9000
```
La consola te mostrará tanto la dirección local (`http://localhost:8080`) como la IP para conectarte desde tu teléfono móvil o tablet en la misma red Wi-Fi.

---

### Opción 2: Despliegue con Docker / Docker Compose (Recomendada para Servidores)
Ideal para desplegar en tu servidor casero, VPS, Raspberry Pi, Synology NAS o Unraid:

```bash
cd /ruta/a/Honda_Accord_Web
docker compose up -d
```
¡Y listo! El contenedor compilará una imagen ultra ligera de Nginx Alpine (~20 MB) y expondrá el manual en el puerto `8080`.

Para detener el servicio:
```bash
docker compose down
```

---

### Opción 3: Servidor Web Existente (Nginx / Apache / Caddy)
Si ya cuentas con un servidor web Nginx o Apache en tu servidor:
1. Copia el contenido de esta carpeta a tu directorio web (ej. `/var/www/honda_manual`).
2. Configura tu virtual host usando como referencia el archivo [`nginx.conf`](./nginx.conf) provisto.

---

## ✨ Características de la Aplicación

- **Estilo Neumórfico (Soft UI):** Sombras duales extruidas e invertidas, tarjetas limpias y modo oscuro completo para el taller.
- **Navegación Unificada sin Pestañas:**
  - Todos los enlaces internos entre procedimientos se cargan directamente en el visor integrado.
  - Al hacer clic en esquemas o ilustraciones, se abre un **Lightbox Modal** interactivo con zoom y arrastre (sin popups de 2004).
- **Buscador Reactivo:** Búsqueda en tiempo real sobre los más de 2.700 procedimientos y diagramas.
- **Selector Instantáneo:** Cambio entre Manual de Taller y Manual de Carrocería, y entre los años 2003, 2004 y 2005.
- **Favoritos e Historial:** Guarda tus procedimientos más consultados (pares de apriete, esquema de fusibles) en memoria local del navegador.
- **Diseño Responsive:** Adaptable a pantallas de escritorio, portátiles, tablets y móviles.
