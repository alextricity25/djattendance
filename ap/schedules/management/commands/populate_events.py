from django.core.management.base import BaseCommand
from schedules.models import Event, Schedule

from datetime import time

class Command(BaseCommand):

  # to use: python ap/manage.py populate_events --settings=ap.settings.dev
  def _create_events(self):
    
    #GENERAL HOUSE SCHEDULE
    for i in range(1,7):
      name = "Rise"
      code = "Rise"
      type = "H"
      start = time(6, 30)
      end = time(7, 00)
      weekday = i
      e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='HC')
      e.save()

    for i in [0,1,2,3,5]:
      name = "House Prayer"
      code = "Prayer"
      type = "H"
      start = time(22, 0)
      end = time(22, 10)
      weekday = i
      e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='HC')
      e.save()

    for i in [0,1,2,3,5]:
      name = "Lights Out"
      code = "Lights"
      type = "H"
      start = time(22, 30)
      end = time(22, 45)
      weekday = i
      e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='HC')
      e.save()

    name = "Lights Out"
    code = "Lights"
    type = "H"
    start = time(22, 45)
    end = time(23, 0)
    weekday = 4
    e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='HC')
    e.save()

    name = "Lights Out"
    code = "Lights"
    type = "H"
    start = time(23, 30)
    end = time(23, 45)
    weekday = 6
    e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='HC')
    e.save()

    name = "Curfew"
    code = "Curfew"
    type = "H"
    start = time(22, 30)
    end = time(22, 45)
    weekday = 4
    e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='HC')
    e.save()

    name = "Curfew"
    code = "Curfew"
    type = "H"
    start = time(23, 0)
    end = time(23, 15)
    weekday = 6
    e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='HC')
    e.save()

    name = "PSRP Class"
    code = "PSRP"
    type = "H"
    start = time(16, 30)
    end = time(17, 45)
    weekday = 5
    e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='HC')
    e.save()

    #GENERAL MEAL SCHEDULE
    for i in range(1,7):
      name = "Breakfast"
      code = "BF"
      type = "M"
      start = time(7, 30)
      end = time(7, 45)
      weekday = i
      e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='AM')
      e.save()

    for i in [0,1,2,3,5]:
      name = "Dinner"
      code = "Din"
      type = "M"
      start = time(17, 45)
      end = time(18, 15)
      weekday = i
      e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='AM')
      e.save()

    name = "Lunch"
    code = "Lun"
    type = "M"
    start = time(11, 45)
    end = time(12, 15)
    weekday = 5
    e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='AM')
    e.save()

    #MAIN CLASS SCHEDULE
    class_names = [('FM', 'FM', 'Full Ministry of Christ'), ('GW', 'GW', 'God-ordained Way'), ('GE', 'GE', "God's Economy") , ('SP', 'SP', 'Spirit')]
    i = 0
    type = "C"
    for code, av_code, name in class_names:
      start = time(8, 25)
      end = time(10, 0)
      i += 1
      weekday = i
      e = Event(name=name, av_code=av_code, code=code, type=type, start=start, end=end, weekday=weekday, monitor='AM', class_type='MAIN')
      e.save()

    class_names = {'MV': 'Monday Revival Meeting', 'MM': 'Ministry Meeting' , 'VC': 'Video Class'}

    name = class_names['MV']
    code = "MV"
    type = "C"
    start = time(18, 45)
    end = time(21, 15)
    weekday = 0
    e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='AM', class_type='MAIN')
    e.save()

    name = class_names['MM']
    code = "MM"
    type = "C"
    start = time(19, 20)
    end = time(21, 15)
    weekday = 2
    e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='AM', class_type='MAIN')
    e.save()

    name = class_names['VC']
    code = "VC"
    type = "C"
    start = time(10, 15)
    end = time(11, 45)
    weekday = 5
    e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='AM', class_type='MAIN')
    e.save()

    #1ST YEAR CLASS SCHEDULE
    class_names = [('TG', 'TG', 'Triune God', 1), ('BCI', 'B1', 'Body of Christ I', 3), ('ECI', 'E1', "Experience of Christ as Life I", 4)]
    type = "C"
    for code, av_code, name, weekday in class_names:
      start = time(10, 15)
      end = time(11, 30)
      e = Event(name=name, av_code=av_code, code=code, type=type, start=start, end=end, weekday=weekday, monitor='AM', class_type='1YR')
      e.save()

    #2ND YEAR CLASS SCHEDULE
    class_names = [('BC2', 'B2', 'Body of Christ II', 1), ('LS', 'LS', 'Life of Service', 3), ('EC2', 'E2', 'Experience of Christ as Life II', 4)]
    type = "C"
    for code, av_code, name, weekday in class_names:
      start = time(10, 15)
      end = time(11, 30)
      e = Event(name=name, av_code=av_code, code=code, type=type, start=start, end=end, weekday=weekday, monitor='AM', class_type='2YR')
      e.save()    

    class_names = {'CY': "Children's and Young People's Work"}
    name = class_names['CY']
    code = "CY"
    av_code = 'CY'
    type = "C"
    start = time(8, 25)
    end = time(10, 0)
    weekday = 5
    e = Event(name=name, av_code=av_code, code=code, type=type, start=start, end=end, weekday=weekday, monitor='AM', class_type='1YR')
    e.save()

    class_names = {'NJ': "New Jerusalem"}
    name = class_names['NJ']
    code = "NJ"
    av_code = 'NJ'
    type = "C"
    start = time(8, 25)
    end = time(10, 0)
    weekday = 5
    e = Event(name=name, av_code=av_code, code=code, type=type, start=start, end=end, weekday=weekday, monitor='AM', class_type='2YR')
    e.save()

    #1ST YEAR GREEK SCHEDULE
    for i in [1, 3]:
      name = ["Greek I", "Greek II", "German", "Character"]
      code = ["GK I", "GK II", "GER", "CHAR"]
      type = "C"
      start = time(16, 45)
      end = time(17, 45)
      weekday = i
      for j in range(0,3):
        e = Event(name=name[j], code=code[j], type=type, start=start, end=end, weekday=weekday, monitor='AM', class_type='AFTN')
        e.save()

    # Campus schedule
    for i in range(1,4):
      name = "Campus Work Time"
      code = "CP Work"
      type = "T"
      start = time(12, 30)
      end = time(14, 00)
      weekday = i
      e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor="TM")
      e.save()

    #Team Fellowship
    name = "Campus Team Fellowship"
    code = "TF"
    type = "T"
    start = time(10, 30)
    end = time(12, 00)
    weekday = 2
    e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='TM')
    e.save()

    #Prayer Meeting
    name = "Prayer Meeting"
    code = "PM"
    type = "T"
    start = time(19, 00)
    end = time(21, 30)
    weekday = 1
    e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='TM')
    e.save()

    #Home Meeting
    name = "Home Meeting"
    code = "HM"
    type = "T"
    start = time(18, 30)
    end = time(21, 30)
    weekday = 4
    e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='TM')
    e.save()

    # Study
    name = "Campus Study"
    code = "CP Study"
    type = "S"
    start = time(16, 15)
    end = time(16, 45)
    weekday = 1
    e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='TM')
    e.save()

    name = "Campus Study"
    code = "Study"
    type = "S"
    start = time(16, 30)
    end = time(17, 45)
    weekday = 2
    e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='TM')
    e.save()

    name = "Campus Work"
    code = "CP Work"
    type = "T"
    start = time(16, 30)
    end = time(17, 45)
    weekday = 4
    e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='TM')
    e.save()

    name = "Campus Study"
    code = "CP Study"
    type = "S"
    start = time(14, 15)
    end = time(16, 15)
    weekday = 5
    e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='TM')
    e.save()

    # Evening Study
    for i in [3, 5]:
      name = "Campus Study"
      code = "CP Study"
      type = "S"
      start = time(18, 45)
      end = time(21, 15)
      weekday = i
      e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='TM')
      e.save()

    # Team only Fellowship
    name = "Campus Team Only Fellowship"
    code = "Team Fellowship"
    type = "T"
    start = time(16, 00)
    end = time(17, 45)
    weekday = 6
    e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='TM')
    e.save()

    # group events for Group Events schedule
    for i in range(1, 6):
      name = "Session I"
      code = "SESS1"
      type = 'C'
      start = time(8, 25)
      end = time(10, 0)
      weekday = i
      description = "generic first session for group events"
      e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='AM', description=description)
      e.save()

    
    for i in range(1, 5):
      name = "Session II"
      code = "SESS2"
      type = 'C'
      start = time(10, 15)
      end = time(11, 30)
      weekday = i
      description = "generic second session for group events"
      e = Event(name=name, code=code, type=type, start=start, end=end, weekday=weekday, monitor='AM', description=description)
      e.save()

      name = "Session II"
      code = "SESS2"
      type = 'C'
      start = time(10, 0)
      end = time(11, 45)
      description = "generic second session for group events"
      e = Event(name=name, code=code, type=type, start=start, end=end, weekday=5, monitor='AM', description=description)
      e.save()

    times = [time(16, 15), time(16, 30), time(16, 45)]
    for i in range(1, 4):
      name = "YPC Work"
      code = "YPCW"
      type = 'T'
      start = time(14, 15)
      description = "generic second afternoon session for group events"
      e = Event(name=name, code=code, type=type, start=start, end=times[i-1], weekday=i, monitor='', description=description)
      e.save()

    name = "Team Fellowship"
    code = "TF"
    type = 'T'
    start = time(14, 15)
    end = time(17, 45)
    description = "generic second session for group events"
    e = Event(name=name, code=code, type=type, start=start, end=end, weekday=4, monitor='TM', description=description)
    e.save()

    name = "Lang/Char"
    code = "LANG/CHAR"
    type = 'C'
    start = time(16, 45)
    end = time(17, 45)
    description = "Greek or German or Character class"
    for i in [1, 3]:
      e = Event(name=name, code=code, type=type, start=start, end=end, weekday=i, monitor='AM', description=description)
      e.save()

  def handle(self, *args, **options):
    Event.objects.all().delete()
    print("* Populating events...")
    self._create_events()