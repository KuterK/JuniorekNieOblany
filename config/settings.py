import os
from pathlib import Path
from urllib.parse import urlparse

import sentry_sdk
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Environment(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )

    secret_key: str = Field(
        default="dev-only-insecure-key",
        validation_alias=AliasChoices("DJANGO_SECRET_KEY", "SECRET_KEY"),
    )
    debug: bool = Field(default=False, validation_alias="DJANGO_DEBUG")
    allowed_hosts: str = Field(
        default="localhost,127.0.0.1", validation_alias="DJANGO_ALLOWED_HOSTS"
    )
    database_url: str = Field(
        default="postgresql://juniorek:juniorek@localhost:5432/juniorek",
        validation_alias="DATABASE_URL",
    )
    redis_url: str = Field(default="redis://localhost:6379/0", validation_alias="REDIS_URL")
    cache_redis_url: str = Field(
        default="redis://localhost:6379/1", validation_alias="CACHE_REDIS_URL"
    )
    sentry_dsn: str = Field(default="", validation_alias="SENTRY_DSN")


env = Environment()
SECRET_KEY = env.secret_key
DEBUG = env.debug
ALLOWED_HOSTS = [host.strip() for host in env.allowed_hosts.split(",") if host.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_htmx",
    "analyses",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


def parse_database_url(url: str) -> dict[str, str | int]:
    parsed = urlparse(url)
    if parsed.scheme == "sqlite":
        name = parsed.path.lstrip("/") or ":memory:"
        return {"ENGINE": "django.db.backends.sqlite3", "NAME": name}
    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": parsed.path.lstrip("/"),
        "USER": parsed.username or "",
        "PASSWORD": parsed.password or "",
        "HOST": parsed.hostname or "",
        "PORT": str(parsed.port or 5432),
        "CONN_MAX_AGE": 60,
    }


DATABASES = {"default": parse_database_url(env.database_url)}
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env.cache_redis_url,
        "KEY_PREFIX": "juniorek",
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE = "pl"
TIME_ZONE = "Europe/Warsaw"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "analysis-list"
LOGOUT_REDIRECT_URL = "login"
CELERY_BROKER_URL = env.redis_url
CELERY_RESULT_BACKEND = env.redis_url
CELERY_TASK_TIME_LIMIT = 15
CELERY_TASK_SOFT_TIME_LIMIT = 13
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_ALWAYS_EAGER = os.getenv("CELERY_TASK_ALWAYS_EAGER", "").lower() == "true"

if env.sentry_dsn:
    sentry_sdk.init(
        dsn=env.sentry_dsn,
        send_default_pii=False,
        traces_sample_rate=0.1,
    )
