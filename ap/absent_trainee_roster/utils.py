from datetime import date, timedelta, datetime

from django.template import loader
from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models import Prefetch

from .models import Roster
from accounts.models import User, Trainee
from terms.models import Term
from absent_trainee_roster.models import Entry
from aputils.utils import render_to_pdf

from collections import Counter

TUESDAY = 1
MONDAY = 0
SUNDAY = 6
ONE_DAY = timedelta(1)
TWO_DAYS = timedelta(2)
SEVEN_DAYS = timedelta(7)


def get_or_create_roster(d):
  if Roster.objects.filter(date=d).exists():
    roster = Roster.objects.get(date=d)
  else:
    print 'WARNING: No Roster was made today, creating an empty one for reporting'
    roster = Roster.objects.create_roster(date=d)
    roster.save()

  return roster


def build_report_ctx(date):
  roster = get_or_create_roster(date)
  entries = roster.entry_set.all().order_by('-absentee')

  bro_entries = roster.entry_set.filter(absentee__gender='B').order_by('absentee__firstname', 'absentee__lastname')
  sis_entries = roster.entry_set.filter(absentee__gender='S').order_by('absentee__firstname', 'absentee__lastname')
  bro_unreported_houses = roster.unreported_houses.filter(gender='B')
  sis_unreported_houses = roster.unreported_houses.filter(gender='S')

  trainee_absent_freq, unreported_last_seven_days = calculate_trainee_absent_freq(date)

  return {
      'pagesize': 'letter portrait',
      'roster': roster,
      'bro_entries': bro_entries,
      'sis_entries': sis_entries,
      'genders': User.GENDER,
      'bro_unreported_houses': bro_unreported_houses,
      'sis_unreported_houses': sis_unreported_houses,
      'trainee_absent_freq': trainee_absent_freq,
      'unreported_last_seven_days': unreported_last_seven_days,
  }


def generate_pdf(year, month, day):
  d = date(int(year), int(month), int(day))
  ctx = build_report_ctx(d)
  return render_to_pdf(
      'absent_trainee_roster/generate_roster.html',
      ctx
  )


# calculate how many consecutive days a trainee has been absent going back from today's absence
# Returns: {trainee.id: absent_count,}
def calculate_trainee_absent_freq(date):
  # Get absentees
  roster = get_or_create_roster(date)
  unreported_last_seven_days = set()
  absent_tb = Counter()
  entries = roster.entry_set.prefetch_related(
      'absentee',
      Prefetch(
          'absentee__entry_set',
          queryset=Entry.objects.order_by('-roster__date'), to_attr='sorted_entries'
      )
  )
  for absent_entry in entries:
    absentee = absent_entry.absentee
    d = date
    i = 0
    m = 0
    days = 1
    while d > date - SEVEN_DAYS + ONE_DAY:
      i += 1
      d = date - ONE_DAY * i
      if d.weekday() == MONDAY:
        m = 1
        continue
      r = get_or_create_roster(d)
      absentee.entry_set
      trainees = map(lambda e: e['absentee'], list(r.entry_set.all().values('absentee')))
      is_unreported = absentee.house in r.unreported_houses.all()
      if is_unreported:
        unreported_last_seven_days.add(absentee.id)
      if absentee.id in trainees or is_unreported:
        days += 1 + m
        m = 0
      else:
        break
    absent_tb[absentee.id] = days
  return absent_tb, unreported_last_seven_days


def send_absentee_report(year, month, day):
  d = date(int(year), int(month), int(day))
  if d.weekday() == 0:
    return "Today's a monday, so no absent trainee roster"
  ctx = build_report_ctx(d)

  subject = "Absent Trainee Roster for " + str(d)
  email_template = loader.get_template('absent_trainee_roster/generate_roster.html')

  recipients_emails = settings.ABSENTEE_ROSTER_RECIPIENTS
  email = EmailMessage(subject, email_template.render(ctx), settings.ABSENT_TRAINEE_ROSTER_EMAIL, recipients_emails)
  email.content_subtype = "html"
  pdf_data = generate_pdf(year, month, day)
  email.attach('roster.pdf', pdf_data.content, 'application/pdf')
  email.send(fail_silently=False)

  print 'Absentee report email sent', datetime.now()


def test_send_absentee_report():
  from datetime import date
  t = date.today()
  send_absentee_report(t.year, t.month, t.day)
