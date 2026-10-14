#!/usr/bin/env python3
"""
Servidor HTTP seguro y autónomo para Honda Accord Web ESM
Diseñado conforme a estándares de seguridad OWASP y mejores prácticas CIS.
Sin dependencias externas.
"""
import http.server
import socketserver
import socket
import os
import sys
import argparse
import urllib.parse

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Lista negra de archivos y carpetas sensibles del sistema que nunca deben servirse
BLOCKED_EXACT_FILES = {
    "server.py",
    "dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "nginx.conf",
    "readme.md",
    ".dockerignore",
    ".gitignore",
}

class ESMHandler(http.server.SimpleHTTPRequestHandler):
    server_version = "HondaESM"
    sys_version = ""
    timeout = 15

    def version_string(self):
        return "HondaESM"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Silenciar peticiones rutinarias de imágenes/scripts para mantener limpia la consola
        if " 200 " not in str(args):
            super().log_message(format, *args)

    def is_path_safe(self, path):
        """Verifica que la ruta no acceda a archivos ocultos, traversal o archivos del servidor"""
        decoded_path = urllib.parse.unquote(path.split('?')[0].split('#')[0])
        parts = decoded_path.replace('\\', '/').split('/')
        
        # Bloquear cualquier segmento que comience con '.' (como .git, .env, ..)
        for part in parts:
            if part.startswith('.') and part not in ('', '.'):
                return False
            if part.lower() in BLOCKED_EXACT_FILES:
                return False

        # Verificar resolución canónica dentro de DIRECTORY
        translated = self.translate_path(self.path)
        real_translated = os.path.realpath(translated)
        real_directory = os.path.realpath(DIRECTORY)
        if not real_translated.startswith(real_directory):
            return False

        # Bloquear si apunta a un archivo bloqueado por su nombre real en disco
        basename = os.path.basename(real_translated).lower()
        if basename in BLOCKED_EXACT_FILES or basename.startswith('.'):
            return False

        return True

    def do_GET(self):
        if not self.is_path_safe(self.path):
            self.send_error(404, "Recurso no encontrado")
            return
        super().do_GET()

    def do_HEAD(self):
        if not self.is_path_safe(self.path):
            self.send_error(404, "Recurso no encontrado")
            return
        super().do_HEAD()

    def do_POST(self):
        self.send_error(405, "Método no permitido")

    def do_PUT(self):
        self.send_error(405, "Método no permitido")

    def do_DELETE(self):
        self.send_error(405, "Método no permitido")

    def do_OPTIONS(self):
        self.send_error(405, "Método no permitido")

    def do_TRACE(self):
        self.send_error(405, "Método no permitido")

    def list_directory(self, path):
        # Deshabilitar por completo el listado de directorios (CWE-548)
        self.send_error(403, "Acceso al directorio denegado")
        return None

    def end_headers(self):
        # Cabeceras de seguridad HTTP robustas (OWASP Best Practices)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("X-XSS-Protection", "1; mode=block")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=()")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self'; frame-src 'self' about:; object-src 'none'; base-uri 'self';")
        super().end_headers()

    def guess_type(self, path):
        # Mapeo estricto de tipos MIME y codificación de caracteres
        if path.endswith(".json"):
            return "application/json; charset=utf-8"
        if path.endswith("index.html"):
            return "text/html; charset=utf-8"
        if path.endswith(".HTML") or path.endswith(".html"):
            return "text/html; charset=iso-8859-1"
        if path.endswith(".JS") or path.endswith(".js"):
            return "application/javascript; charset=iso-8859-1"
        if path.endswith(".PNG") or path.endswith(".png"):
            return "image/png"
        if path.endswith(".CSS") or path.endswith(".css"):
            return "text/css"
        return super().guess_type(path)

def get_local_ip():
    """Detecta la IP local en la red Wi-Fi o LAN para facilitar acceso desde móvil"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class ThreadingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

def main():
    parser = argparse.ArgumentParser(description="Servidor Seguro Honda Accord ESM Web")
    parser.add_argument("--port", "-p", type=int, default=8080, help="Puerto del servidor (default: 8080)")
    parser.add_argument("--host", "-H", type=str, default="0.0.0.0", help="Dirección de escucha (default: 0.0.0.0)")
    args = parser.parse_args()

    os.chdir(DIRECTORY)
    local_ip = get_local_ip()

    try:
        httpd = ThreadingServer((args.host, args.port), ESMHandler)
    except OSError as e:
        print(f"Error al abrir el puerto {args.port}: {e}")
        sys.exit(1)

    print("=" * 66)
    print("      HONDA ACCORD - MANUAL ELECTRÓNICO TÉCNICO (WEB APP)")
    print("      [SERVIDOR ENDURECIDO - ESTÁNDARES OWASP / CIS]")
    print("=" * 66)
    print(f"\n Servidor ejecutándose correctamente:")
    print(f" -> En esta máquina:       http://localhost:{args.port}/")
    if local_ip != "127.0.0.1":
        print(f" -> Desde tu móvil/tablet: http://{local_ip}:{args.port}/")
    print(f" -> En tu red/servidor:    http://{args.host}:{args.port}/\n")
    print(" Protección activa: Listado denegado, .git bloqueado, CSP y cabeceras OWASP.")
    print(" Presiona Ctrl + C para detener el servidor cuando termines.")
    print("=" * 66)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo el servidor de forma segura. ¡Hasta pronto!")
        httpd.server_close()
        sys.exit(0)

if __name__ == "__main__":
    main()
