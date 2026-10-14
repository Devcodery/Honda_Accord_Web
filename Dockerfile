FROM nginx:alpine

# Reemplazar configuración default por la versión endurecida con estándares OWASP
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar archivos estáticos de la aplicación (filtrados automáticamente por .dockerignore)
COPY . /usr/share/nginx/html/

# Capa de seguridad adicional: asegurar eliminación de cualquier archivo del sistema
RUN rm -rf /usr/share/nginx/html/.git \
           /usr/share/nginx/html/.dockerignore \
           /usr/share/nginx/html/.gitignore \
           /usr/share/nginx/html/Dockerfile \
           /usr/share/nginx/html/docker-compose.yml \
           /usr/share/nginx/html/docker-compose.yaml \
           /usr/share/nginx/html/nginx.conf \
           /usr/share/nginx/html/server.py \
           /usr/share/nginx/html/README.md

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
