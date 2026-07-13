# Контракт приложения `subscriptions` (view → шаблон)

Подписка и отписка от карточек питомцев.

---

## Подписаться на питомца

- **URL:** `/subscriptions/pets/<int:pet_pk>/subscribe/`
- **View:** `subscriptions.views.subscribe`
- **Метод:** `POST`
- **Доступ:** `login_required` (аноним → редирект на `LOGIN_URL`)

### Действия
- Если пользователь пытается подписаться на своего питомца, запрос отклоняется с `403 Forbidden`.
- Иначе создаётся запись `Subscription` для текущего пользователя и указанного питомца.
- После успешного действия происходит редирект на страницу питомца (`pets:detail`).

### Ошибки
- Питомец не найден → `404`.
- Самоподписка → `403 Forbidden`.

---

## Отписаться от питомца

- **URL:** `/subscriptions/pets/<int:pet_pk>/unsubscribe/`
- **View:** `subscriptions.views.unsubscribe`
- **Метод:** `POST`
- **Доступ:** `login_required` (аноним → редирект на `LOGIN_URL`)

### Действия
- Удаляется запись `Subscription` для текущего пользователя и указанного питомца.
- После успешного действия происходит редирект на страницу питомца (`pets:detail`).

### Ошибки
- Питомец не найден → `404`.

---

## Маршруты (namespace `subscriptions`)

| Имя | URL | View |
| --- | --- | --- |
| `subscriptions:subscribe` | `/subscriptions/pets/<int:pet_pk>/subscribe/` | `subscriptions.views.subscribe` |
| `subscriptions:unsubscribe` | `/subscriptions/pets/<int:pet_pk>/unsubscribe/` | `subscriptions.views.unsubscribe` |
