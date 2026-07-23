from django import forms

from .models import Analysis


def validate_code_line_count(value: str) -> None:
    if not value.strip():
        raise forms.ValidationError("Wklej kod do analizy.")
    if len(value.splitlines()) > 100:
        raise forms.ValidationError("Kod może zawierać maksymalnie 100 linii.")


class AnalysisCreateForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = ["code"]
        widgets = {
            "code": forms.Textarea(
                attrs={
                    "rows": 18,
                    "placeholder": "Wklej fragment kodu (maks. 100 linii)…",
                    "class": "code-input",
                }
            )
        }

    def clean_code(self) -> str:
        code = self.cleaned_data["code"]
        validate_code_line_count(code)
        return code


class AnalysisTitleForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = ["title"]
