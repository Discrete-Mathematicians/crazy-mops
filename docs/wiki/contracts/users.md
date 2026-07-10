# Контракты приложения `users`

Приложение подключено как `path("users/", include("users.urls"))`, namespace — `users`.
Модель: `users.User` (`AUTH_USER_MODEL`), наследует `AbstractUser`.
Поля профиля: `login`, `display_name`, `avatar`, `account_type` (+ стандартные `username`, `email`, `password`).

---

## Регистрация
- **URL:** /users/signup/
- **View:** users.views.signup
- **Шаблон:** templates/users/signup.html
- **Форма:** users.forms.SignUpForm (поля: username, login, email, display_name + password1/password2)
- **Доступ:** гость (аноним)

### Контекст
| Переменная | Тип | Описание |
| --- | --- | --- |
| form | SignUpForm | форма регистрации, ошибки валидации в form.errors |

### Действия на странице
- POST формы -> создаёт пользователя, логинит и редиректит на users:profile_edit

### Ошибки
- Невалидные данные -> повторный рендер страницы с form.errors (не редирект)

---

## Вход
- **URL:** /users/login/
- **View:** django.contrib.auth.views.LoginView
- **Шаблон:** templates/users/login.html
- **Форма:** AuthenticationForm (поля: username, password)
- **Доступ:** гость (аноним)

### Контекст
| Переменная | Тип | Описание |
| --- | --- | --- |
| form | AuthenticationForm | форма входа |
| next | str | URL для редиректа после входа (из ?next=) |

### Действия на странице
- POST -> при успехе редирект на LOGIN_REDIRECT_URL (/) или на ?next=

### Ошибки
- Неверный логин/пароль -> рендер с ошибкой формы

---

## Выход
- **URL:** /users/logout/
- **View:** django.contrib.auth.views.LogoutView
- **Шаблон:** нет (сразу редирект)
- **Доступ:** залогиненный

### Действия
- Разлогинивает и редиректит на LOGOUT_REDIRECT_URL (users:login)

---

## Редактирование профиля
- **URL:** /users/profile/edit/
- **View:** users.views.profile_edit
- **Шаблон:** templates/users/profile_edit.html
- **Форма:** users.forms.ProfileEditForm (поля: display_name, avatar, email)
- **Доступ:** login_required (гостя редиректит на LOGIN_URL = users:login)

### Контекст
| Переменная | Тип | Описание |
| --- | --- | --- |
| form | ProfileEditForm | предзаполнена данными request.user |

### Действия на странице
- POST (multipart/form-data — из-за avatar) -> сохраняет профиль, редирект на users:profile_edit

### Ошибки
- Невалидные данные -> рендер с form.errors
- Гость -> редирект на страницу входа (обрабатывает login_required, не шаблон)

### Важно для шаблона
- Тег <form> должен иметь enctype="multipart/form-data", иначе avatar не загрузится
