# Контракты приложения `posts` (view -> шаблон)

Namespace `posts`, подключено как `path("posts/", include("posts.urls"))`.
Права: редактирование/удаление - владелец питомца или админ (capability,
как can_manage в pets/profile). Создание - только к своему питомцу (или админ).

---

## Создание поста
- **URL:** /posts/new/<int:pet_pk>/
- **View:** posts.views.PostCreateView (CreateView)
- **Шаблон:** templates/posts/post_form.html
- **Доступ:** login_required + владелец питомца pet_pk или админ (иначе 403)

### Контекст
| Переменная | Тип | Описание |
| --- | --- | --- |
| form | PostForm | поля: title (обязателен), description, tags (строка хештегов), media (несколько файлов) |
| pet | Pet | питомец, к которому создаётся пост (для заголовка страницы) |

### Действия
- POST -> создаётся Post, pet проставляется из URL
- tags - строка парсится по запятым/пробелам, `#` в начале слова отбрасывается; для каждого имени тега - `Tag.objects.get_or_create` (существующий переиспользуется, новый создаётся), затем `post.tags.set(...)`
- media - каждый загруженный файл сохраняется как отдельный `PostMedia` (media_type определяется по content_type файла: image/* -> image, иначе video; display_order - по порядку загрузки)
- редирект на posts:detail

### Ошибки
- Питомец pet_pk не найден -> 404
- Ошибки валидации -> под полями

---

## Просмотр поста
- **URL:** /posts/<int:pk>/
- **View:** posts.views.PostDetailView (DetailView)
- **Шаблон:** templates/posts/post_detail.html
- **Доступ:** публичный (гость читает)

### Контекст
| Переменная | Тип | Описание |
| --- | --- | --- |
| post | Post | title, description, created_at, post.pet - для ссылки на питомца |
| post.media | QuerySet[PostMedia] | медиафайлы поста, отсортированы по display_order; media_url.url, media_type (image/video) |
| post.tags | QuerySet[Tag] | хештеги поста; каждый - ссылка на posts:by_tag |
| can_manage | bool | владелец питомца или админ - кнопки «Редактировать»/«Удалить» |

Будущее расширение: контекст дополнится comments/reactions,
когда появятся соответствующие приложения.

### Ошибки
- Пост не найден -> 404

---

## Редактирование поста
- **URL:** /posts/<int:pk>/edit/
- **View:** posts.views.PostUpdateView (UpdateView)
- **Шаблон:** templates/posts/post_form.html (общий с созданием, предзаполнен)
- **Доступ:** login_required + владелец питомца или админ (403)

### Действия
- tags - предзаполняется текущими тегами поста, обрабатывается так же, как при создании (набор тегов поста полностью заменяется на разобранный из строки)
- media - новые загруженные файлы добавляются к уже существующим (display_order продолжает нумерацию), старые не удаляются

---

## Удаление поста
- **URL:** /posts/<int:pk>/delete/
- **View:** posts.views.PostDeleteView (DeleteView)
- **Шаблон:** templates/posts/post_confirm_delete.html
- **Доступ:** login_required + владелец питомца или админ (403)
- POST -> удаление, редирект на pets:detail питомца

---

## Посты по тегу
- **URL:** /posts/tag/<str:tag>/
- **View:** posts.views.PostsByTagView (ListView)
- **Шаблон:** templates/posts/posts_by_tag.html
- **Доступ:** публичный (гость читает)

### Контекст
| Переменная | Тип | Описание |
| --- | --- | --- |
| posts_page | Page | посты с данным тегом, сортировка по created_at (новые сверху), пагинация по 10 |
| tag_name | str | имя тега из URL (для заголовка страницы) |

### Действия
- Клик по посту -> GET posts:detail

### Ошибки
- Тег не существует или без постов -> 200, posts_page пустой (не 404)

---

## Маршруты (namespace `posts`)
| Имя | URL | View |
| --- | --- | --- |
| posts:create | /posts/new/<pet_pk>/ | PostCreateView |
| posts:by_tag | /posts/tag/<tag>/ | PostsByTagView |
| posts:detail | /posts/<pk>/ | PostDetailView |
| posts:edit | /posts/<pk>/edit/ | PostUpdateView |
| posts:delete | /posts/<pk>/delete/ | PostDeleteView |

---

## Партиалы

| Партиал | Ожидает | Описание |
| --- | --- | --- |
| includes/post_card.html | post (Post) | карточка поста в списках (профиль питомца, лента, посты по тегу); превью текста, ссылки на пост и питомца |

Вызов: `{% include "includes/post_card.html" with post=obj only %}`

## Точки входа из других приложений

- Кнопка «Создать пост» - на странице питомца (`pets/pet_detail.html`),
  внутри блока `can_manage`, ведёт на `posts:create` с pk питомца.
- История постов питомца - на странице питомца (`pets/pet_detail.html`),
  секция «Посты»: `pet.posts.all` через партиал post_card.
