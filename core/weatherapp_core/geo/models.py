from django.db import models

from weatherapp_core.users.models import User


class Location(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=8, decimal_places=5)
    longitude = models.DecimalField(max_digits=8, decimal_places=5)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_user_name",
                fields=["user", "name"],
                nulls_distinct=False,
            ),
            models.UniqueConstraint(
                name="unique_user_is_default",
                fields=["user", "is_default"],
                nulls_distinct=False,
                condition=models.Q(is_default=True),
            ),
        ]

    def __str__(self) -> str:
        return self.name
