from semi.models import SemiAnnual
from semi.utils import ROLL_STATUS, LOCATIONS
from django import forms


class AttendanceForm(forms.Form):

  location = forms.ChoiceField(choices=LOCATIONS)
  tuesday = forms.ChoiceField(choices=ROLL_STATUS, widget=forms.RadioSelect)
  wednesday = forms.ChoiceField(choices=ROLL_STATUS, widget=forms.RadioSelect)
  thursday = forms.ChoiceField(choices=ROLL_STATUS, widget=forms.RadioSelect)
  friday = forms.ChoiceField(choices=ROLL_STATUS, widget=forms.RadioSelect)
  saturday = forms.ChoiceField(choices=ROLL_STATUS, widget=forms.RadioSelect)


class LocationForm(forms.ModelForm):

  OPTIONS = (
      ('Training Center', 'Training Center (with trainees)'),
      ('Ministry Conference Center', 'Ministry Conference Center (with college students and young people)'),
      ('Other', "Other (indicate proposed location, then submit a note to Jerome Keh's mail slot for approval or denial)"),
  )

  location_specific = forms.CharField(max_length=200)

  location = forms.ChoiceField(choices=OPTIONS)

  class Meta:
    model = SemiAnnual
    fields = ['location']
    widgets = {
      "location": forms.RadioSelect,
      "location_specific": forms.HiddenInput()
    }
