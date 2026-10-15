from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

TRAVEL_FEE_CHOICES = [
    (0, "Inclus dans la zone d'intervention (0 €)"),
    (20, "Forfait standard zone proche (+20 €)"),
    (35, "Zone élargie > 25 km (+35 €)"),
    (50, "Déplacement grand couronne (+50 €)"),
]


class Service(models.Model):
    class Category(models.TextChoices):
        PLUMBING = "plomberie", "Plomberie & Sanitaire"
        ELECTRICITY = "electricite", "Électricité générale"
        LOCKSMITH = "serrurerie", "Serrurerie & Dépannage"
        PAINTING = "peinture", "Peinture & Finition"
        HEATING = "chauffage", "Chauffage & Climatisation"
        GARDENING = "jardinage", "Jardinage & Aménagement"

    class Supplies(models.TextChoices):
        PROVIDER = "artisan", "Fournies par l'artisan"
        CLIENT = "client", "À la charge du client"
        QUOTE = "devis", "Au choix après diagnostic"

    class PricingType(models.TextChoices):
        HOURLY = "horaire", "Tarif horaire"
        FIXED = "forfait", "Forfait fixe"
        QUOTE = "devis", "Sur devis libre"

    class LeadTime(models.IntegerChoices):
        H2 = 2, "2 heures"
        H12 = 12, "12 heures"
        H24 = 24, "24 heures"
        H48 = 48, "48 heures"

    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="services", limit_choices_to={"role": "provider"},
    )
    name = models.CharField("Intitulé précis de la prestation", max_length=100)
    category = models.CharField("Catégorie", max_length=20, choices=Category.choices)
    description = models.TextField("Description détaillée", blank=True, max_length=1000)
    supplies = models.CharField("Fournitures", max_length=10, choices=Supplies.choices,
                                default=Supplies.PROVIDER)
    pricing_type = models.CharField("Mode de facturation", max_length=10,
                                    choices=PricingType.choices, default=PricingType.HOURLY)
    price = models.DecimalField("Montant brut facturé (€ HT)", max_digits=8, decimal_places=2,
                                validators=[MinValueValidator(Decimal("0.01"))])
    travel_fee = models.PositiveSmallIntegerField("Frais de déplacement",
                                                  choices=TRAVEL_FEE_CHOICES, default=20)
    has_urgency = models.BooleanField("Intervention d'urgence", default=False)
    base_city = models.CharField("Ville de départ", max_length=100)
    radius_km = models.PositiveSmallIntegerField(
        "Rayon d'action (km)", default=20,
        validators=[MinValueValidator(5), MaxValueValidator(80)],
    )
    lead_time_hours = models.PositiveSmallIntegerField(
        "Délai minimum", choices=LeadTime.choices, default=LeadTime.H24,
    )
    is_active = models.BooleanField("Publié", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"