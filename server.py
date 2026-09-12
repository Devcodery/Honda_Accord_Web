#!/usr/bin/env python3
"""
Servidor HTTP autónomo para Honda Accord Web ESM
Listo para producción local o en servidor hogareño / VPS.
Sin dependencias externas.
"""
import http.server
import socketserver
import socket
import os
import sys
import argparse

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class ESMHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Silenciar peticiones rutinarias de imágenes/scripts para mantener limpia la consola
        if " 200 " not in str(args):
            super().log_message(format, *args)

    def end_headers(self):
        # Permitir CORS y deshabilitar restricciones de caché molestas
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Content-Type-Options", "nosniff")
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

def main():
    parser = argparse.ArgumentParser(description="Servidor Honda Accord ESM Web")
    parser.add_argument("--port", "-p", type=int, default=8080, help="Puerto del servidor (default: 8080)")
    parser.add_argument("--host", "-H", type=str, default="0.0.0.0", help="Dirección de escucha (default: 0.0.0.0)")
    args = parser.parse_args()

    os.chdir(DIRECTORY)
    local_ip = get_local_ip()

    class ThreadingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True

    try:
        httpd = ThreadingServer((args.host, args.port), ESMHandler)
    except OSError as e:
        print(f"Error al abrir el puerto {args.port}: {e}")
        sys.exit(1)

    print("=" * 66)
    print("      HONDA ACCORD - MANUAL ELECTRÓNICO TÉCNICO (WEB APP)")
    print("=" * 66)
    print(f"\n Servidor ejecutándose correctamente:")
    print(f" -> En esta máquina:       http://localhost:{args.port}/")
    if local_ip != "127.0.0.1":
        print(f" -> Desde tu móvil/tablet: http://{local_ip}:{args.port}/")
    print(f" -> En tu red/servidor:    http://{args.host}:{args.port}/\n")
    print(" Presiona Ctrl + C para detener el servidor cuando termines.")
    print("=" * 66)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo el servidor. ¡Hasta pronto!")
        httpd.server_close()
        sys.exit(0)

if __name__ == "__main__":
    main()
