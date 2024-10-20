from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from weatherapp_core.users.models import User


class Location(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_user_name",
                fields=["user", "name"],
                nulls_distinct=False,
            ),
        ]

    def __str__(self) -> str:
        return self.name

    async def aget_default_for(self, user: User) -> bool:
        return await self.default_for.filter(user=user).aexists()

    async def aset_default_for(self, user: User) -> None:
        await DefaultLocation.objects.aupdate_or_create(
            user=user,
            defaults={"location": self},
        )


class DefaultLocation(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="default_location"
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="default_for"
    )

    def __str__(self) -> str:
        return str(self.location)
