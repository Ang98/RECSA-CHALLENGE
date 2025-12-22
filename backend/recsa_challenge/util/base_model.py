from django.db import models
import uuid
from model_utils.models import TimeStampedModel


class BaseModel(TimeStampedModel):
    is_active = models.BooleanField(verbose_name="¿Activo?", default=True)
    order = models.PositiveIntegerField(verbose_name="Orden", default=1)
    is_deleted = models.BooleanField(verbose_name="¿Eliminado?", default=False)

    # UUID para identificación pública y entre microservicios
    uuid = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True, 
        db_index=True
    )

    class Meta:
        abstract = True
