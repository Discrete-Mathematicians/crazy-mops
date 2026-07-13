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

## Маршруты (namespace `reactions`)

| Имя | URL | View |
| --- | --- | --- |
| reactions:react_post | /reactions/post/<post_pk>/ | react_to_post |
| reactions:react_comment | /reactions/comment/<comment_pk>/ | react_to_comment |