function initSingleDropzone(inputId, previewId, placeholderId) {
    const input = document.getElementById(inputId);
    if (!input) return;

    input.addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function (event) {
            const preview = document.getElementById(previewId);
            const placeholder = document.getElementById(placeholderId);
            preview.src = event.target.result;
            preview.style.display = 'block';
            placeholder.style.display = 'none';
        };
        reader.readAsDataURL(file);
    });
}