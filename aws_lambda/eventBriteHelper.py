import asyncio
import json

from aiohttp import ClientSession
from datetime import datetime
from requests import Session

session = Session()
headers = {
    "Authorization": "Bearer <key>"
}

eventBriteApiUrl = "https://www.eventbriteapi.com/v3/"
organisationId = "464103861019"

monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
eventTemplate = "<div class=\"row card\"><div class=\"col-12`eventClass`\"><div class=\"row\"><div class=\"col-sm-4 col-lg-2 event-date\"><span class=\"event-date-month\">`month`</span> <span class=\"event-date-day\">`day`</span><p><span class=\"event-date-start-time\">`eventStart``eventStartAmPm` - </span><span class=\"event-date-end-time\">`eventEnd``eventEndAmPm`</span></p></div><div class=\"col-sm-8 col-lg-10 event-title\"><span class=\"event-title\">`eventName`</span>`venueDetails`</div></div><div class=\"row\"><div class=\"col-md-12 col-lg-9 event-description\"><span class=\"event-description\">`eventDescription`</span></div><div class=\"col-md-12 col-lg-3 event-book-button\"><!-- Noscript content for added SEO --><noscript><a href=\"https://www.eventbrite.co.uk/e/programming-101-tickets-`eventId`\"rel=\"noopener noreferrer\" target=\"_blank\"></noscript><!-- You can customize this button any way you like --><button id=\"`eventbriteWidgetModalTriggerEventId`\" class=\"btn `registerButtonClass` float-right\"type=\"button\">`registerButtonText`</button><noscript></a>Register for tickets on Eventbrite</noscript></div></div></div></div>"
venueTemplate = "<p><b>`venueName`</b>, `venueAddress`</p>"
widgetPrefix = "var orderComplete = function () {var resultString = \"Order complete!\";alert(resultString);console.log(resultString);};"
widgetTemplate = "/* `eventName` */ window.EBWidgets.createWidget({widgetType: 'checkout',eventId: '`eventId`',modal: true,modalTriggerElementId: '`eventbriteWidgetModalTriggerEventId`',onOrderComplete: orderComplete});"

async def fetchEventTicketClasses(session, eventId):
    url = eventBriteApiUrl + "events/" + str(eventId) + "/ticket_classes/"
    async with session.get(url = url, headers = headers) as response:
        responseJson = await response.json()
        return {'eventId': eventId, 'response': responseJson}

def getOrganisationEvents(organisationId):
    eventsUrl = eventBriteApiUrl + "organizations/" + str(organisationId) + "/events/?time_filter=current_future&status=live"
    response = session.get(url = eventsUrl, headers = headers)
    return json.loads(response.text)['events']

def getVenueDetails(venueId):
    venuesUrl = eventBriteApiUrl + "venues/" + str(venueId)
    response = session.get(url = venuesUrl, headers = headers)
    return json.loads(response.text)
    
async def getEventTicketClasses(eventData):
    async with ClientSession() as session:
        asyncTasks = []
        for event in eventData:
            asyncTasks.append(fetchEventTicketClasses(session, event['id']))

        responses = await asyncio.gather(*asyncTasks, return_exceptions=True)

        ticketClassData = {}
        for response in responses:
            if response['response']['pagination']['object_count'] == 0:
                continue

            ticketClassData[response['eventId']] = response['response']
        
        return ticketClassData

def processOrganisationEventsResponse(response):
    global organisationEvents
    organisationEvents = json.loads(response.text)

def processEventTicketClassesResponse(response):
    global ticketClasses
    ticketClasses = json.loads(response.text)['ticket_classes']

def getEventsAsHtml(event, lambda_context):
    content = ""
    dropins = ""
    huddles = ""
    workshops = ""
    
    widgets = widgetPrefix

    eventData = getOrganisationEvents(organisationId)
    ticketClassData = asyncio.run(getEventTicketClasses(eventData))

    for event in eventData:
        if event['status'] != "live":
            continue
        
        eventId = event['id']
        venue = None if event['venue_id'] is None else getVenueDetails(event['venue_id'])

        ticketClasses = ticketClassData[eventId]['ticket_classes']
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

        eventHtml = eventTemplate \
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

        if venue is None:
            eventHtml = eventHtml.replace("`venueDetails`", "")
        else:
            eventHtml = eventHtml \
                .replace("`venueDetails`", venueTemplate) \
                .replace("`venueName`", venue['name']) \
                .replace("`venueAddress`", venue['address']['localized_address_display'])

        widgets += "\r\n" + widgetTemplate \
            .replace("`eventName`", eventName) \
            .replace("`eventId`", eventId) \
            .replace("`eventbriteWidgetModalTriggerEventId`", "eventbrite-widget-modal-trigger-" + eventId)

        content += eventHtml
        
        if 'drop' in eventName.lower() and 'in' in eventName.lower():
            dropins += eventHtml
        elif 'huddle' in eventName.lower():
            huddles += eventHtml
        else:
            workshops += eventHtml

    if dropins == "":
        dropins = "<p>We don't have any drop-ins scheduled at the moment. Ask on Slack if you'd like us to arrange one.</p>"

    if huddles == "":
        huddles = "<p>We don't have any huddles scheduled at the moment. Ask on Slack if you'd like us to arrange one.</p>"

    if workshops == "":
        workshops = "<p>We don't have any workshops planned at the moment. Ask on Slack if you'd like us to arrange one.</p>"

    return {'statusCode': 200, 'content': content, 'dropins': dropins, 'huddles': huddles, 'workshops': workshops, 'widgets': widgets}
