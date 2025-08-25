#!/bin/bash

# Script de configuración para desarrollo local de ITICO
# Ejecutar con: chmod +x setup_dev.sh && ./setup_dev.sh

echo "🚀 Configurando entorno de desarrollo ITICO..."

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado. Por favor instálalo primero."
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv .venv
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source .venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "⚙️ Creando archivo .env..."
    cp .env.example .env
    echo "✅ Archivo .env creado. Por favor configura las variables necesarias."
else
    echo "ℹ️ Archivo .env ya existe."
fi

# Ejecutar migraciones
echo "🗄️ Ejecutando migraciones..."
python manage.py migrate

# Crear directorio de logs
mkdir -p logs

# Recopilar archivos estáticos
echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ Configuración completada!"
echo ""
echo "🔧 Próximos pasos:"
echo "1. Configura las variables en el archivo .env"
echo "2. Crea un superusuario: python manage.py createsuperuser"
echo "3. Ejecuta el servidor: python manage.py runserver"
echo ""
echo "📋 Para Celery (en terminales separadas):"
echo "   Worker: celery -A itico worker --loglevel=info"
echo "   Beat: celery -A itico beat --loglevel=info"
echo ""
echo "🌐 Accede a la aplicación en: http://127.0.0.1:8000"
