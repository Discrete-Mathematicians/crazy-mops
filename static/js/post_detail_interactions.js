/*
Лайтбокс медиа (post_detail) - нативный <dialog>
*/

document.addEventListener('click', (event) => {
    const trigger = event.target.closest('[data-lightbox]');
    if (trigger) {
        const dialog = document.getElementById('media-lightbox');
        dialog.querySelector('.lightbox__image').src = trigger.dataset.lightbox;
        dialog.showModal();
        return;
    }
    if (event.target.closest('.lightbox__close')) {
        document.getElementById('media-lightbox').close();
    }
});

document.getElementById('media-lightbox')?.addEventListener('click', (event) => {
    if (event.target.id === 'media-lightbox') {
        event.target.close();
    }
});

/*
Раскрытие reply-формы под комментарием (comment_item)
Кнопка "Ответить" получает data-reply-toggle с id формы
*/

document.addEventListener('click', (event) => {
    const toggle = event.target.closest('[data-reply-toggle]');
    if (!toggle) {
        return;
    }
    const form = document.getElementById(toggle.dataset.replyToggle);
    form.classList.toggle('is-collapsed');
    if (!form.classList.contains('is-collapsed')) {
        form.querySelector('textarea')?.focus();
    }
});