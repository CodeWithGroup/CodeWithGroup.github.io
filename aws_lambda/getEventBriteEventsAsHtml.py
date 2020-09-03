from datetime import datetime
from requests import Request, Session
import json

eventTemplate = "<div class=\"row card\"><div class=\"col-12\"><div class=\"row\"><div class=\"col-sm-4 col-lg-2 event-date\"><span class=\"event-date-month\">`month`</span> <span class=\"event-date-day\">`day`</span><p><span class=\"event-date-start-time\">`eventStart``eventStartAmPm` - </span><span class=\"event-date-end-time\">`eventEnd``eventEndAmPm`</span></p></div><div class=\"col-sm-8 col-lg-10 event-title\"><span class=\"event-title\">`eventName`</span></div></div><div class=\"row\"><div class=\"col-md-12 col-lg-9 event-description\"><span class=\"event-description\">`eventDescription`</span></div><div class=\"col-md-12 col-lg-3 event-book-button\"><!-- Noscript content for added SEO --><noscript><a href=\"https://www.eventbrite.co.uk/e/programming-101-tickets-`eventId`\"rel=\"noopener noreferrer\" target=\"_blank\"></noscript><!-- You can customize this button any way you like --><button id=\"`eventbriteWidgetModalTriggerEventId`\" class=\"btn btn-primary float-right\"type=\"button\">Register</button><noscript></a>Register for tickets on Eventbrite</noscript></div></div></div></div>"
widgetPrefix = "var orderComplete = function () {var resultString = \"Order complete!\";alert(resultString);console.log(resultString);};"
widgetTemplate = "/* `eventName` */ window.EBWidgets.createWidget({widgetType: 'checkout',eventId: '`eventId`',modal: true,modalTriggerElementId: '`eventbriteWidgetModalTriggerEventId`',onOrderComplete: orderComplete});"
monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def getEventBriteEventsAsHtml(event, lambda_context):
    session = Session()

    session.head(
        'https://www.eventbriteapi.com/v3/organizations/464103861019/events/')

    response = session.get(
        url='https://www.eventbriteapi.com/v3/organizations/464103861019/events/',
        headers={
            "Authorization": "Bearer X6NY5BM5UQ3RKQNGHRD3",
            "Content-Type": "application/json"
        }
    )

    data = json.loads(response.text)

    content = ""
    widgets = widgetPrefix

    for event in data['events']:
        startDate = datetime.strptime(event['start']['local'], "%Y-%m-%dT%H:%M:%S")
        endDate = datetime.strptime(event['end']['local'], "%Y-%m-%dT%H:%M:%S")

        month = monthNames[startDate.month - 1][:3].upper()
        day = startDate.day
        eventStart = startDate.hour
        eventEnd = endDate.hour
        eventName = event['name']['text']
        eventDescription = event['description']['text']
        eventId = event['id']

        eventStartAmPm = "am"
        eventEndAmPm = "am"

        if eventStart > 12:
            eventStart -= 12
            eventStartAmPm = "pm"

        if eventEnd > 12:
            eventEnd -= 12
            eventEndAmPm = "pm"

        if event['status'] == "live":
            content = content + eventTemplate \
                .replace("`month`", month) \
                .replace("`day`", str(day)) \
                .replace("`eventStart`", str(eventStart)) \
                .replace("`eventStartAmPm`", eventStartAmPm) \
                .replace("`eventEnd`", str(eventEnd)) \
                .replace("`eventEndAmPm`", eventEndAmPm) \
                .replace("`eventName`", eventName) \
                .replace("`eventDescription`", eventDescription) \
                .replace("`eventId`", eventId) \
                .replace("`eventbriteWidgetModalTriggerEventId`", "eventbrite-widget-modal-trigger-" + eventId)

            widgets = widgets + "\r\n" + widgetTemplate \
                .replace("`eventName`", eventName) \
                .replace("`eventId`", eventId) \
                .replace("`eventbriteWidgetModalTriggerEventId`", "eventbrite-widget-modal-trigger-" + eventId)

    return {'content': content, 'widgets': widgets}
