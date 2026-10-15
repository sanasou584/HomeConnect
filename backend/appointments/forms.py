from datetime import datetime, time, timedelta

from django import forms
from django.utils import timezone

from .models import Appointment

FIELD = ("w-full px-4 py-2.5 rounded-lg bg-surface-container-low text-on-surface font-body-md text-body-md "
         "focus:bg-surface-container-lowest focus:outline-none focus:ring-2 focus:ring-primary")


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ("date", "time_slot", "address", "address_details", "access_code", "description", "urgent")
        widgets = {
            "address": forms.TextInput(attrs={"class": f"{FIELD} pl-10", "placeholder": "N°, rue, code postal, ville"}),
            "address_details": forms.TextInput(attrs={"class": FIELD, "placeholder": "Bâtiment, étage, porte"}),
            "access_code": forms.TextInput(attrs={"class": FIELD, "placeholder": "Digicode, nom sur l'interphone"}),
            "description": forms.Textarea(attrs={"class": f"{FIELD} resize-none", "rows": 3,
                                                 "placeholder": "Décrivez la panne ou l'opération demandée..."}),
        }

    def __init__(self, *args, service, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = service

    def clean(self):
        cleaned = super().clean()
        day, slot = cleaned.get("date"), cleaned.get("time_slot")
        if day and slot:
            start = timezone.make_aware(datetime.combine(day, time(int(slot.split("-")[0]))))
            earliest = timezone.now() + timedelta(hours=self.service.lead_time_hours)
            if start < earliest:
                raise forms.ValidationError(
                    f"Ce créneau est trop proche : ce prestataire demande un délai minimum de "
                    f"{self.service.lead_time_hours} h."
                )
        if cleaned.get("urgent") and not self.service.has_urgency:
            cleaned["urgent"] = False
        return cleaned