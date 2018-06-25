# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from accounts.models import Trainee
from aputils.trainee_utils import is_trainee, trainee_from_user
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from semi.models import SemiAnnual
from semi.forms import AttendanceForm
from django.shortcuts import get_object_or_404
from terms.models import Term


# Create your views here.
def attendance_base(request):
  term = Term.current_term()
  if is_trainee(request.user):
    trainee = trainee_from_user(request.user)
  else:
    trainee = Trainee.objects.first()
  semi, created = SemiAnnual.objects.get_or_create(trainee=trainee, term=term)
  return HttpResponseRedirect(reverse('semi:attendance', kwargs={'pk': semi.pk}))


class AttendanceUpdate(TemplateView):
  template_name = 'semi/attendance_form.html'
  semi = None

  def get(self, request, *args, **kwargs):
    self.semi = get_object_or_404(SemiAnnual, pk=self.kwargs['pk'])
    return super(AttendanceUpdate, self).get(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    self.semi = get_object_or_404(SemiAnnual, pk=self.kwargs['pk'])
    form = AttendanceForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      self.semi.location = data.pop('location')
      for k, v in data.items():
        if v:
          self.semi.attendance[k] = v
      self.semi.save()
    context = self.get_context_data()
    return super(AttendanceUpdate, self).render_to_response(context)

  def get_context_data(self, **kwargs):
    context = super(AttendanceUpdate, self).get_context_data(**kwargs)
    init = self.semi.attendance
    init.update({'location': self.semi.location})
    context['form'] = AttendanceForm(initial=init)
    context['term'] = self.semi.term
    context['page_title'] = "Personal Study Attendance Form"
    context['button_label'] = "Save"
    return context
