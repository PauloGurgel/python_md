# Consultation and Finance Microservices

Author: Paulo Gurgel

# Architecture decisions

- DDD for consults and finance domain
- Event based notifications, so URLs are based on Command/Event/Query and not Restful standard
- Kafka to keep messages even while services are offline
- A light CQRS pattern (write on )

I avoided to go full event driven moving the message bus between views and service layer. This would be the best but it's too different for those who are used to orchestrated, instead of coreography, approaches.

# Manual testing, happy flow

1. Send the following request. Please pay attention to accepted ISO 8601 date format instead of date space time (internationally accepted for international API integrations). 

`POST` /consultation/v1/create
```json
{
    "patient_id": "e6afa807-8705-43d8-ba48-40a421843248",
    "physician_id": "e6afa807-8705-43d8-ba48-40a421843248",
    "start_date": "2021-07-01T08:30:00.000"
}
```

It will return a redirect. Get the ID and send a close request

`POST` /consultation/v1/close
```json
{
    "end_date": "2021-07-01T13:40:00.000",
    "id": "4baa39f8-f414-4ac4-9720-64fdfe09998b",
    "patient_id": "e6afa807-8705-43d8-ba48-40a421843248",
    "physician_id": "e6afa807-8705-43d8-ba48-40a421843248",
    "start_date": "2021-07-01T08:30:00.000"
}
```

This will calculate the final price. You can check it on the following gets:

`GET` /consultation/v1/consultation/<id>

or 

`GET` /consultation/v1/consultation for all

Once the close service is called, it will calculate the price, save it on database and send a ConsultationClosed event on message bus. Finance MS is able to save the Appointment.


# Issues

* For now, if you run everything from docker composer there is a chance flush does not work. I have not found the reason yet. It's a well known issue with older versions of librdkafka. I think it's related to some version conflict.
* Running only mariadb and kafka on container and running both applications from pycharm everything works (Python 3.8, Windows 10)

# Missing points

* Unit tests 




