from typing import Optional, List
from pydantic import BaseModel
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

class stock_filter(BaseModel):
    stock_code: Optional[List] = None

class sector_filter(BaseModel):
    sector_code: Optional[List] = None

class date_filter(BaseModel):
    # inputs
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    period: Optional[str] = None

    # date values that we'll search with
    start: Optional[date] = None
    end: Optional[date] = None

    def processSearchDates(self):
        # they didn't give any input at all
        if self.period == None and self.start_date == None and self.end_date == None:
            # not sure what to do here - don't want to raise an Exception because this is fine
            pass
        # if they have set a period as well as either start or end date - can't have it both ways...
        elif self.period != None and ( self.start_date != None or self.end_date != None):
            # default to using period
            self.setPeriod()
        elif self.period != None:
            # use period
            self.setPeriod()
        elif self.start_date == None:
            # need a start date.  Don't need to test for an end date, since that can be implied as today
            pass
        else:
            # they've given a start date and maybe an end date
            self.start = datetime.strptime(self.start_date, '%Y-%m-%d')
            
            if self.end_date == None:
                # assume end date
                self.end = date.today()
            else:
                # explicit end date
                self.end = datetime.strptime(self.end_date, '%Y-%m-%d')
            pass

    def setPeriod(self):
        self.end = date.today()
        if self.period[-1] == 'd':
            self.start = date.today() + relativedelta(days=-int(self.period[:-1]))
        elif self.period[-1] == 'w':
            self.start = date.today() + relativedelta(weeks=-int(self.period[:-1]))
        elif self.period[-1] == 'm':
            self.start = date.today() + relativedelta(months=-int(self.period[:-1]))
        elif self.period[-1] == 'y':
            self.start = date.today() + relativedelta(years=-int(self.period[:-1]))
        else:
            # default to days
            self.start = date.today() + relativedelta(days=-int(self.period[:-1]))
        pass