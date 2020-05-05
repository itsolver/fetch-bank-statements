from datetime import datetime
import pytz

tz = pytz.timezone('Australia/Brisbane')

date_time_str = "2020-01-01"
date_time_obj = datetime.strptime(date_time_str, '%Y- %I:%M%p')

# a datetime with timezone
dt_with_tz = tz.localize(datetime(2020, 3, 31, 0, 0, 0), is_dst=None)
print(dt_with_tz)
# get timestamp
ts = (dt_with_tz - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
print (ts)
# -> 1346200430.0
# It is how datetime.timestamp method is implemented for timezone-aware datetime objects in Python 3.

# To get 'now epoch':

# from datetime import datetime

# now_epoch = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
# Or (assuming time uses POSIX epoch):

# import time

# now_epoch = time.time()