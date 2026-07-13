# Контракты приложения `users`

Приложение: `path("users/", include("users.urls"))`, namespace `users`.
Модель: `users.User` (`AUTH_USER_MODEL`), наследует `AbstractBaseUser + PermissionsMixin`.
Вход по полю **login** (`USERNAME_FIELD = "login"`), поля username НЕТ.

Поведение по умолчанию (пока пользователь не изменил):
- `display_name` = `login`
- `avatar` пустой -> показывается дефолт из статики (см. `User.avatar_url`)

Поля: login (уник., обязателен), password, display_name, first_name, last_name, email, avatar, account_type.

Аватар: дефолтная картинка лежит в статике `static/users/img/default_avatar.png`. В шаблонах использовать `user.avatar_url` — он отдаёт загруженный аватар либо дефолт.

---

## Регистрация
- **URL:** /users/signup/
- **View:** users.views.signup
- **Шаблон:** templates/users/signup.html
- **Форма:** users.forms.SignUpForm (поля: login + password1/password2)
- **Доступ:** гость
- **Обязательные поля:** login, password (остальное заполняется автоматически / позже)

### Контекст
| Переменная | Тип | Описание |
| --- | --- | --- |
| form | SignUpForm | форма регистрации |

### Действия
- POST -> создаёт пользователя (display_name=login), логинит, редирект на users:profile_edit

---

## Вход
- **URL:** /users/login/
- **View:** django.contrib.auth.views.LoginView
- **Шаблон:** templates/users/login.html
- **Форма:** AuthenticationForm (поле username в форме = наш login)
- **Доступ:** гость

### Действия
- POST -> при успехе редирект на LOGIN_REDIRECT_URL (/) или ?next=

---

## Выход
- **URL:** /users/logout/
- **View:** django.contrib.auth.views.LogoutView
- **Доступ:** залогиненный
- Разлогинивает, редирект на LOGOUT_REDIRECT_URL (users:login)

---

## Редактирование профиля
- **URL:** /users/profile/edit/
- **View:** users.views.profile_edit
- **Шаблон:** templates/users/profile_edit.html
- **Форма:** users.forms.ProfileEditForm (display_name, first_name, last_name, email, avatar)
- **Доступ:** login_required (гостя -> LOGIN_URL)

### Контекст
| Переменная | Тип | Описание |
| --- | --- | --- |
| form | ProfileEditForm | предзаполнена данными request.user |

### Действия
- POST (multipart/form-data из-за avatar) -> сохраняет профиль, редирект на users:profile_edit

### Важно для шаблона
- <form> должен иметь enctype="multipart/form-data", иначе avatar не загрузится
