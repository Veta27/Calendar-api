# Calendar-api

## Описание
Сервис для работы с Календарем с использованием Flask.

## Установка и запуск
Установите зависимости:
```bash
   pip install -r requirements.txt
   ```

1. **Клонируйте репозиторий**
   ```bash
   git clone <ссылка на репозиторий>
   cd calendarapi
   ```

2. **Создайте виртуальное окружение и активируйте его**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Windows используйте venv\Scripts\activate
   ```

3. **Установите зависимости**
   ```bash
   pip install Flask Flask-SQLAlchemy
   ```

4. **Запустите приложение**
   ```bash
   python app.py
   ```

   После запуска вы должны увидеть сообщение, что сервер работает на `http://127.0.0.1:5000/`.

## API

### 1. Список событий (GET)
- **URL:** `/api/v1/calendar`

### 2. Добавление события (POST)
- **URL:** `/api/v1/calendar`

### 3. Чтение события (GET)
- **URL:** `/api/v1/calendar/<eventid>

### 4. Обновление события (PUT)
- **URL:** `/api/v1/calendar/<event_id>`
  
- ### 5. Удаление события (DELETE)
- **URL:** `/api/v1/calendar/<event_id>`

## Ограничения
- Максимальная длина заголовка: 30 символов.
- Максимальная длина текста: 200 символов.
- Нельзя добавлять более одного события в день.
