from waitress import serve
from core.wsgi import application

serve(application, listen='*:9090', threads=1)