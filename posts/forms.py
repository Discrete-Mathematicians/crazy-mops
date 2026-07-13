import re

from django import forms

from posts.models import Post, Tag


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(item, initial) for item in data]
        return single_file_clean(data, initial)


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        label="хештеги",
        required=False,
        help_text="через запятую или пробел, например: #прогулка гуляем",
    )
    media = MultipleFileField(label="медиа", required=False)

    class Meta:
        model = Post
        fields = ("title", "description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["tags"].initial = ", ".join(self.instance.tags.values_list("name", flat=True))

    def clean_tags(self):
        raw = self.cleaned_data.get("tags", "")
        names = []
        seen = set()
        for chunk in re.split(r"[,\s]+", raw):
            name = chunk.lstrip("#").strip().lower()
            if name and name not in seen:
                seen.add(name)
                names.append(name)
        return names

    def clean_media(self):
        files = self.cleaned_data.get("media")
        if not files:
            return []
        return files if isinstance(files, list) else [files]

    def save_tags(self, post):
        tags = [Tag.objects.get_or_create(name=name)[0] for name in self.cleaned_data.get("tags", [])]
        post.tags.set(tags)
