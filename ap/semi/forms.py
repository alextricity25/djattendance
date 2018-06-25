from semi.models import SemiAnnual
from django import forms


class AttendanceForm(forms.Form):

  ROLL_STATUS = (
      ('A', 'Attended'),
      ('S', 'Service'),
      ('I', 'Illness'),
      ('F', 'Fellowship'),
      ('U', 'Unexcused Absence')
  )

  tuesday = forms.ChoiceField(choices=ROLL_STATUS, widget=forms.RadioSelect, required=False)
  wednesday = forms.ChoiceField(choices=ROLL_STATUS, widget=forms.RadioSelect, required=False)
  thursday = forms.ChoiceField(choices=ROLL_STATUS, widget=forms.RadioSelect, required=False)
  friday = forms.ChoiceField(choices=ROLL_STATUS, widget=forms.RadioSelect, required=False)
  saturday = forms.ChoiceField(choices=ROLL_STATUS, widget=forms.RadioSelect, required=False)


class LocationForm(forms.ModelForm):

  LOCATIONS = (
      ('Training Center', 'Training Center (with trainees)'),
      ('Ministry Conference Center', 'Ministry Conference Center (with college students and young people)'),
      ('Other', "Other (indicate proposed location, then submit a note to Jerome Keh's mail slot for approval or denial)"),
  )

  location_specific = forms.CharField(max_length=200)

  location = forms.ChoiceField(choices=LOCATIONS)

  class Meta:
    model = SemiAnnual
    fields = ['location']
    widgets = {
      "location": forms.RadioSelect,
      "location_specific": forms.HiddenInput()
    }
