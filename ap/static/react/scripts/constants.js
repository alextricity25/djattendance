import dateFns from 'date-fns'

//constants

export const ATTENDANCE_MONITOR_GROUP = 4

export const ATTENDANCE_STATUS = [
  {id: 'P', name: 'Present'},
  {id: 'A', name: 'Absent'},
  {id: 'T', name: 'Tardy'},
  {id: 'U', name: 'Uniform'},
  {id: 'L', name: 'Left Class'},
]

export const ATTENDANCE_STATUS_LOOKUP = {
    'P': 'present',
    'A': 'absent',
    'T': 'tardy',
    'U': 'uniform',
    'L': 'left-class'
}

export const SLIP_STATUS_LOOKUP = {
    'A': 'approved',
    'P': 'pending',
    'F': 'fellowship',
    'D': 'denied',
    'S': 'approved' //by TA sister
}

export const SLIP_TYPES = [
  {id: 'SICK', name: 'Sickness'},
  {id: 'SERV', name: 'Service'},
  {id: 'FWSHP', name: 'Fellowship'},
  {id: 'NIGHT', name: 'Night Out'},
  {id: 'MEAL', name: 'Meal Out'},
  {id: 'INTVW', name: 'Interview'},
  {id: 'GOSP', name: 'Gospel'},
  {id: 'CONF', name: 'Conference'},
  {id: 'WED', name: 'Wedding'},
  {id: 'FUNRL', name: 'Funeral'},
  {id: 'SPECL', name: 'Special'},
  {id: 'OTHER', name: 'Other'},
  {id: 'EMERG', name: 'Family Emergency'},
  {id: 'NOTIF', name: 'Notification Only'},
]

export const TA_IS_INFORMED = {'id': 'true', 'name': 'TA informed'}

export const INFORMED = [
  TA_IS_INFORMED,
  {id: 'false', name: 'Did not inform training office'},
  {id: 'texted', name: 'Texted attendance number (for sisters during non-front office hours only)'},
]

export const SLIP_TYPE_LOOKUP = {
    'CONF': 'Conference',
    'EMERG': 'Family Emergency',
    'FWSHP': 'Fellowship',
    'FUNRL': 'Funeral',
    'GOSP': 'Gospel',
    'INTVW': 'Grad School/Job Interview',
    'GRAD': 'Graduation',
    'MEAL': 'Meal Out',
    'NIGHT': 'Night Out',
    'OTHER': 'Other',
    'SERV': 'Service',
    'SICK': 'Sickness',
    'SPECL': 'Special',
    'WED': 'Wedding',
    'NOTIF': 'Notification Only'
}

export const FA_ICON_LOOKUP = {
    "pending": "refresh",
    "denied": "minus-square",
    "approved": "check-square-o"
}

export function joinValidClasses(classes) {
  return _.compact(classes).join(' ');
};

export function categorizeEventStatus(wesr) {
  //absenses unexcused
  var status = ''
  if(wesr[i].slip === null) {
    status = 'unexcused'
  } else if(wesr[i].slip["status"] == "D" || wesr[i].slip["status"] == "P" || wesr[i].slip["status"] == "F") {
    status = 'pending'
  } else if(wesr[i].slip && wesr[i].slip["status"] == "A") {
    status = 'approved'
  }

  if(wesr[i].roll && wesr[i].roll["status"] == "A") {
    status += " absent"
  } else if(wesr[i].roll && (wesr[i].roll["status"] == "T" || wesr[i].roll["status"] == "U" || wesr[i].roll["status"] == "L")) {
    status += "tardy"
  }
  return status
}

export function canSubmitRoll(dateDetails) {
  let weekStart = dateDetails.weekStart
  let weekEnd = dateFns.addDays(dateDetails.weekEnd, 1)
  let rollDate = new Date()
  return (rollDate >= weekStart && rollDate <= weekEnd)
}

// this is necessary because Roll.date and Event dates are given as Date, not Datetime, from django
export function getDateWithoutOffset(dateWithOffset) {
  let millsecsInMinute = 60000
  let dateWithoutOffset = new Date(dateWithOffset.getTime() + dateWithOffset.getTimezoneOffset() * 60000)
  return dateWithoutOffset
}

export function canFinalizeRolls(rolls, dateDetails) {
  let weekStart = dateDetails.weekStart
  let weekEnd = dateDetails.weekEnd
  let isWeekFinalized = rolls.filter(function(roll) {
    let rollDate = getDateWithoutOffset(new Date(roll.date))
    return rollDate >= weekStart && rollDate <= weekEnd && roll.finalized
  }).length > 0
  let now = new Date()
  // Monday midnight is when you can begin finalizing
  let isPastMondayMidnight = now >= weekEnd
  // Tuesday midnight is when you can no longer finalize
  weekEnd = dateFns.addDays(weekEnd, 1)
  let isBeforeTuesdayMidnight = now <= weekEnd
  let canFinalizeWeek = !isWeekFinalized && isPastMondayMidnight && isBeforeTuesdayMidnight
  return canFinalizeWeek
}

export const compareLeaveslipEvents = (e1, e2) => {
  return new Date(e1.date) < new Date(e2.date) ? -1 : 1
}

export const compareEvents = (e1, e2) => {
  return new Date(e1.start_datetime) < new Date(e2.start_datetime) ? -1 : 1
}

export const compareLeaveslips = (ls1, ls2) => {
  let ls1Date = new Date(ls1.events.sort(compareLeaveslipEvents).slice(-1)[0].date)
  let ls2Date = new Date(ls2.events.sort(compareLeaveslipEvents).slice(-1)[0].date)
  return ls1Date < ls2Date ? -1 : 1
}

export function lastLeaveslip(leaveslips, type, status) {
  let matchingSlips = leaveslips.filter((ls) => {
    return ls.status == status && ls.type == type
  })
  return matchingSlips.sort(compareLeaveslips).slice(-1)[0]
}
