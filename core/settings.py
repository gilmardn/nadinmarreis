from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'
LINHAS_POR_PAGINA = os.getenv('LINHAS_POR_PAGINA')


#SECRET_KEY = 'django-insecure-2)p^pk40f0me5lu0jl_6n=t8547enviomgbv2nxn0odq&in1mf'
#DEBUG = True  # Em produção  =  True
#LINHAS_POR_PAGINA = 14

ALLOWED_HOSTS = ['*',]

# minhas variaveis



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "crispy_forms",
    "crispy_bootstrap5",
    'socios',
    'financas',
    'usuarios',
    'relatorios',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]



# Internationalization

LANGUAGE_CODE = 'pt-br'           # Idioma padrão: português do Brasil
USE_TZ = False                    # Desabilita o uso de fusos horários
TIME_ZONE = 'America/Sao_Paulo'   # Fuso horário padrão: Brasília
USE_I18N = True                   # Habilita internacionalização (i18n)
USE_L10N = True                 # Desabilita a localização automática para usar os formatos acima




STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'templates/static'),)
STATIC_ROOT = os.path.join('static')
MEDIA_URL = '/media/'  # URL para acessar as imagens
MEDIA_ROOT = os.path.join(BASE_DIR, 'templates/media')  # Diretório onde as imagens serão salvas
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'usuarios.Usuario'
LOGIN_REDIRECT_URL = 'home'

LOGIN_URL = 'login'  # URL da view de login
LOGIN_REDIRECT_URL = 'home'  # URL para redirecionar após o login


# Messages
from django.contrib.messages import constants
MESSAGE_TAGS = {
    constants.DEBUG: 'alert-primary',
    constants.ERROR: 'alert-danger',
    constants.SUCCESS: 'alert-success',
    constants.INFO: 'alert-info',
    constants.WARNING: 'alert-warning',
}