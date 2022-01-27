# TO DO
# 1. parameters (e.g. -s to download Stripe, -st to download Stripe and Transferwise)
from dotenv import load_dotenv
import os
import stripe
import time
import datetime
from datetime import date
import pyinputplus
import requests
import argparse
parser = argparse.ArgumentParser(
    description='Fetcher of bank statements and accounting reports.')

parser.add_argument("-l", "--last_quarter",
                    help="Gets statements for last quarter.", action="store_true")

args = parser.parse_args()

# START import secrets
env_path = '/Users/angusmclauchlan/.secrets/itsolver/automation/fetch-bank-statements/.env'
load_dotenv(dotenv_path=env_path)

transferwise_key = str(os.getenv("transferwise_key"))
transferwise_profile_id = str((os.getenv("transferwise_profile_id")))
transferwise_borderless_account_id = str(
    os.getenv("transferwise_borderless_account_id"))
stripe.api_key = os.getenv("stripe_key")
# END import secrets


def make_dir(name):
    try:
        os.mkdir(str(name))
    except OSError as e:
        print("Directory exists")


def previous_quarter_end(ref):
    if ref.month < 4:
        return datetime.date(ref.year - 1, 12, 31)
    elif ref.month < 7:
        return datetime.date(ref.year, 3, 31)
    elif ref.month < 10:
        return datetime.date(ref.year, 6, 30)
    return datetime.date(ref.year, 9, 30)


def previous_quarter_start(ref):
    if ref.month < 4:
        return datetime.date(ref.year - 1, 10, 1)
    elif ref.month < 7:
        return datetime.date(ref.year, 1, 1)
    elif ref.month < 10:
        return datetime.date(ref.year, 4, 1)
    return datetime.date(ref.year, 7, 1)


def fetch_transferwise(folder):
    headers = {
        'Authorization': 'Bearer ' + str(transferwise_key)
    }
    csv_url = str('https://transferwise.com/gateway/v3/profiles/' + str(transferwise_profile_id) + '/borderless-accounts/'+str(transferwise_borderless_account_id) +
                  '/statement.csv?intervalStart='+str(start_datem)+'T00%3A00%3A00.000%2B10%3A00&intervalEnd='+str(end_datem)+'T00%3A00%3A00.000%2B10%3A00&currency=AUD')
    try:
        req = requests.get(csv_url, headers=headers)
        req.raise_for_status()
        url_content = req.content
        path = os.path.join(str(folder), 'wise-statement.csv')
        csv_file = open(path, 'wb')
        csv_file.write(url_content)
        csv_file.close()
        print('Fetched TransferWise')
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def fetch_stripe(report_type, folder):
    if report_type == 'balance.summary.1':
        request_balance_summary = stripe.reporting.ReportRun.create(
            report_type=report_type,
            parameters={
                'interval_start': start_epoch_GMT,
                'interval_end': end_epoch_GMT,
                'timezone': 'Australia/Brisbane'
            },
        )
    else:
        request_balance_summary = stripe.reporting.ReportRun.create(
            report_type=report_type,
            parameters={
                'interval_start': start_epoch_GMT,
                'interval_end': end_epoch_GMT
            },
        )

    report_balance_summary = None
    while True:
        report_balance_summary = stripe.reporting.ReportRun.retrieve(
            request_balance_summary.id,
        )
        if report_balance_summary.status == 'succeeded':
            break
        time.sleep(6)
        print('...', end=' ')

    report_balance_summary_url = report_balance_summary['result']['url']
    stripe_headers = {
        'Authorization': 'Bearer ' + stripe.api_key
    }
    file = requests.get(report_balance_summary_url, headers=stripe_headers)
    if(file.status_code == 200):
        path = os.path.join(str(folder), 'stripe-'+report_type+'.csv')
        csv_file = open(path, 'wb')
        csv_file.write(file.content)
        csv_file.close()
        print('Fetched Stripe: ' + report_type)
    else:
        print('Failed to fetch Stripe: ' + report_type)


if (args.last_quarter == True):  # fetch last quarter statements
    today = date.today()
    start_datem = previous_quarter_start(today)
    end_datem = previous_quarter_end(today)
    print('Last quarter')
    print('start: ', start_datem)
    print('end: ', end_datem)
else:  # fetch statements for period manually specified
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
end_epoch_GMT = round(datetime.datetime(
    end_year, end_month, end_day, 0, 0, 0, 0, datetime.timezone.utc).timestamp())

make_dir(end_datem)
# Do the fetching
fetch_transferwise(end_datem)

fetch_stripe('balance.summary.1', end_datem)
# These report runs don't accept timezone parameter, therefore datetime is provided in UTC format
fetch_stripe('balance_change_from_activity.itemized.2', end_datem)
fetch_stripe('payout_reconciliation.summary.1', end_datem)
fetch_stripe('payouts.itemized.2', end_datem)


# clear secrets:
transferwise_key = None
stripe_key = None
