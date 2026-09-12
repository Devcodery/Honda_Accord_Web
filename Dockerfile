FROM nginx:alpine

# Reemplazar configuración default
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar todos los datos de la aplicación y manuales
COPY . /usr/share/nginx/html/

# Eliminar archivos innecesarios dentro del contenedor web
RUN rm -f /usr/share/nginx/html/Dockerfile \
          /usr/share/nginx/html/docker-compose.yml \
          /usr/share/nginx/html/nginx.conf \
          /usr/share/nginx/html/server.py

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
