from django.db import models
from django.db.models.functions import Coalesce
from django.db.models import Avg

from datetime import timedelta, date

from terms.models import Term

import services

from django.utils.functional import cached_property


# Has: assignments
class WeekSchedule(models.Model):
  class Meta:
    ordering = ['-start']

  """
  A service schedule for one week in the training.
  """

  # Hold id's of exceptions disabled this week
  # exception_blacklist =

  start = models.DateField()  # should be the Tuesday of every week
  description = models.TextField(blank=True, null=True)
  # period = models.ForeignKey(Period)  # ???Can't we get this from start?

  # line of encouragement in the beginning
  encouragement = models.TextField(blank=True, null=True)

  # workload calculations
  workload_margin = models.PositiveSmallIntegerField(default=2)

  # exceptions inactive for just this week
  silenced_exceptions = models.ManyToManyField('ServiceException', blank=True, verbose_name='Exceptions to ignore this week')

  #TODO
  # # average workload for this schedule
  @property
  def avg_workload(self):
    return self.assignments.aggregate(avg_workload=Coalesce(Avg('workload'), 0))['avg_workload'] / services.models.Worker.objects.count()

  # Prevent from working way above the average trainee workload (standard of deviation)
  # avg_workload + margin = workload ceiling
  @property
  def workload_ceiling(self):
    return self.avg_workload + self.workload_margin

  ## Info on scheduler who created the schedule and info on last modified
  scheduler = models.ForeignKey('accounts.Trainee', on_delete=models.SET_NULL, null=True)
  last_modified = models.DateTimeField(auto_now=True)

  @staticmethod
  def get_or_create_current_week_schedule(scheduler):
    ct = Term.current_term()
    current_week = ct.term_week_of_date(date.today())
    return WeekSchedule.get_or_create_week_schedule(scheduler, current_week)

  @staticmethod
  def get_or_create_week_schedule(scheduler, week_number):
    ct = Term.current_term()
    # service week starts on Tuesdays rather than Mondays
    start = ct.get_date(int(week_number), 1)
    if WeekSchedule.objects.filter(start=start).exists():
      week_schedule = WeekSchedule.objects.get(start=start)
    else:
      week_schedule = WeekSchedule(start=start, scheduler=scheduler)
      week_schedule.save()
    return week_schedule

  @cached_property
  def week_range(self):
    week_start = self.start
    week_end = self.start + timedelta(days=6)
    return (week_start, week_end)

  @staticmethod
  def latest_week_schedule():
    return WeekSchedule.objects.latest('start')

  @staticmethod
  def current_week_schedule():
    t = date.today()
    ct = Term.current_term()
    if ct.is_date_within_term(t):
      week = ct.term_week_of_date(t)
      # service week starts on Tuesdays rather than Mondays
      start = ct.startdate_of_week(week) + timedelta(days=1)
      if WeekSchedule.objects.filter(start=start).exists():
        return WeekSchedule.objects.get(start=start)
      else:
        return None

  def __unicode__(self):
    return 'Week Schedule - ' + str(self.start)

  @classmethod
  def create(cls, start, desc, period):
    schedule = cls(start=start, desc=desc, period=period)

    # create instances
    for sv in self.period.services:
      inst = Instance(service=sv, period=self.period)
      # since the week starts on Tuesday, add 6 and modulo 7 to get the
      # delta
      inst.date = self.start + \
        timedelta(days=((int(sv.weekday) + 6) % 7))
      inst.save()
      self.instances.add(inst)  # add created instance to this schedule

    return schedule

  def assign_designated_services(self):
    # assign designated services
    for dsv in self.instances.filter(service__designated=True):
      dsv.workers.add(dsv.service.designated_workers)

  def calculate_solution_space(self):
    # calculate solution space
    for worker in Worker.objects.filter(active=True):
      # clear any old eligibility data (e.g. from previous week)
      worker.services_eligible.clear()

      # if over workload ceiling, not eligible for any services, so skip
      if worker.workload >= self.workload_ceiling:
        continue

      # first assume everyone is eligible for every service
      worker.services_eligible.add(self.instances.all())

      # then remove based on exceptions
      worker.services_eligible.remove(worker.services_exempted)

      # remove based on gender
      if worker.account.gender == 'B':
        worker.services_eligible.remove(
          self.instances.filter(service__gender='S'))
      else:
        worker.services_eligible.remove(
          self.instances.filter(service__gender='B'))

  def assign(self, workers, instance, role='wor', commit=False):
    """ assign workers to a service instance """

    warnings = list()
    # convert to list if passed single worker
    if type(workers) is not list: workers = [workers]

    for worker in workers:
      # check worker's exceptions against instance
      for exception in worker.exceptions:
        if not exception.checkException(worker, instance):
          warnings.append(LogEvent.exception_violated(
            self, exception, instance, worker))

      # check worker's new workload versus workload ceiling
      if (worker.workload + instance.workload) > self.workload_ceiling:
        warnings.append(LogEvent.workload_excessive(
          self, instance, worker, worker.workload + instance.workload))

      if commit:  # dry-run by default to preview warnings
        Assignment(instance=instance, worker=worker, role=role,
               schedule=self).save()  # assign worker to instance
        for warning in warnings:
          warning.save()  # write warnings to log
        # recalculate solution space
        if worker.workload > self.workload_ceiling:
          worker.services_eligible.clear()
        else:
          # remove same-day services
          worker.services_eligible.remove(self.instances.filter(date=instance.date))
        worker.save()

    return warnings

  def unassign(self, worker, instance):
    """ unassign a worker from a service instance """

    # delete service assignment
    Assignment.objects.get(instance=instance, worker=worker).delete()
    # restore workload
    worker.workload -= instance.workload

    if worker.workload > self.workload_ceiling:
      worker.save()
      return  # terminate early

    # otherwise, rebuild solution space for this worker:
    # add all services again
    worker.services_eligible.add(self.instances.all())
    # then remove based on exceptions
    worker.services_eligible.remove(worker.services_exempted)
    # remove based on gender
    if worker.account.gender == 'B':
      worker.services_eligible.remove(
        self.instances.filter(service__gender='S'))
    else:
      worker.services_eligible.remove(
        self.instances.filter(service__gender='B'))

    # then simulate reassigning current services
    for inst in worker.instance_set:
      worker.services_eligible.remove(self.instances.filter(date=inst.date))


  def heuristic(self, instance, pick=1):
    """ heuristic to choose a worker from an instance's eligible workers """

    workers=instance.workers_eligible.annotate(
      num_eligible=Count('services_eligible'))

    # sort by:
    # how many services the trainee is elilgible for
    # trainee's current workload
    workers.order_by('workload', 'num_eligible')
    return workers[:pick]


  def fill(self, instances):
    """ takes a list of instances and automatically assigns workers to them """

    # yes, i know nested loops are bad.
    while not instances:
      # sorts instances by number of eligilble workers
      instance=instances.sort(
        key=lambda inst: inst.workers_eligible.count()).pop()
      while not instance.filled and instance.workers_eligible > 0:
        if instance.workers_eligible <= instance.workers_needed:
          # assign everyone if not enough workers
          assign(instance.workers_eligible, instance, commit=True)
        else:
          assign(heuristic(instance, pick=1), instance, commit=True)

  def validate(self):
    """ validate this schedule, report any warnings """
    LogEvent.info(self, "beginning validation").save()

    # check instances are filled
    for instance in self.instances:
      if not instance.filled:
        LogEvent.instance_unfilled(self, instance)
      else:
        continue

    for worker in Workers.objects.filter(active=True):
      # check each workers assignments against exceptions
      if worker.services_exempted and worker.assignment_set.filter(schedule=self).values('service'):
        pass
        # issue exception warnings

      # check workload ceilings
      if worker.workload > self.workload_ceiling:
        LogEvent.workload_excessive(self, worker).save()

  def finalize(self):
    Workers.objects.filter(active=True).update(weeks=F('weeks') + 1)
    self.validate()
