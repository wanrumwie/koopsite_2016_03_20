import datetime
import json
from pytz import UTC

date_handler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime.datetime)
    or isinstance(obj, datetime.date)
    else None
)
json.dumps(datetime.datetime.now(), default=date_handler)
'"2010-04-20T20:08:21.634121"'

dt = datetime.datetime.now()
print(dt)
dt = datetime.datetime(2015, 7, 24, 12, 51, 10, 640000, tzinfo=UTC)
print(dt)
dtiso = dt.isoformat()
print(dtiso)
js = json.dumps(dtiso)
print(js)
a = [dt, dtiso, js]
print(a)
