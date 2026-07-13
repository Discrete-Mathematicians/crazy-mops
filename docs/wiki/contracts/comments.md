# Контракт приложения `comments` (view -> шаблон)

Namespace `comments`, подключено как `path("comments/", include("comments.urls"))`.
Комментарии к посту, с вложенными ответами (ответ на ответ - тоже допустим).
Права на удаление - по автору комментария или админ (не по владельцу поста).

---

## Добавить комментарий к посту

- **URL:** /comments/post/<int:post_pk>/new/
- **View:** comments.views.add_comment
- **Метод:** POST
- **Доступ:** login_required (аноним -> редирект на LOGIN_URL)

### Действия
- Пост post_pk не найден -> 404
- Форма CommentForm валидна -> создаётся Comment (post, user = request.user, reply_comment = None)
- Форма невалидна (пустой текст) -> комментарий не создаётся
- Редирект на posts:detail поста

---

## Ответить на комментарий

- **URL:** /comments/<int:comment_pk>/reply/
- **View:** comments.views.add_reply
- **Метод:** POST
- **Доступ:** login_required (аноним -> редирект на LOGIN_URL)

### Действия
- Комментарий comment_pk не найден -> 404
- Форма CommentForm валидна -> создаётся Comment (post = post родителя,
  user = request.user, reply_comment = родительский комментарий)
- Ответ на ответ работает так же - вложенность не ограничена
- Редирект на posts:detail поста родительского комментария

---

## Удалить комментарий

- **URL:** /comments/<int:comment_pk>/delete/
- **View:** comments.views.delete_comment
- **Метод:** POST
- **Доступ:** login_required (аноним -> редирект на LOGIN_URL)

### Действия
- Комментарий comment_pk не найден -> 404
- Удалить может автор комментария (comment.user) или админ (is_staff) -
  **не** владелец поста/питомца, если он не автор комментария -> иначе 403 Forbidden
- Удаление комментария каскадно удаляет его ответы (reply_comment self FK, CASCADE)
- Редирект на posts:detail поста

---

## Отображение в посте

Комментарии рендерятся на странице поста (posts:detail, см. contracts/posts.md),
контекст добавляется в PostDetailView:

| Переменная | Тип | Описание |
| --- | --- | --- |
| comments | QuerySet[Comment] | комментарии верхнего уровня поста (reply_comment is null) |
| comment_form | CommentForm | форма добавления комментария, видна только залогиненным |

Каждый комментарий (и его ответы, рекурсивно) рендерится инклюжн-тегом
`comment_item` (comments/templatetags/comment_tags.py, шаблон
includes/comment_item.html):

| Переменная | Тип | Описание |
| --- | --- | --- |
| comment | Comment | автор, текст, дата |
| can_delete | bool | считается отдельно для каждого комментария: user == comment.user или user.is_staff |
| replies | QuerySet[Comment] | вложенные ответы этого комментария |

### Доступ
- Гость видит все комментарии, но не видит форму добавления и кнопки удаления/ответа
- Залогиненный видит форму добавления/ответа; кнопку «Удалить» - только на своих
  комментариях (или если админ)

### Ошибки
- Пост не найден -> 404 (обрабатывает posts:detail)

---

## Маршруты (namespace `comments`)

| Имя | URL | View |
| --- | --- | --- |
| comments:create | /comments/post/<post_pk>/new/ | add_comment |
| comments:reply | /comments/<comment_pk>/reply/ | add_reply |
| comments:delete | /comments/<comment_pk>/delete/ | delete_comment |
