import datetime

class Eastern_tzinfo(datetime.tzinfo):
    """Implementation of the Eastern timezone.
    
    Adapted from http://code.google.com/appengine/docs/python/datastore/typesandpropertyclasses.html
    """
    def utcoffset(self, dt):
        return datetime.timedelta(hours=-5) + self.dst(dt)

    def _FirstSunday(self, dt):
        """First Sunday on or after dt."""
        return dt + datetime.timedelta(days=(6-dt.weekday()))

    def dst(self, dt):
        # 2 am on the second Sunday in March
        dst_start = self._FirstSunday(datetime.datetime(dt.year, 3, 8, 2))
        # 1 am on the first Sunday in November
        dst_end = self._FirstSunday(datetime.datetime(dt.year, 11, 1, 1))

        if dst_start <= dt.replace(tzinfo=None) < dst_end:
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(hours=0)
        
    def tzname(self, dt):
        if self.dst(dt) == datetime.timedelta(hours=0):
            return "EST"
        else:
            return "EDT"
        
        
def date_for_new_snippet():
    """Return most recent Monday, unless it is Monday (0)"""
    today = datetime.datetime.now(Eastern_tzinfo()).date()
    if (today.weekday() == 0):
        aligned = today - datetime.timedelta(weeks=1)
    else:
        aligned = today - datetime.timedelta(days=today.weekday()) 
    return aligned 

def date_for_retrieval():
    """Always return the previous Monday."""
    return date_for_new_snippet()

def date_for_missed_snippets():
    """Always return the Monday from the last completed cycle."""
    return date_for_retrieval() - datetime.timedelta(weeks=1)
