## Фудграм - Ваш гид в мире рецептов

Платформа для обмена кулинарными рецептами с возможностью планирования меню и составления списка покупок.

### 🌟 Ключевые функции
### 🛡️ Защищенная система доступа (регистрация, авторизация, смена пароля)

### ✍️ Полный цикл работы с рецептами (добавление, изменение, удаление)

### 🗂️ Система категоризации и тегирования контента

### 🛒 Автоматическое формирование списка необходимых ингредиентов

### ⭐ Возможность сохранять понравившиеся рецепты

### 👨‍🍳 Подписка на интересных авторов

### 📱 Полностью адаптивный веб-интерфейс

### ⚙️ Используемые технологии
Серверная часть
Компонент	Назначение
<img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" width=16> Python	Основной язык серверной разработки
<img src="https://www.djangoproject.com/m/img/logos/django-logo-positive.png" width=16> Django	Фреймворк для веб-разработки
DRF	REST API интерфейс
<img src="https://www.postgresql.org/media/img/about/press/elephant.png" width=16> PostgreSQL	Реляционная база данных
<img src="https://redis.io/images/redis-white.png" width=16> Redis	Брокер сообщений и кеширование
Celery	Обработка фоновых задач
Клиентская часть
Компонент	Назначение
<img src="https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg" width=16> React	Библиотека пользовательского интерфейса
Redux	Хранение состояния приложения
Material-UI	Готовые UI компоненты
Axios	Работа с HTTP запросами
🏁 Начало работы
Для разработки
Скопируйте проект:

```sh
git clone https://github.com/Nikkitos-AASD/foodgram-st.git && cd culinary-compass
```
Подготовьте окружение:

```sh
python3 -m venv env && source env/bin/activate  # Unix
py -m venv env && .\env\Scripts\activate  # Windows
```
Установите необходимые пакеты:

```sh
pip install -r requirements/development.txt
npm --prefix client install
```
Настройте окружение (.env):

```properties
APP_ENV=development
DATABASE_URL=postgres://user:pass@localhost:5432/dbname
```
Запустите серверы:

```sh
# Сервер API
python manage.py runserver

# Клиентское приложение
cd client && npm start
```
Развертывание в Docker
Соберите образы:

```sh
docker-compose -f docker-compose.prod.yml build
```
Запустите сервисы:

```sh
docker-compose -f docker-compose.prod.yml up -d
```
Примените миграции:

```sh
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```
Создайте администратора:

```sh
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```
Соберите статические файлы:

```sh
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```
## 📖 API Документация

Доступные форматы документации:

Интерактивная документация: /api/swagger/

Альтернативный формат: /api/redoc/

Пример запроса:

```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```