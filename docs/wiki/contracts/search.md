## Страница поиска

- **URL:** /search/
- **View:** search.views.SearchView
- **Шаблон:** templates/search/search.html
- **Доступ:** гость читает

### Контекст
| Переменная | Тип | Описание |
| --- | --- | --- |
| results | Page | пагинатор; User или Pet - в зависимости от search_type |
| q | str | поисковая строка как её ввёл юзер (для повторного заполнения поля) |
| search_type | str | 'owners' или 'pets', невалидное значение в query - фоллбэк на 'owners' |
| searched | bool | True, если в query был параметр q (отличает "не искал" от "искал, пусто") |
| query_string | str | q и type без page - для ссылок пагинации |
| is_paginated | bool | True, если результатов больше одной страницы |
| page_obj | Page | стандартный Django Paginator page object |

### Действия на странице (если есть)
- Переключатель типа -> GET /search/?type=owners или ?type=pets
- Форма поиска -> GET /search/?q=<строка>
- Клик по карточке владельца -> GET profiles:profile_detail (см. contracts/user_profile.md)
- Клик по карточке питомца -> GET pets:detail (см. contracts/pets.md)

### Ошибки
- Пустой запрос (q отсутствует или пустой) -> results пустой, searched=False, не ошибка
- Запрос без результатов -> results пустой, searched=True, не ошибка