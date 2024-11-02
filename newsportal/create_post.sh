#!/bin/bash

# Переход в директорию проекта
cd "C:/Users/Константин/PycharmProjects/Project/NP" || exit

# Активация виртуального окружения
source .venv/Scripts/activate

# Запуск локального сервера в фоновом режиме
python manage.py runserver &

# Запуск Django Shell и выполнение команд
python manage.py shell <<EOF
from newsportal.models import Post, Category, Author

# Получаем или создаем автора
author, created = Author.objects.get_or_create(name_id=1)

# Получаем или создаем категорию
category, created = Category.objects.get_or_create(name="Новости")

# Создаем пост
post = Post.objects.create(
    author=author,
    type='NS',
    title="Тестовый пост из скрипта",
    content="Это текст для тестового поста, созданного из Bash-скрипта.",
    slug="test-post-from-script"
)

# Добавляем категорию к посту
post.category.add(category)

print("Пост успешно создан:", post)
EOF
