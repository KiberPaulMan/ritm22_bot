#### Сборка и запуск контейнера из репозитория:
```python
   docker compose up -d
```

### Внутри контейнера:
#### Создание файла .env и копирование в него чувствительных данных в следующем формате:
```python
# TELEGRAM_BOT_TOKEN
BOT_TOKEN=**********

# ID_TELEGRAM_USERS
ANNA_TG_ID=**********
ALENA_TG_ID=**********
PAVEL_TG_ID=**********

# DATABASE SETTINGS
PG_HOST=**********
PG_DB=**********
PG_PORT=**********
PG_USER=**********
PG_PASSWORD=**********
```
