# Контракт приложения `feed` (view -> шаблон)

Служебное приложение - без своей модели, только логика чтения и
комбинирования данных из `posts` (Post) и `subscriptions` (Subscription).
Собирает домашнюю страницу. календарь ДР и рейтинг питомцев добавятся отдельными задачами
поверх этого контракта.

---

## Лента (главная страница)
- **URL:** /
- **View:** feed.views.FeedView (ListView)
- **Шаблон:** templates/feed/feed.html
- **Доступ:** login_required (аноним -> редирект на LOGIN_URL, лента персонализирована)

### Контекст
| Переменная | Тип | Описание |
| --- | --- | --- |
| posts | Page (object_list) | посты питомцев из подписок текущего юзера, сортировка по created_at desc |
| page_obj | Page | пагинатор, 10 постов на страницу |
| is_paginated | bool | показывать пагинатор |

### Действия на странице
- Клик по посту -> GET posts:detail (см. contracts/posts.md)
- Клик по питомцу в шапке карточки -> GET pets:detail
- Пустая лента (нет подписок или у подписок нет постов) -> ссылка на search:search («Найти питомцев»)

### Ошибки
- Аноним -> редирект на страницу логина

---

## Партиалы

| Партиал | Ожидает | Описание |
| --- | --- | --- |
| includes/post_card.html | post (Post) | карточка поста, переиспользуется из `posts`, не дублируется |

Вызов: `{% include "includes/post_card.html" with post=post only %}`

## Виджет: дни рождения

Партиал, встраивается в шаблон ленты (feed.html), не отдельная страница.

### Контекст (передаётся из FeedView.get_context_data)
| Переменная | Тип | Описание |
| --- | --- | --- |
| upcoming_birthdays | list[Pet] | питомцы из подписок юзера с заполненным birthday, отсортированы по ближайшей дате ДР (месяц/день, без учёта года рождения) |

### Партиал
| Партиал | Ожидает | Описание |
| --- | --- | --- |
| includes/birthday_widget.html | upcoming_birthdays (list[Pet]) | список: аватар, имя, дата ДР, ссылка на pets:detail |

Вызов: `{% include "includes/birthday_widget.html" with upcoming_birthdays=upcoming_birthdays only %}`

### Действия
- Без подписок или без питомцев с birthday -> виджет показывает подсказку, не ошибка

## Точки входа из других приложений

- Ссылка «Лента» в навбаре (`base.html`) -> feed:home.
- LOGIN_REDIRECT_URL (настройка `users`, зона Грега) должен указывать на
  feed:home, иначе после логина юзера кинет на несуществующий
  /accounts/profile/.

## Зависимости

- posts: модель Post, партиал includes/post_card.html
- subscriptions: модель Subscription (обратная связь pet.subscription -> user)