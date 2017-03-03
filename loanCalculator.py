#!/usr/bin/python3

import datetime


# http://www.studentloanrepayment.co.uk/portal/page?_pageid=93,6678755&_dad=portal&_schema=PORTAL
INTEREST_RATES = [
  { "from": datetime.date(2012,  9,  1), "to": datetime.date(2013, 8, 31), "value": .03 + .036 },
  { "from": datetime.date(2013,  9,  1), "to": datetime.date(2014, 8, 31), "value": .03 + .033 },
  { "from": datetime.date(2014,  9,  1), "to": datetime.date(2015, 8, 31), "value": .03 + .025 },
  { "from": datetime.date(2015,  9,  1), "to": datetime.date(2016, 8, 31), "value": .03 + .009 },
  { "from": datetime.date(2016,  9,  1), "to": datetime.date(2017, 8, 31), "value": .03 + .016 },

  # We assume things don't change much to make projections
  { "from": datetime.date(2017,  9,  1), "to": datetime.date(2050, 8, 31), "value": .03 + .016 },
]


LOANS = [
  # Year 1
  { "date": datetime.date(2012, 11, 7), "value": 2250. },
  { "date": datetime.date(2013,  2,  6), "value": 2250. },
  { "date": datetime.date(2013,  5,  1), "value": 4500. },

  # Year 2
  { "date": datetime.date(2013, 10, 16), "value": 2250. },
  { "date": datetime.date(2014,  2,  5), "value": 2250. },
  { "date": datetime.date(2014,  5,  7), "value": 4500. },

  # Year 3 - Non standard second payment due to change of status to 4YF
  { "date": datetime.date(2014, 10, 15), "value": 2250. },
  { "date": datetime.date(2015,  2, 4), "value": 2250. },
  { "date": datetime.date(2015,  5,  6), "value": 4500. },

  # Year 4 - I screwed up the documents so the money got in late
  { "date": datetime.date(2016,  10, 21), "value": 2250. },
  { "date": datetime.date(2016,  2,  3), "value": 2250. },
  { "date": datetime.date(2016,  5,  4), "value": 4500. },
]


# Notified this is the amount I owe
CHECKSUMS = [
  { "date": datetime.date(2016,  5, 31), "value": 39333.68 },
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


def fetchPrincipalForDay(day):
  for loan in LOANS:
    if loan['date'] == day:
      return loan['value']
  return 0


def getDailyInterestRate(day):
  daysInCurrentYear = (datetime.date(day.year, 12, 31) - datetime.date(day.year, 1, 1)).days + 1
  return fetchInterestRate(day) / daysInCurrentYear


def getMonthlyInterestRate(day):
  return fetchInterestRate(day) / 12.


def isEndOfCompoundingPeriod(day):
  return day.day == 1


def getInterestForPrincipal(principal, day):
  return getMonthlyInterestRate(day) * principal


def main():
  principal      = 0.0
  closedInterest = 0.0 # Compounds
  openInterest   = 0.0 # Does not compound yet
  previousClose  = 0.0

  for day in daterange(START_DATE, END_DATE):
    principal += fetchPrincipalForDay(day)

    if isEndOfCompoundingPeriod(day):
      openInterest += getInterestForPrincipal(principal + closedInterest, day)
      closedInterest += openInterest
      openInterest = 0

    closingBalance = principal + closedInterest + openInterest

    print("{} | {:>8.2f} | {:>8.2f} | {:>8.2f} | {:>3.2f}".format(
      day,
      principal,
      closedInterest + openInterest,
      closingBalance,
      closingBalance - previousClose,
    ))

    previousClose = closingBalance


if __name__ == "__main__":
  main()
