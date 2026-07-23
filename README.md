# JuniorekNieOblany

Aplikacja edukacyjna do analizy fragmentów kodu przez AI i budowania prywatnej
biblioteki wiedzy. Implementacja jest oparta na Django Templates, HTMX,
PostgreSQL, Celery i Redis.

## Uruchomienie lokalne

Wymagane: Python 3.13.11, `uv`, Node.js 22 oraz Docker.

```bash
copy .env.example .env
docker compose up -d postgres redis
uv sync
npm install
npm run css:build
uv run python manage.py migrate
uv run python manage.py runserver
```

W drugim terminalu uruchom worker:

```bash
uv run celery -A config worker --loglevel=info
```

Uzupełnij `OPENAI_API_KEY` w `.env`. Domyślna konfiguracja używa jednego modelu
przez zgodne z OpenAI API OpenRouter. Klucz i przesyłany kod nie są logowane.

## Kontenery

```bash
docker compose up --build
```

Aplikacja będzie dostępna przez Caddy pod `http://localhost`.

## Kontrole jakości

```bash
uv run ruff check .
uv run pytest
uv run mypy .
```

Testy nie wywołują prawdziwego API LLM — integracja jest mockowana.
