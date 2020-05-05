import requests, csv, pyinputplus, time, json
import stripe
# START import secrets into variables
import os
from dotenv import load_dotenv
load_dotenv()
transferwise_key = os.getenv("transferwise_key")
transferwise_profile_id = os.getenv("transferwise_profile_id")
transferwise_borderless_account_id = os.getenv("transferwise_borderless_account_id")
stripe.api_key = os.getenv("stripe_key")
# END import secrets into variables
print('🦴 Fetching bank statements in csv')
start_date = str(pyinputplus.inputDate('📆 Start date: ', formats=['%Y-%m-%d']))
end_date = str(pyinputplus.inputDate('📅 End date: ', formats=['%Y-%m-%d']))

def fetch_transferwise():
  headers = {
      'Authorization': 'Bearer ' + transferwise_key
    }
  csv_url = 'https://transferwise.com/gateway/v3/profiles/'+transferwise_profile_id+'/borderless-accounts/'+transferwise_borderless_account_id+'/statement.csv?intervalStart='+start_date+'T00%3A00%3A00.000%2B10%3A00&intervalEnd='+end_date+'T00%3A00%3A00.000%2B10%3A00&currency=AUD'
  try: 
    req = requests.get(csv_url, headers=headers)
    req.raise_for_status()
    url_content = req.content
    csv_file = open('transferwise-statement.csv', 'wb')
    csv_file.write(url_content)
    csv_file.close()
    print('🎉 Fetched TransferWise')
  except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

def fetch_stripe(report_type):
  if report_type == 'balance.summary.1':
    request_balance_summary = stripe.reporting.ReportRun.create(
    report_type=report_type,
    parameters={
      'interval_start': 1577800800, # Australia/Queensland Time: 2020-01-01 00:00:00
      'interval_end': 1585576800, # Australia/Queensland Time: 2020-04-01 00:00:00
      'timezone': 'Australia/Brisbane'
    },
    )
  else:
    request_balance_summary = stripe.reporting.ReportRun.create(
    report_type=report_type,
    parameters={
      'interval_start': 1577800800, # Australia/Queensland Time: 2020-01-01 00:00:00
      'interval_end': 1585576800, # Australia/Queensland Time: 2020-04-01 00:00:00
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
    csv_file = open('stripe-'+report_type+'.csv', 'wb')
    csv_file.write(file.content)
    csv_file.close()
    print('🎉 Fetched Stripe: ' + report_type)
  else:
    print('👎 Failed to fetch Stripe: ' + report_type)
  
fetch_transferwise()
fetch_stripe('balance.summary.1') # accepts paramater timezone
fetch_stripe('balance_change_from_activity.itemized.2') # does not accept paramater timezone
fetch_stripe('payout_reconciliation.summary.1') # does not accept paramater timezone
fetch_stripe('payouts.itemized.2') # does not accept paramater timezone

transferwise_key = None
stripe_key = None
