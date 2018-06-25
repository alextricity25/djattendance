# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from accounts.models import Trainee
from terms.models import Term
from django.db import models
from django.contrib.postgres.fields import JSONField


def default_attendance():
  return {"tuesday": "N", "wednesday": "N", "thursday": "N", "friday": "N", "saturday": "N"}


class SemiAnnual(models.Model):

  trainee = models.ForeignKey(Trainee)

  term = models.ForeignKey(Term)

  attendance = JSONField(default=default_attendance())

  location = models.CharField(max_length=200, blank=True)
