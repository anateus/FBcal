# FBcal a.k.a Calendarics

This is a little webservice that fixes a "feature" Facebook just introduced: the iCal-format export URLs expire and so you can't just stick em in your favorite calendar software and remain synchronized.

Right now this takes an access token like so:

```
/cal/<whatevername>.ics?access_token=<access_token>
```

Then you can stick ```/cal/<whatevername>.ics``` in your calendar software. Soon it will allow you to authorize right from the web service. For now you can grab an access token from [Facebook's Graph API Explorer](https://developers.facebook.com/tools/explorer/?method=GET&path=me%2Fevents).

## Requirements

Well, you can look in the requirements.txt file, but basically, this is written in Python using the Flask web framework and utilizing Redis as the datastore.

## Deployment

Currently it's set up to be deployed unto dotcloud, but should be easily adjustable to run anywhere wsgi is spoken.
