import datetime

from kotti import DBSession
from kotti.security import has_permission
from kotti.views.slots import assign_slot
from sqlalchemy.sql.expression import or_

from kotti_calendar import events_settings
from kotti_calendar.resources import Event


def upcoming_events(context, request):
    now = datetime.datetime.now()
    settings = events_settings()
    future = or_(Event.start > now, Event.end > now)
    events = DBSession.query(Event).filter(future).order_by(Event.start).all()
    events = [event for event in events if\
                has_permission('view', event, request)]
    if len(events) > settings['events_count']:
        events = events[:settings['events_count']]
    return {'events': events}


def includeme_upcoming_events(config):
    config.add_view(
        upcoming_events,
        name='upcoming-events',
        renderer='kotti_calendar:templates/upcoming-events.pt')
    assign_slot('upcoming-events', 'right')


def previous_events(context, request):
    now = datetime.datetime.now()
    settings = events_settings()
    past = or_(Event.start < now, Event.end < now)
    events = DBSession.query(Event).filter(past).order_by(Event.start).all()
    events = [event for event in events if\
                has_permission('view', event, request)]
    if len(events) > settings['events_count']:
        events = events[:settings['events_count']]
    return {'events': events}


def includeme_previous_events(config):
    config.add_view(
        previous_events,
        name='previous-events',
        renderer='kotti_calendar:templates/previous-events.pt')
    assign_slot('previous-events', 'right')
