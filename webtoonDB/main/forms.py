from django.forms import ModelForm
from .models import Webtoon


class WebtoonForm(ModelForm):
    class Meta:
        model = Webtoon
        fields = ["title", "site", "finished_ch"]
