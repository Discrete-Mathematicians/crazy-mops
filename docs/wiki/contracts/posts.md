# Контракты приложения `posts` (view → шаблон)

Namespace `posts`, подключено как `path("posts/", include("posts.urls"))`.
Права: редактирование/удаление — владелец питомца или админ (capability,
как can_manage в pets/profile). Создание — только к своему питомцу (или админ).

---

## Создание поста
- **URL:** /posts/new/<int:pet_pk>/
- **View:** posts.views.PostCreateView (CreateView)
- **Шаблон:** templates/posts/post_form.html
- **Доступ:** login_required + владелец питомца pet_pk или админ (иначе 403)

### Контекст
| Переменная | Тип | Описание |
| --- | --- | --- |
| form | PostForm | поля: title (обязателен), description |
| pet | Pet | питомец, к которому создаётся пост (для заголовка страницы) |

### Действия
- POST → создаётся Post, pet проставляется из URL, редирект на posts:detail

### Ошибки
- Питомец pet_pk не найден → 404
- Ошибки валидации → под полями

---

## Просмотр поста
- **URL:** /posts/<int:pk>/
- **View:** posts.views.PostDetailView (DetailView)
- **Шаблон:** templates/posts/post_detail.html
- **Доступ:** публичный (гость читает)

### Контекст
| Переменная | Тип | Описание |
| --- | --- | --- |
| post | Post | title, description, created_at, post.pet — для ссылки на питомца |
| can_manage | bool | владелец питомца или админ — кнопки «Редактировать»/«Удалить» |

Будущее расширение (вне #37): контекст дополнится comments/reactions,
когда появятся соответствующие приложения.

### Ошибки
- Пост не найден → 404

---

## Редактирование поста
- **URL:** /posts/<int:pk>/edit/
- **View:** posts.views.PostUpdateView (UpdateView)
- **Шаблон:** templates/posts/post_form.html (общий с созданием, предзаполнен)
- **Доступ:** login_required + владелец питомца или админ (403)

---

## Удаление поста
- **URL:** /posts/<int:pk>/delete/
- **View:** posts.views.PostDeleteView (DeleteView)
- **Шаблон:** templates/posts/post_confirm_delete.html
- **Доступ:** login_required + владелец питомца или админ (403)
- POST → удаление, редирект на pets:detail питомца

---

## Маршруты (namespace `posts`)
| Имя | URL | View |
| --- | --- | --- |
| posts:create | /posts/new/<pet_pk>/ | PostCreateView |
| posts:detail | /posts/<pk>/ | PostDetailView |
| posts:edit | /posts/<pk>/edit/ | PostUpdateView |
| posts:delete | /posts/<pk>/delete/ | PostDeleteView |