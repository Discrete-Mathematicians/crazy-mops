## Отношения

- **subscription to user**: многие ко многим
- **pet to user**: многие ко многим
- **post to pet**: многие ко многим
- **comment to user**: многие ко многим
- **comment_media to comment**: многие ко многим
- **reaction to comment**: многие ко многим
- **comment to post**: многие ко многим
- **reaction to post**: многие ко многим
- **post_tag to tag**: многие ко многим
- **post_media to post**: многие ко многим
- **post_tag to post**: one_to_one
- **subscription to pet**: многие ко многим
- **comment to comment**: один ко многим


## ER-Диаграма

```mermaid
erDiagram
	subscription }o--|| user : references
	pet }o--|| user : references
	post }o--|| pet : references
	comment }o--|| user : references
	comment_media }o--|| comment : references
	reaction }o--|| comment : references
	comment }o--|| post : references
	reaction }o--|| post : references
	post_tag }o--|| tag : references
	post_media }o--|| post : references
	post_tag ||--|| post : references
	subscription }o--|| pet : references
	comment ||--o{ comment : references

	pet {
		BIGSERIAL id
		BIGINT owner_id
		VARCHAR(255) name
		TEXT avatar
		VARCHAR(100) breed
		DATE birthday
		VARCHAR(50) eye_color
		VARCHAR(50) coat_color
		VARCHAR(50) pet_type
		SMALLINT sex
	}

	post {
		BIGSERIAL id
		BIGINT pet_id
		TEXT description
		VARCHAR(255) title
		TIMESTAMP created_at
	}

	comment {
		BIGSERIAL id
		BIGINT post_id
		BIGINT user_id
		BIGINT reply_comment_id
		TEXT description
		TIMESTAMP created_at
	}

	user {
		BIGSERIAL id
		VARCHAR(255) display_name
		TEXT avatar
		VARCHAR(255) password
		VARCHAR(255) login
		VARCHAR(255) email
		SMALLINT account_type
		TIMESTAMP join_date
		TEXT info
		VARCHAR(50) pronouns
		VARCHAR(30) gender
		VARCHAR(100) city
		VARCHAR(20) phone_number
	}

	subscription {
		BIGSERIAL id
		BIGINT user_id
		BIGINT pet_id
		TIMESTAMP created_at
	}

	tag {
		BIGSERIAL id
		VARCHAR(255) name
	}

	post_tag {
		BIGINT post_id
		BIGINT tag_id
	}

	post_media {
		BIGSERIAL id
		BIGINT post_id
		TEXT media_url
		SMALLINT media_type
		SMALLINT display_order
	}

	comment_media {
		BIGSERIAL id
		BIGINT comment_id
		TEXT media_url
		SMALLINT media_type
		SMALLINT display_order
	}

	reaction {
		BIGSERIAL id
		BIGINT comment_id
		BIGINT post_id
		BIGINT user_id
		SMALLINT reaction_type
		TIMESTAMP created_at
	}
```