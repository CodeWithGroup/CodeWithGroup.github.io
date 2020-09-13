from datetime import datetime
from requests import Request, Session
import json

session = Session()
headers = {
    "Authorization": "Bearer <key>",
    "Content-Type": "application/json"
}

organisationId = "464103861019"
monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

eventTemplate = "<div class=\"row card\"><div class=\"col-12`eventClass`\"><div class=\"row\"><div class=\"col-sm-4 col-lg-2 event-date\"><span class=\"event-date-month\">`month`</span> <span class=\"event-date-day\">`day`</span><p><span class=\"event-date-start-time\">`eventStart``eventStartAmPm` - </span><span class=\"event-date-end-time\">`eventEnd``eventEndAmPm`</span></p></div><div class=\"col-sm-8 col-lg-10 event-title\"><span class=\"event-title\">`eventName`</span></div></div><div class=\"row\"><div class=\"col-md-12 col-lg-9 event-description\"><span class=\"event-description\">`eventDescription`</span></div><div class=\"col-md-12 col-lg-3 event-book-button\"><!-- Noscript content for added SEO --><noscript><a href=\"https://www.eventbrite.co.uk/e/programming-101-tickets-`eventId`\"rel=\"noopener noreferrer\" target=\"_blank\"></noscript><!-- You can customize this button any way you like --><button id=\"`eventbriteWidgetModalTriggerEventId`\" class=\"btn `registerButtonClass` float-right\"type=\"button\">`registerButtonText`</button><noscript></a>Register for tickets on Eventbrite</noscript></div></div></div></div>"
widgetPrefix = "var orderComplete = function () {var resultString = \"Order complete!\";alert(resultString);console.log(resultString);};"
widgetTemplate = "/* `eventName` */ window.EBWidgets.createWidget({widgetType: 'checkout',eventId: '`eventId`',modal: true,modalTriggerElementId: '`eventbriteWidgetModalTriggerEventId`',onOrderComplete: orderComplete});"

def getOrganisationUrl(organisationId):
    return "https://www.eventbriteapi.com/v3/organizations/" + str(organisationId)

def getEventUrl(eventId):
    return "https://www.eventbriteapi.com/v3/events/" + str(eventId)

def getResponse(url):
    response = session.get(url = url, headers = headers)
    return json.loads(response.text)

def getOrganisationEvents(organisationId):
    return getResponse(getOrganisationUrl(organisationId) + "/events/")

def getEventAttendees(eventId):
    return getResponse(getEventUrl(eventId) + "/attendees/")

def getEventTicketClasses(eventId):
    return getResponse(getEventUrl(eventId) + "/ticket_classes/")

def getEventsAsHtml(event, lambda_context):
    data = getOrganisationEvents(organisationId)

    content = ""
    widgets = widgetPrefix

    for event in data['events']:
        eventId = event['id']

        ticketClasses = getEventTicketClasses(eventId)['ticket_classes']
        onSaleStatus = '' if ticketClasses == [] else ticketClasses[0]['on_sale_status']
        
        eventClass = ''
        registerButtonClass = 'btn-primary'
        registerButtonText = 'Register'
        if onSaleStatus == 'SOLD_OUT':
            eventClass = ' event-sold-out'
            registerButtonClass = 'btn-default'
            registerButtonText = 'Sold out'
        
        startDate = datetime.strptime(event['start']['local'], "%Y-%m-%dT%H:%M:%S")
        endDate = datetime.strptime(event['end']['local'], "%Y-%m-%dT%H:%M:%S")

        month = monthNames[startDate.month - 1][:3].upper()
        day = startDate.day
        eventStart = startDate.hour
        eventEnd = endDate.hour
        eventName = event['name']['text']
        eventDescription = event['description']['text']

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
                .replace("`eventClass`", eventClass) \
                .replace("`registerButtonClass`", registerButtonClass) \
                .replace("`registerButtonText`", registerButtonText) \
                .replace("`eventClass`", eventClass) \
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

    return {'statusCode': 200, 'content': content, 'widgets': widgets}
