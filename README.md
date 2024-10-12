Клонируйте репозиторий:

git clone https://github.com/ftox121/crud_fastapi.git
cd gudel_test
Создайте виртуальное окружение:

python -m venv venv
source venv/bin/activate  # Для Windows используйте venv\Scripts\activate

Установите зависимости:

pip install -r requirements.txt
Настройте базу данных:

Убедитесь, что у вас установлен PostgreSQL и настроен правильно. Создайте базу данных, если она еще не создана.

psql -U ваш_пользователь
CREATE DATABASE имя_базы_данных;
Настройте переменные окружения:

Создайте файл .env в корневом каталоге вашего проекта и добавьте необходимые переменные. Например:

DATABASE_URL=postgresql://ваш_пользователь:ваш_пароль@localhost:5432/имя_базы_данных
Запуск проекта
Для запуска проекта используйте следующую команду:

uvicorn main:app --reload
