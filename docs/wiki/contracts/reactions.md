# Контракт приложения `reactions` (view -> шаблон)

Namespace `reactions`, подключено как `path("reactions/", include("reactions.urls"))`.
Своей страницы нет - виджет (кнопки-реакции + счётчики) внутри поста и комментария.

---

## Поставить/сменить/убрать реакцию на пост

- **URL:** /reactions/post/<int:post_pk>/
- **View:** reactions.views.react_to_post
- **Метод:** POST (поле reaction_type - целое, код типа)
- **Доступ:** login_required (аноним -> редирект на LOGIN_URL)

### Действия
- Нет реакции юзера на пост -> создаётся
- Есть с тем же reaction_type -> удаляется (снятие)
- Есть с другим reaction_type -> меняется тип
- Редирект на posts:detail

### Ошибки
- Пост не найден -> 404

---

## Поставить/сменить/убрать реакцию на комментарий

- **URL:** /reactions/comment/<int:comment_pk>/
- **View:** reactions.views.react_to_comment
- **Метод:** POST (поле reaction_type)
- **Доступ:** login_required
- Логика идентична реакции на пост; редирект на posts:detail поста комментария

---

## Типы реакций

| Код | Название |
| --- | --- |
| 0 | лайк |
| 1 | сердце |
| 2 | смех |
| 3 | вау |

## Виджет реакций

Inclusion tag `{% reaction_widget user post=post %}` или `{% reaction_widget user comment=comment %}`
(reactions/templatetags/reaction_tags.py, шаблон includes/reaction_widget.html).

| Аргумент | Тип | Описание |
| --- | --- | --- |
| user | User | текущий юзер - подсветка активной реакции; аноним видит счётчики без кнопок |
| post / comment | Post / Comment | цель реакций, передаётся ровно одна |

- Кнопка-эмодзи + счётчик; активная реакция подсвечена
- Клик -> POST reactions:react_post / react_comment (toggle)
- Используется: templates/posts/post_detail.html, templates/includes/comment_item.html
- В post_card не вставлен: include only не передаёт user

## Маршруты (namespace `reactions`)

| Имя | URL | View |
| --- | --- | --- |
| reactions:react_post | /reactions/post/<post_pk>/ | react_to_post |
| reactions:react_comment | /reactions/comment/<comment_pk>/ | react_to_comment |