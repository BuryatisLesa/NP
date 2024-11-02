from .models import *

author, created = Author.objects.get_or_create(name_id=1)
category, created = Category.objects.get_or_create(name="Новости")

post = Post.objects.create(
    author=author,
    type='NS',
    title="Тестовый пост из скрипта",
    content="Это текст для тестового поста, созданного из Bash-скрипта.",
    slug="test-post-from-script"
)
post.category.add(category)
print("Пост успешно создан:", post)
