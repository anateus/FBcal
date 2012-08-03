# FBcal a.k.a Calendarics

This is a little webservice that fixes a "feature" Facebook just introduced: the iCal-format export URLs expire and so you can't just stick em in your favorite calendar software and remain synchronized.

Right now this takes an access token like so:

```
/cal/<whatevername>.ics?access_token=<access_token>
```

Then you can stick ```/cal/<whatevername>.ics``` in your calendar software. Soon it will allow you to authorize right from the web service. For now you can grab an access token from [Facebook's Graph API Explorer](https://developers.facebook.com/tools/explorer/?method=GET&path=me%2Fevents).
