# Модель базы данных

- [Тип БД](#Тип_БД)
- [Структура таблиц](#Структура_таблиц)
	- [pet](#pet)
	- [post](#post)
	- [comment](#comment)
	- [user](#user)
	- [subscription](#subscription)
	- [tag](#tag)
	- [post_tag](#post_tag)
	- [post_media](#post_media)
	- [comment_media](#comment_media)
	- [reaction](#reaction)
- [Отношения](#Отношения)
- [Скриншот схемы](#Скриншот_схемы)

## Тип_БД

- **Database system:** PostgreSQL

## Структура_таблиц

### pet

| Name           | Type         | Settings        | References | Note |
| -------------- | ------------ | --------------- | ---------- | ---- |
| **id**         | BIGSERIAL    | 🔑 PK, not null |            |      |
| **owner_id**   | BIGINT       | not null        |            |      |
| **name**       | VARCHAR(255) | not null        |            |      |
| **avatar**     | TEXT         | null            |            |      |
| **breed**      | VARCHAR(100) | null            |            |      |
| **birthday**   | DATE         | null            |            |      |
| **eye_color**  | VARCHAR(50)  | null            |            |      |
| **coat_color** | VARCHAR(50)  | null            |            |      |
| **pet_type**   | VARCHAR(50)  | not null        |            |      |
| **sex**        | SMALLINT     | null            |            |      | 


### post

| Name            | Type         | Settings        | References | Note |
| --------------- | ------------ | --------------- | ---------- | ---- |
| **id**          | BIGSERIAL    | 🔑 PK, not null |            |      |
| **pet_id**      | BIGINT       | not null        |            |      |
| **description** | TEXT         | null            |            |      |
| **title**       | VARCHAR(255) | null            |            |      |
| **created_at**  | TIMESTAMP    | not null        |            |      | 


### comment

| Name                 | Type      | Settings        | References | Note |
| -------------------- | --------- | --------------- | ---------- | ---- |
| **id**               | BIGSERIAL | 🔑 PK, not null |            |      |
| **post_id**          | BIGINT    | not null        |            |      |
| **user_id**          | BIGINT    | not null        |            |      |
| **reply_comment_id** | BIGINT    | null            |            |      |
| **description**      | TEXT      | not null        |            |      |
| **created_at**       | TIMESTAMP | not null        |            |      | 


### user

| Name             | Type         | Settings                | References | Note |
| ---------------- | ------------ | ----------------------- | ---------- | ---- |
| **id**           | BIGSERIAL    | 🔑 PK, not null, unique |            |      |
| **display_name** | VARCHAR(255) | not null                |            |      |
| **avatar**       | TEXT         | null                    |            |      |
| **password**     | VARCHAR(255) | not null                |            |      |
| **login**        | VARCHAR(255) | not null, unique        |            |      |
| **email**        | VARCHAR(255) | not null, unique        |            |      |
| **account_type** | SMALLINT     | not null, default: 0    |            |      |
| **join_date**    | TIMESTAMP    | not null                |            |      |
| **info**         | TEXT         | null                    |            |      |
| **pronouns**     | VARCHAR(50)  | null                    |            |      |
| **gender**       | VARCHAR(30)  | null                    |            |      |
| **city**         | VARCHAR(100) | null                    |            |      |
| **phone_number** | VARCHAR(20)  | null                    |            |      | 


### subscription

| Name           | Type      | Settings        | References | Note |
| -------------- | --------- | --------------- | ---------- | ---- |
| **id**         | BIGSERIAL | 🔑 PK, not null |            |      |
| **user_id**    | BIGINT    | not null        |            |      |
| **pet_id**     | BIGINT    | not null        |            |      |
| **created_at** | TIMESTAMP | not null        |            |      | 


#### Indexes
| Name                 | Unique | Fields          |
| -------------------- | ------ | --------------- |
| subscription_index_0 | ✅      | user_id, pet_id |
### tag

| Name     | Type         | Settings         | References | Note |
| -------- | ------------ | ---------------- | ---------- | ---- |
| **id**   | BIGSERIAL    | 🔑 PK, not null  |            |      |
| **name** | VARCHAR(255) | not null, unique |            |      | 


### post_tag

| Name        | Type   | Settings        | References | Note |
| ----------- | ------ | --------------- | ---------- | ---- |
| **post_id** | BIGINT | 🔑 PK, not null |            |      |
| **tag_id**  | BIGINT | 🔑 PK, not null |            |      | 


#### Indexes
| Name             | Unique | Fields |
| ---------------- | ------ | ------ |
| post_tag_index_0 |        | tag_id |

### post_media

| Name              | Type      | Settings        | References | Note |
| ----------------- | --------- | --------------- | ---------- | ---- |
| **id**            | BIGSERIAL | 🔑 PK, not null |            |      |
| **post_id**       | BIGINT    | not null        |            |      |
| **media_url**     | TEXT      | not null        |            |      |
| **media_type**    | SMALLINT  | not null        |            |      |
| **display_order** | SMALLINT  | not null        |            |      | 


### comment_media

| Name              | Type      | Settings        | References | Note |
| ----------------- | --------- | --------------- | ---------- | ---- |
| **id**            | BIGSERIAL | 🔑 PK, not null |            |      |
| **comment_id**    | BIGINT    | not null        |            |      |
| **media_url**     | TEXT      | not null        |            |      |
| **media_type**    | SMALLINT  | not null        |            |      |
| **display_order** | SMALLINT  | not null        |            |      | 


### reaction

| Name              | Type      | Settings        | References | Note |
| ----------------- | --------- | --------------- | ---------- | ---- |
| **id**            | BIGSERIAL | 🔑 PK, not null |            |      |
| **comment_id**    | BIGINT    | null            |            |      |
| **post_id**       | BIGINT    | null            |            |      |
| **user_id**       | BIGINT    | not null        |            |      |
| **reaction_type** | SMALLINT  | not null        |            |      |
| **created_at**    | TIMESTAMP | not null        |            |      | 


#### Indexes
| Name             | Unique | Fields              |
| ---------------- | ------ | ------------------- |
| reaction_index_0 | ✅      | post_id, user_id    |
| reaction_index_1 | ✅      | user_id, comment_id |

#### Checks

| Name              | Type      | Settings        | References | Note | Check |
| ----------------- | --------- | --------------- | ---------- | ---- | ----- |
| **comment_id**    | BIGINT    | null            |            |      | (post_id IS NOT NULL AND comment_id IS NULL) OR (post_id IS NULL AND comment_id IS NOT NULL) |

## Отношения

- **subscription to user**: many_to_one
- **pet to user**: many_to_one
- **post to pet**: many_to_one
- **comment to user**: many_to_one
- **comment_media to comment**: many_to_one
- **reaction to comment**: many_to_one
- **comment to post**: many_to_one
- **reaction to post**: many_to_one
- **post_tag to tag**: many_to_one
- **post_media to post**: many_to_one
- **post_tag to post**: one_to_one
- **subscription to pet**: many_to_one
- **comment to comment**: one_to_one

## Скриншот_схемы
![alt text](mops-bd.png)
