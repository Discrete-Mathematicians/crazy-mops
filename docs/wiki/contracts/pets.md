# Контракты приложения `pets` (view → шаблон)

Профиль питомца: создание, просмотр, редактирование и удаление карточки.
Поля модели соответствуют схеме `pet` из [docs/MODELS.md](../../MODELS.md).

> Доступ к редактированию/удалению — только у владельца (`owner`).
> `login_required` реализован через `LoginRequiredMixin`, проверка владельца — через `UserPassesTestMixin` (403 для чужого пользователя).

---

## Создание карточки

- **URL:** `/pets/new/`
- **View:** `pets.views.PetCreateView` (`CreateView`)
- **Шаблон:** `templates/pets/pet_form.html`
- **Доступ:** `login_required` (аноним → редирект на `LOGIN_URL`)

### Контекст
| Переменная | Тип | Описание |
| --- | --- | --- |
| form | PetForm | поля: name, avatar, pet_type, breed, birthday, sex, eye_color, coat_color |

### Действия
- POST формы → создаётся `Pet`, `owner` проставляется из `request.user`
- Успех → редирект на `get_absolute_url()` (страница питомца)

### Ошибки
- Ошибки валидации формы рендерятся под соответствующими полями

---

## Просмотр карточки

- **URL:** `/pets/<int:pk>/`
- **View:** `pets.views.PetDetailView` (`DetailView`)
- **Шаблон:** `templates/pets/pet_detail.html`
- **Доступ:** публичный (гость читает)

### Контекст
| Переменная | Тип | Описание |
| --- | --- | --- |
| pet | Pet | name, avatar, pet_type, breed, birthday, sex, eye_color, coat_color |
| can_manage | bool | True только у владельца — показывать кнопки «Редактировать»/«Удалить» |
| posts_page | Page | пагинатор истории постов питомца (5 на страницу, новые сверху); ?page= в query |

### Ошибки
- Объект не найден → 404 (обрабатывает view, не шаблон)

---

## Редактирование карточки

- **URL:** `/pets/<int:pk>/edit/`
- **View:** `pets.views.PetUpdateView` (`UpdateView`)
- **Шаблон:** `templates/pets/pet_form.html`
- **Доступ:** `login_required` + только владелец (иначе 403)

### Контекст
| Переменная | Тип | Описание |
| --- | --- | --- |
| form | PetForm | предзаполнена данными питомца |
| pet / object | Pet | редактируемый объект |

### Действия
- POST формы → сохранение изменений, редирект на страницу питомца

---

## Удаление карточки

- **URL:** `/pets/<int:pk>/delete/`
- **View:** `pets.views.PetDeleteView` (`DeleteView`)
- **Шаблон:** `templates/pets/pet_confirm_delete.html`
- **Доступ:** `login_required` + только владелец (иначе 403)

### Контекст
| Переменная | Тип | Описание |
| --- | --- | --- |
| pet / object | Pet | удаляемый объект (для подтверждения) |

### Действия
- GET → страница подтверждения
- POST → удаление, редирект на `success_url` (`pets:create`)

---

## Маршруты (namespace `pets`)

| Имя | URL | View |
| --- | --- | --- |
| `pets:create` | `/pets/new/` | PetCreateView |
| `pets:detail` | `/pets/<pk>/` | PetDetailView |
| `pets:edit` | `/pets/<pk>/edit/` | PetUpdateView |
| `pets:delete` | `/pets/<pk>/delete/` | PetDeleteView |

## Заметки для смежных задач

- **Шаблоны** (sub-issue «Шаблоны приложения pets»): текущие `templates/pets/*.html` — заглушки, наследуются от `base.html`. Ошибки валидации показывать под полями; форма создания/редактирования — `enctype="multipart/form-data"` (загрузка `avatar`).
- **Зависимость от `users`:** `owner` ссылается на `settings.AUTH_USER_MODEL`. Пока приложение `users` не подключено, `LOGIN_URL = "/admin/login/"` (см. TODO в `settings.py`); после подключения заменить на `users:login`.
