from django import forms
from .models import Service

LOW = ("w-full h-11 px-space-md rounded-xl bg-surface-container-low text-on-surface font-body-md "
       "text-body-md focus:bg-surface-container-lowest focus:ring-2 focus:ring-primary outline-none transition-all")
LOWEST = LOW.replace("bg-surface-container-low", "bg-surface-container-lowest")


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ("name", "category", "description", "supplies", "pricing_type", "price",
                  "travel_fee", "has_urgency", "base_city", "radius_km", "lead_time_hours")
        widgets = {
            "name": forms.TextInput(attrs={"class": f"{LOW} pr-10",
                                           "placeholder": "ex. Détection non destructive de fuite d'eau"}),
            "description": forms.Textarea(attrs={
                "class": ("w-full p-space-md rounded-xl bg-surface-container-low text-on-surface font-body-md "
                          "text-body-md focus:bg-surface-container-lowest focus:ring-2 focus:ring-primary "
                          "outline-none transition-all leading-relaxed"),
                "rows": 4,
                "placeholder": "Précisez les phases de travail, les contrôles de sécurité et ce qui n'est pas compris...",
            }),
            "price": forms.NumberInput(attrs={
                "class": f"{LOWEST} font-headline-sm text-headline-sm font-bold pr-12",
                "min": "1", "max": "1500", "step": "0.5"}),
            "travel_fee": forms.Select(attrs={"class": LOWEST}),
            "base_city": forms.TextInput(attrs={"class": LOW, "placeholder": "ex. Tunis"}),
        }