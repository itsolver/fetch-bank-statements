import pyinputplus
import datetime

start_datem = pyinputplus.inputDate(
    'Start date (YYYY-MM-DD): ', formats=['%Y-%m-%d'])
end_datem = pyinputplus.inputDate(
    'End date: (YYYY-MM-DD): ', formats=['%Y-%m-%d'])
start_year = start_datem.year
start_month = start_datem.month
start_day = start_datem.day
start_epoch = round(datetime.datetime(
    start_year, start_month, start_day).timestamp())
start_epoch_GMT = round(datetime.datetime(
    start_year, start_month, start_day, 0, 0, 0, 0, datetime.timezone.utc).timestamp())

end_year = end_datem.year
end_month = end_datem.month
end_day = end_datem.day
end_epoch = round(datetime.datetime(
    end_year, end_month, end_day).timestamp())
end_epoch_GMT = round(end_epoch + 36000)

print(start_epoch)
print(start_epoch_GMT)
