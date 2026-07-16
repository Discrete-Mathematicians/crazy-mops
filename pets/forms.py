from django import forms

from .models import Pet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ["name", "avatar", "pet_type", "breed", "birthday", "sex", "eye_color", "coat_color"]
        widgets = {
            "birthday": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "avatar": forms.FileInput(attrs={"class": "dropzone-square__input"}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Кличка не может быть пустой.")
        return name
