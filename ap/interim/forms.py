from django import forms

from interim.models import InterimIntentions, InterimItinerary, InterimIntentionsAdmin
from aputils.widgets import DatePicker, DatetimePicker


class InterimItineraryForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(InterimItineraryForm, self).__init__(*args, **kwargs)
    self.fields['start'].required = True
    self.fields['end'].required = True

  class Meta:
    model = InterimItinerary
    fields = ["start", "end", "comments", ]
    widgets = {
      "start": DatePicker(),
      "end": DatePicker(),
    }


class InterimIntentionsForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(InterimIntentionsForm, self).__init__(*args, **kwargs)
    self.fields['cell_phone'].label = 'Cell Phone'
    self.fields['email'].label = 'E-mail'
    self.fields['home_phone'].label = 'Home Phone'
    self.fields['home_locality'].label = 'Home Locality'
    self.fields['home_address'].label = 'Home Address'
    self.fields['home_city'].label = 'City'
    self.fields['home_state'].label = 'State'
    self.fields['home_zip'].label = 'Zip'
    self.fields['intent'].label = 'Intent to Return'
    self.fields['post_training_intentions'].label = 'Post Training Intentions'
    self.fields['post_intent_comments'].label = 'Explain'

  class Meta:
    model = InterimIntentions
    fields = ["cell_phone", "email", "home_phone", "home_locality", "home_address", "home_city", "home_state", "home_zip", "intent", "post_training_intentions", "post_intent_comments"]
    widgets = {
      "intent": forms.RadioSelect,
    }


class InterimIntentionsAdminForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(InterimIntentionsAdminForm, self).__init__(*args, **kwargs)
    self.fields['date_1yr_return'].required = True
    self.fields['date_2yr_return'].required = True
    self.fields['earliest_arrival_date'].required = True
    self.fields['term_begin_date'].required = True

  class Meta:
    model = InterimIntentionsAdmin
    fields = ["open_time", "close_time", "date_1yr_return", "date_2yr_return", "earliest_arrival_date", "term_begin_date"]
    widgets = {
      "open_time": DatetimePicker(),
      "close_time": DatetimePicker(),
      "date_1yr_return": DatetimePicker(),
      "date_2yr_return": DatetimePicker(),
      "earliest_arrival_date": DatePicker(),
      "term_begin_date": DatePicker()
    }
