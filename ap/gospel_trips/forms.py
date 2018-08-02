from collections import OrderedDict

from aputils.widgets import DatePicker, DatetimePicker
from django import forms
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from .constants import SHOW_CHOICES
from .models import (Answer, AnswerChoice, Destination, GospelTrip,
                     Instruction, LocalImage, Question, Section)
from .utils import get_answer_types


class GospelTripForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(GospelTripForm, self).__init__(*args, **kwargs)

  class Meta:
    model = GospelTrip
    fields = "__all__"
    labels = {
      'name': 'Gospel Trip Name',
    }
    widgets = {
      'open_time': DatetimePicker(),
      'close_time': DatetimePicker()
    }


class LocalImageForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(LocalImageForm, self).__init__(*args, **kwargs)

  class Meta:
    model = LocalImage
    fields = "__all__"


class SectionForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(SectionForm, self).__init__(*args, **kwargs)
    self.fields['show'] = forms.ChoiceField(choices=SHOW_CHOICES)

  class Meta:
    model = Section
    fields = ["name", "show"]


class InstructionForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(InstructionForm, self).__init__(*args, **kwargs)
    self.fields['instruction'].widget.attrs = {'class': 'editor'}

  class Meta:
    model = Instruction
    fields = ["name", "instruction"]


class QuestionForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super(QuestionForm, self).__init__(*args, **kwargs)
    self.fields['answer_type'] = forms.ChoiceField(choices=get_answer_types())
    self.fields['instruction'].widget.attrs = {'class': 'editor'}

  class Meta:
    model = Question
    fields = ["instruction", "answer_type", "answer_required"]


class AnswerForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    if 'gospel_trip__pk' in kwargs:
      gospel_trip = kwargs.pop('gospel_trip__pk')
    super(AnswerForm, self).__init__(*args, **kwargs)
    self.fields['response'] = forms.CharField(widget=forms.Textarea)
    if self.instance.question:
      answer_type = self.instance.question.answer_type
      req = self.instance.question.answer_required

      if answer_type == 'text':
        pass

      elif answer_type == 'destinations':
        choices = []
        choices.extend([(d['id'], d['name']) for d in Destination.objects.filter(gospel_trip=gospel_trip).values('id', 'name')])
        self.fields['response'] = forms.ChoiceField(choices=choices, required=True)

      elif answer_type == 'date':
        self.fields['response'] = forms.DateField(widget=DatePicker())

      elif answer_type == 'datetime':
        self.fields['response'] = forms.DateField(widget=DatetimePicker())

      elif answer_type == 'airports':
        self.fields['response'].widget.attrs = {'class': 'airport-field'}

      elif answer_type == 'airlines':
        self.fields['response'].widget.attrs = {'class': 'airline-field'}

      else:
        try:
          opts = AnswerChoice.objects.get(name=answer_type).options.split(',')
          if req:
            choices = []
          else:
            choices = [('', '---------')]
          choices.extend([(c, c) for c in opts])
          self.fields['response'] = forms.ChoiceField(choices=choices, required=req)
        except AnswerChoice.DoesNotExist:
          pass

  class Meta:
    model = Answer
    fields = ['response', ]


InstructionFormSet = inlineformset_factory(Section, Instruction, form=InstructionForm, extra=1, can_order=True)
QuestionFormSet = inlineformset_factory(Section, Question, form=QuestionForm, extra=1, can_order=True)


class BaseSectionFormset(BaseInlineFormSet):
  def add_fields(self, form, index):
    super(BaseSectionFormset, self).add_fields(form, index)

    # save the formset in the 'nested' property
    form.nested = OrderedDict()
    form.nested['Instructions'] = InstructionFormSet(
        instance=form.instance,
        data=form.data if form.is_bound else None,
        files=form.files if form.is_bound else None,
        prefix='instruction-%s-%s' % (
            form.prefix,
            InstructionFormSet.get_default_prefix()),)

    form.nested['Questions'] = QuestionFormSet(
        instance=form.instance,
        data=form.data if form.is_bound else None,
        files=form.files if form.is_bound else None,
        prefix='question-%s-%s' % (
            form.prefix,
            QuestionFormSet.get_default_prefix()),)

  def is_valid(self):
    result = super(BaseSectionFormset, self).is_valid()

    if self.is_bound:
      for form in self.forms:
        if hasattr(form, 'nested'):
          for _, f in form.nested.items():
            result = result and f.is_valid()

    return result

  def save(self, commit=True):
    result = super(BaseSectionFormset, self).save(commit=commit)

    for form in self.forms:
      if hasattr(form, 'nested'):
        if not self._should_delete_form(form):
          for _, f in form.nested.items():
            f.save(commit=commit)

    return result


SectionFormSet = inlineformset_factory(
  GospelTrip, Section, form=SectionForm,
  formset=BaseSectionFormset, extra=1, can_order=True)
