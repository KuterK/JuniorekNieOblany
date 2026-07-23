FROM node:22.22-alpine AS assets
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install --no-audit --no-fund
COPY tailwind.config.js ./
COPY templates ./templates
COPY analyses ./analyses
COPY static/src ./static/src
RUN npm run css:build

FROM python:3.13.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip install --no-cache-dir uv==0.8.2
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .
COPY --from=assets /app/static/dist ./static/dist
RUN chmod +x docker-entrypoint.sh
EXPOSE 8000
