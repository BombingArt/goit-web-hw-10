from django.forms import (
    ModelForm,
    CharField,
    TextInput,
    ChoiceField,
    Textarea,
    ModelChoiceField,
)
from quotesapp.models import Quote, Author


class AuthorsForm(ModelForm):
    fullname = CharField(min_length=2, max_length=50, required=True, widget=TextInput)
    born_location = CharField(
        min_length=5, max_length=50, required=True, widget=TextInput
    )
    description = CharField(max_length=1000, required=True, widget=Textarea)

    DAY_CHOICES = [(str(day), str(day)) for day in range(1, 32)]
    MONTH_CHOICES = [
        ("January", "January"),
        ("February", "February"),
        ("March", "March"),
        ("April", "April"),
        ("May", "May"),
        ("June", "June"),
        ("July", "July"),
        ("August", "August"),
        ("September", "September"),
        ("October", "October"),
        ("November", "November"),
        ("December", "December"),
    ]
    YEAR_CHOICES = [(str(year), str(year)) for year in range(1600, 2025)]

    born_day = ChoiceField(choices=DAY_CHOICES, label="Day")
    born_month = ChoiceField(choices=MONTH_CHOICES, label="Month")
    born_year = ChoiceField(choices=YEAR_CHOICES, label="Year")

    class Meta:
        model = Author
        fields = [
            "fullname",
            "born_location",
            "description",
            "born_day",
            "born_month",
            "born_year",
        ]

    def save(self, commit=True):
        instance = super(AuthorsForm, self).save(commit=False)
        born_day = self.cleaned_data["born_day"]
        born_month = self.cleaned_data["born_month"]
        born_year = self.cleaned_data["born_year"]
        born_date_str = f"{born_month} {born_day}, {born_year}"
        instance.born_date = born_date_str
        instance.born_location = f"in {self.cleaned_data['born_location']}"
        if commit:
            instance.save()
        return instance


class QuoteForm(ModelForm):
    author = ModelChoiceField(queryset=Author.objects.all(), empty_label=None)
    tags = CharField(max_length=50, required=False, widget=TextInput)
    quote = CharField(max_length=1000, required=True, widget=Textarea)

    class Meta:
        model = Quote
        fields = ["tags", "author", "quote"]

    def clean_tags(self):
        tags = self.cleaned_data.get("tags")
        return [] if tags == "" else tags
