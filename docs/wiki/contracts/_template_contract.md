## Шаблон контракта (`contracts/_template.md`)

## <Название страницы/виджета>
- **URL:** /pets/<int:pk>/
- **View:** pets.views.PetDetailView
- **Шаблон:** templates/pets/pet_detail.html
- **Доступ:** гость читает / login_required

### Контекст
| Переменная | Тип | Описание |
| --- | --- | --- |
| pet | Pet | name, avatar, breed, birthday, pet_type, sex |
| posts | Page | пагинатор, посты питомца, новые сверху |
| can_manage | bool | показывать владельческие кнопки |

### Действия на странице (если есть)
- Кнопка «Подписаться» - POST subscriptions:subscribe (см. contracts/subscriptions.md)

### Ошибки
- Объект не найден - 404 (обрабатывает view, не шаблон)
