from django.db import models
from django.contrib.postgres.indexes import GinIndex

# Create your models here.


# USE db_index=True
#  indexes = [
            # GinIndex(name='ProduceGinIndex',fields=['title','keywords','shortDescription','details'],,opclasses=['gin_trgm_ops'])
        # ]