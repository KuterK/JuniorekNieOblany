| Obszar          | Rekomendacja                                      |
| --------------- | ------------------------------------------------- |
| Runtime         | Python 3.13, przypięta wersja patch               |
| Framework       | Django 6.0, przypięta wersja patch                |
| UI              | Django Templates + HTMX                           |
| JavaScript      | Alpine.js tylko tam, gdzie HTMX nie wystarcza     |
| CSS             | Tailwind CSS                                      |
| Baza            | PostgreSQL + psycopg 3                            |
| AI              | SDK jednego dostawcy, jeden model dla MVP         |
| Struktura AI    | Pydantic + wersjonowany schemat                   |
| Zadania         | Celery                                            |
| Broker          | Redis                                             |
| Cache           | Redis z oddzielnym namespace’em lub bazą logiczną |
| Serwer          | Gunicorn                                          |
| Proxy           | Caddy                                             |
| Kontenery       | Docker Compose                                    |
| Zależności      | uv + `pyproject.toml` + lockfile                  |
| Testy           | pytest, pytest-django, testy z mockowanym API LLM |
| Jakość          | Ruff, mypy stopniowo, pre-commit                  |
| CI/CD           | GitHub Actions                                    |
| Błędy           | Sentry z filtrowaniem kodu i sekretów             |
| Metryki MVP     | PostgreSQL + logi + Sentry                        |
| Metryki później | Prometheus + Grafana                              |
