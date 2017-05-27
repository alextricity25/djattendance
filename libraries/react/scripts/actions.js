//we shouldn't have initiatestate in here...
import initialState from './initialstate'
import { getDateDetails } from './selectors/selectors.js'

import {format} from 'date-fns'

// for a reading on why you need this boilerplate, see
// http://redux.js.org/docs/recipes/ReducingBoilerplate.html

export const TOGGLE_LEGEND = 'TOGGLE_LEGEND'
export const toggleLegend = () => {
  return {
    type: TOGGLE_LEGEND
  }
}

export const selectPeriod = (period) => {
  return (dispatch, getState) => {
    let dateDetails = getDateDetails(getState())
    dispatch(changeDate((period - dateDetails.period) * 14))
  }
}

export const CHANGE_DATE = 'CHANGE_DATE'
export const changeDate = (days) => {
  return {
    type: CHANGE_DATE,
    days: days
  }
}

export const TOGGLE_EVENT = 'TOGGLE_EVENT'
export const toggleEvent = (ev) => {
  return {
    type: TOGGLE_EVENT,
    event: ev
  };
}

export const DESELECT_ALL_EVENTS = 'DESELECT_ALL_EVENTS'
export const deselectAllEvents = () => {
  return {
    type: DESELECT_ALL_EVENTS
  };
}

export const FINALIZE_ROLL = 'FINALIZE_ROLL'
export const finalizeRoll = () => {
  return function(dispatch, getState) {
    let dateDetails = getDateDetails(getState())
    // rename the post data here to keep django api clean for future reuse
    dateDetails.trainee = getState().form.traineeView
    dateDetails.submitter = getState().trainee
    return $.ajax({
      url: '/attendance/api/rolls/finalize/',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(dateDetails),
      success: function(data, status, jqXHR) {
        dispatch(submitRoll(data.rolls))
      },
      error: function(jqXHR, textStatus, errorThrown) {
        console.log('Roll post error!');
        console.log(jqXHR, textStatus, errorThrown);
      }
    })
  }
}

// RollSlip has fields {rollStatus, slipType, comments, informed, TAInformed}
// slipId is determine between POST (new slip, slipId == null) or PUT (update slip, slipId != null)
export const postRollSlip = (rollSlip, selectedEvents, slipId) => {
  if ((rollSlip.rollStatus !== undefined || rollSlip.rollStatus != "") && (rollSlip.slipType === undefined || rollSlip.slipType == "")) {
    return function(dispatch) {
      dispatch(postRoll(rollSlip, selectedEvents));
    }
  } else if ((rollSlip.rollStatus === undefined || rollSlip.rollStatus == "") && (rollSlip.slipType !== undefined || rollSlip.slipType != "")) {
    return function(dispatch) {
      dispatch(postLeaveSlip(rollSlip, selectedEvents, slipId));
    }
  } else if ((rollSlip.rollStatus !== undefined || rollSlip.rollStatus != "") && (rollSlip.slipType !== undefined || rollSlip.slipType != "")) {
    return function(dispatch) {
      dispatch(postRoll(rollSlip, selectedEvents, slipId, true));
    }
  } else {
    dispatch(receiveResponse('Error no data for roll or slips'));
  }
}

export const SUBMIT_ROLL = 'SUBMIT_ROLL'
export const submitRoll = (rolls) => {
  return {
    type: SUBMIT_ROLL,
    rolls: rolls
  }
}

export const RESET_ROLL_FORM = 'RESET_ROLL_FORM'
export const resetRollForm = () => {
  return {
    type: RESET_ROLL_FORM
  };
}

export const RESET_LEAVESLIP_FORM = 'RESET_LEAVESLIP_FORM'
export const resetLeaveslipForm = () => {
  return {
    type: RESET_LEAVESLIP_FORM
  };
}

export const RESET_GROUPSLIP_FORM = 'RESET_GROUPSLIP_FORM'
export const resetGroupslipForm = () => {
  return {
    type: RESET_GROUPSLIP_FORM
  };
}
export const postRoll = (values) => {
  var rolls = [];
  var roll = {
    "event": null,
    "trainee": values.traineeView ? values.traineeView.id : values.trainee.id,
    "status": values.rollStatus.id,
    "finalized": false,
    "notes": "",
    "submitted_by": values.trainee.id,
    "last_modified": Date.now(),
    "date": null
  }
  let selectedEvents = values.selectedEvents;
  if (selectedEvents.length == 0) {
    //need to create an error action
    return function(dispatch) {
      dispatch(receiveResponse('error no events selected'));
    }
  } else {
    for (var i = 0; i < selectedEvents.length; i++) {
      rolls.push(Object.assign({}, roll, {
        event: selectedEvents[i].id,
        date: format(selectedEvents[i].start_datetime, 'YYYY-MM-DD')
      }));
    }
  }
  return function(dispatch) {
    var data = null;
    if (rolls.length == 1) {
      data = rolls[0];
    } else {
      data = JSON.stringify(rolls);
    }

    return $.ajax({
      url: '/api/rolls/',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(rolls),
      success: function(data, status, jqXHR) {
        dispatch(submitRoll(rolls));
        dispatch(resetRollForm());
      },
      error: function(jqXHR, textStatus, errorThrown) {
        console.log('Roll post error!');
        console.log(jqXHR, textStatus, errorThrown);
      }
    });
  }
}

export const CHANGE_ROLL_FORM = 'CHANGE_ROLL_FORM'
export const changeRollForm = (values) => {
  return {
    type: CHANGE_ROLL_FORM,
    values: values,
  }
}

export const UPDATE_TRAINEE_VIEW = 'UPDATE_TRAINEE_VIEW'
export const updateTraineeView = (trainee) => {
  return {
    type: UPDATE_TRAINEE_VIEW,
    traineeView: trainee
  }
}

export const UPDATE_EVENTS = 'UPDATE_EVENTS'
export const updateEvents = (events) => {
  return {
    type: UPDATE_EVENTS,
    eventsView: events
  }
}

export const UPDATE_ATTENDANCE = 'UPDATE_ATTENDANCE'
export const updateAttendance = (attendance) => {
  return {
    type: UPDATE_ATTENDANCE,
    attendance: attendance
  }
}

export const CHANGE_TRAINEE_VIEW = 'CHANGE_TRAINEE_VIEW'
export const changeTraineeView = (trainee) => {
  return function(dispatch) {
    dispatch(updateTraineeView(trainee))
    $.ajax({
      url: '/api/events',
      type: 'GET',
      data: {
        trainee: trainee.id
      },
      success: function(data, status, xhr) {
        dispatch(deselectAllEvents())
        dispatch(updateEvents(data))
      },
      error: function(xhr, status, error) {
        console.log('events error')
        console.log(xhr, status, error);
      }
    })
    $.ajax({
      url: '/api/attendance',
      type: 'GET',
      data: {
        trainee: trainee.id
      },
      success: function(data, status, xhr) {
        // this returns a list of trainees so just grab the first
        dispatch(updateAttendance(data[0]))
      },
      error: function(xhr, status, error) {
        console.log('attendance error')
        console.log(xhr, status, error)
      }
    })
  }
}

export const CHANGE_LEAVESLIP_FORM = 'CHANGE_LEAVESLIP_FORM'
  //values here is all the values of the form
export const changeLeaveSlipForm = (values) => {
  return {
    type: CHANGE_LEAVESLIP_FORM,
    values: values
  }
}
export const CHANGE_GROUPSLIP_FORM = 'CHANGE_GROUPSLIP_FORM'
  //values here is all the values of the form
export const changeGroupSlipForm = (values) => {
  return {
    type: CHANGE_GROUPSLIP_FORM,
    values: values
  }
}

export const SUBMIT_LEAVESLIP = 'SUBMIT_LEAVESLIP'
export const submitLeaveSlip = (slip) => {
  // patch uses a list, post doesn't
  // use a list for the reducer
  slip = !(slip[0]) ? [slip] : slip
  return {
    type: SUBMIT_LEAVESLIP,
    leaveslips: slip
  }
}

export const postLeaveSlip = (values) => {
  var event_details = values.selectedEvents.map(e => ({
    id: e.id,
    date: format(e.start_datetime, 'YYYY-MM-DD'),
    name: e.name,
  }))
  var texted = false;
  if (values.ta_informed.id == "texted") {
    texted = true;
    values.ta_informed = false;
  } else if (values.ta_informed.id != "true") {
    values.ta_informed = false;
  }
  var slip = {
    "type": values.slipType.id,
    "status": "P",
    "TA": values.ta.id,
    "trainee": values.trainee.id,
    "submitted": Date.now(),
    "last_modified": Date.now(),
    "finalized": null,
    "description": "",
    "comments": values.comment,
    "texted": texted,
    "informed": values.ta_informed.id,
    "events": event_details,
    "location": values.location,
    "host_name": values.hostName,
    "host_phone": values.hostPhone,
    "hc_notified": values.hcNotified,
  };

  return (dispatch, getState) => {
    let slipId = getState().form.leaveSlip.id || null
    let ajaxType = slipId ? 'PUT' : 'POST'
    slip.id = slipId
    slip = slipId ? [slip] : slip
    return $.ajax({
      url: '/api/individualslips/',
      type: ajaxType,
      contentType: 'application/json',
      data: JSON.stringify(slip),
      success: function(data, status, jqXHR) {
        console.log("returned data", data, status, jqXHR);
        dispatch(submitLeaveSlip(data));
        dispatch(resetLeaveslipForm());
      },
      error: function(jqXHR, textStatus, errorThrown) {
        console.log('Slip post error!');
        console.log(jqXHR, textStatus, errorThrown);
      }
    });
  }
}

//using destroy because delete is an official HTTP action and is used for the thunk
export const DESTROY_LEAVESLIP = 'DESTROY_LEAVESLIP'
export const destroyLeaveSlip = (slip) => {
  return {
    type: DESTROY_LEAVESLIP,
    slip: slip
  }
}

export const EDIT_LEAVESLIP = 'EDIT_LEAVESLIP'
export const loadLeaveSlip = (slip) => {
  return {
    type: EDIT_LEAVESLIP,
    slip: slip,
  }
}
export const editLeaveSlip = (slip) => {
  return (dispatch) => {
    dispatch(selectTab(2))
    dispatch(loadLeaveSlip(slip))
  }
}

export const EDIT_GROUP_LEAVESLIP = 'EDIT_GROUP_LEAVESLIP'
export const loadGroupSlip = (slip) => {
  return {
    type: EDIT_GROUP_LEAVESLIP,
    slip: slip
  }
}
export const editGroupLeaveSlip = (slip) => {
  return (dispatch) => {
    dispatch(selectTab(3))
    dispatch(loadGroupSlip(slip))
  }
}

export const deleteLeaveSlip = (slip) => {
  return function(dispatch) {
    dispatch(destroyLeaveSlip(slip));
    return $.ajax({
      url: '/api/individualslips/' + slip.id.toString(),
      type: 'DELETE',
      success: function(data, status, jqXHR) {
        dispatch(receiveResponse(status));
      },
      error: function(jqXHR, textStatus, errorThrown) {
        console.log('Slip delete error!');
        console.log(jqXHR, textStatus, errorThrown);
      }
    });
  }
}


export const SUBMIT_GROUPSLIP = 'SUBMIT_GROUPSLIP'
export const submitGroupSlip = (gSlip) => {
  return {
    type: SUBMIT_GROUPSLIP,
    groupslip: gSlip,
  }
}

export const postGroupSlip = (gSlip, selectedEvents, slipId) => {
  var tas = initialState.tas;
  var ta_id = null;
  var texted = false;
  if (gSlip.ta_informed.id == "true") {
    ta_id = gSlip.ta.id;
  } else if (gSlip.ta_informed.id == "texted") {
    texted=true;
    gSlip.ta_informed.id = false;
  }

  // Group slips are assigned to a trainee by time range, so cannot skip events in the middle.
  gSlip.start = gSlip.selectedEvents[0].start_datetime
  gSlip.end = gSlip.selectedEvents[0].end_datetime
  for (var i = 1; i < gSlip.selectedEvents.length; i++) {
    event = gSlip.selectedEvents[i];
    if (event.start_datetime < gSlip.start) {
      gSlip.start = event.start_datetime;
    }
    if (event.end_datetime > gSlip.end) {
      gSlip.end = event.end_datetime;
    }
  }
  var trainee_ids = [];
  for (var i = 0; i < gSlip.trainees.length; i++) {
    trainee_ids.push(gSlip.trainees[i].id);
  }
  var slip = {
    "id": slipId,
    "type": gSlip.slipType.id,
    "status": "P",
    "submitted": Date.now(),
    "last_modified": Date.now(),
    "finalized": null,
    "description": "",
    "comments": gSlip.comment,
    "texted": texted,
    "informed": gSlip.ta_informed.id,
    "start": gSlip.start,
    "end": gSlip.end,
    "TA": ta_id,
    "trainee": null,
    "trainees": trainee_ids
  }
  var ajaxType = 'POST';
  if (slipId) {
    ajaxType = 'PUT';
  }
  return function(dispatch, getState) {
    slip.trainee = getState().trainee.id;
    var ajaxData = JSON.stringify(slip);
    if (slipId) {
      ajaxData = JSON.stringify([slip]);
    }
    return $.ajax({
      url: '/api/groupslips/',
      type: ajaxType,
      contentType: 'application/json',
      data: ajaxData,
      success: function(data, status, jqXHR) {
        dispatch(submitGroupSlip(data));
        dispatch(receiveResponse(status));
        dispatch(resetGroupslipForm())
      },
      error: function(jqXHR, textStatus, errorThrown) {
        console.log('Slip post error!');
        console.log(jqXHR, textStatus, errorThrown);
      }
    });
  }
}

export const DESTROY_GROUPSLIP = 'DESTROY_GROUPSLIP'
export const destroyGroupSlip = (slipId) => {
  return {
    type: DESTROY_GROUPSLIP,
    slipId: slipId
  }
}

export const deleteGroupSlip = (slipId) => {
  return function(dispatch) {
    dispatch(destroyGroupSlip(slipId));
    return $.ajax({
      url: '/api/groupslips/' + slipId.toString(),
      type: 'DELETE',
      success: function(data, status, jqXHR) {
        dispatch(receiveResponse(status));
      },
      error: function(jqXHR, textStatus, errorThrown) {
        console.log('Slip delete error!');
        console.log(jqXHR, textStatus, errorThrown);
      }
    });
  }
}

export const SELECT_TAB = 'SELECT_TAB'
export const selectTab = (index) => {
  return function(dispatch, getState) {
    // if not roll tab switch back to the trainee
    if (index != 2 && getState().form.traineeView.id !== getState().trainee.id) {
      dispatch(changeTraineeView(getState().trainee))
    }
    let show = getState().show
    // deselect events if going to and from the group slip tab. Reset the forms.
    if ((show!=='groupslip' && index===3) || (show==='groupslip' && index!==3)) {
      dispatch(resetGroupslipForm())
      dispatch(resetLeaveslipForm())
      dispatch(resetRollForm())
      dispatch(deselectAllEvents())
    }
    dispatch(showCalendar(index))
  }
}

export const SHOW_CALENDAR = 'SHOW_CALENDAR'
export const showCalendar = (index) => {
  switch (index) {
    case 0:
      return {
        type: SHOW_CALENDAR,
        value: 'summary'
      }
    case 1:
      return {
        type: SHOW_CALENDAR,
        value: 'roll'
      }
    case 2:
      return {
        type: SHOW_CALENDAR,
        value: 'leaveslip'
      }
    case 3:
      return {
        type: SHOW_CALENDAR,
        value: 'groupslip'
      }
  }
}