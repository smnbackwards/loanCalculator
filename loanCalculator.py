#!/usr/bin/python3

import datetime

# http://www.studentloanrepayment.co.uk/portal/page?_pageid=93,6678755&_dad=portal&_schema=PORTAL
INTEREST_RATES = [
  { "from": datetime.date(2012,  9,  1), "to": datetime.date(2013, 8, 31), "value": .03 + .036 },
  { "from": datetime.date(2013,  9,  1), "to": datetime.date(2014, 8, 31), "value": .03 + .033 },
  { "from": datetime.date(2014,  9,  1), "to": datetime.date(2015, 8, 31), "value": .03 + .025 },
  { "from": datetime.date(2015,  9,  1), "to": datetime.date(2016, 8, 31), "value": .03 + .009 },
  { "from": datetime.date(2016,  9,  1), "to": datetime.date(2017, 8, 31), "value": .03 + .016 },
]

LOANS = [
  # Year 1
  { "date": datetime.date(2012, 10, 17), "value": 2250. },
  { "date": datetime.date(2013, 02, 06), "value": 2250. },
  { "date": datetime.date(2013, 05, 01), "value": 4500. },

  # Year 2
  { "date": datetime.date(2013, 10, 16), "value": 2250. },
  { "date": datetime.date(2014, 02, 05), "value": 2250. },
  { "date": datetime.date(2014, 05, 07), "value": 4500. },

  # Year 3 - Non standard second payment due to change of status to 4YF
  { "date": datetime.date(2014, 10, 15), "value": 2250. },
  { "date": datetime.date(2015, 03, 18), "value": 2250. },
  { "date": datetime.date(2015, 05, 06), "value": 4500. },

  # Year 4 - I screwed up the documents so the money got in late
  { "date": datetime.date(2016, 05, 25), "value": 2250. },
  { "date": datetime.date(2016, 06, 01), "value": 2250. },
  { "date": datetime.date(2016, 06,  8), "value": 4500. },
]

# Notified this is the amount I owe
CHECKSUMS = [
  { "date": datetime.date(2017, 02, 28), "value": 40606.03 },
]

PAYMENTS = [
]

START_DATE = datetime.date(2012, 9, 1)
END_DATE = datetime.date.today()


def daterange(start_date, end_date):
  if start_date <= end_date:
    for n in range((end_date - start_date).days + 1):
      yield start_date + datetime.timedelta(n)
  else:
    for n in range((start_date - end_date).days + 1):
      yield start_date - datetime.timedelta(n)


def fetchInterestRate(day):
  for interestRate in INTEREST_RATES:
    if interestRate["from"] <= day and day <= interestRate["to"]:
      return interestRate["value"]

  raise "Could not find day " + day


def daysInYearForDate(date):
  return (datetime.date(date.year, 12, 31) - datetime.date(date.year, 1, 1)).days + 1


def getDailyInterestRate(day):
  return fetchInterestRate(day) / daysInYearForDate(day)


def addPrincipalForDay(day):
  for loan in LOANS:
    if loan['date'] == day:
      return loan['value']
  return 0

def addInterestForPrincipal(principal, day):
  return getDailyInterestRate(day) * principal

def main():
  principalAccumulator = 0.0
  interestAccumulator = 0.0
  yesterday = 0.0

  for day in daterange(START_DATE, END_DATE):
    principalAccumulator += addPrincipalForDay(day)
    interestAccumulator += addInterestForPrincipal(principalAccumulator, day)

    print("{} | {:>8.2f} | {:>8.2f} | {:>8.2f} | {:>3.2f}".format(
      day,
      principalAccumulator,
      interestAccumulator,
      principalAccumulator + interestAccumulator,
      principalAccumulator + interestAccumulator - yesterday,
    ))

    yesterday = principalAccumulator + interestAccumulator


if __name__ == "__main__":
  main()

