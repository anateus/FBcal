# To Do

1. Adjust app to request a new access token if it's invalid instead of just failing
2. Add landing page
3. Add button to landing page requesting user to authorize the app
4. If you go to cal/<something>.ics with a valid access_token no longer create a new entry. only the authorization process can create a new calendar.


## Later

We're gonna want to represent events as their own sort of things, then serialize into caches.

```
# each event is a hash
HMSET event:<unique_id> name <name> start <start> ...

# sorted sets are used to store a user's events
ZADD events:<user_id> <utc timestamp> event:<unique_id>
```