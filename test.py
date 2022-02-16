from datetime import date, timezone
import datetime



print(local_timezone)

# Wed Feb 02 2022 12:43:39 GMT-0600 (Central Standard Time)
today = date.today()
timezone = datetime.datetime.utcnow().astimezone().tzinfo
print("Today's date:", today.strftime('%a %b %d %Y %X'))
# print("Today's date:", today.strftime('%c'))
