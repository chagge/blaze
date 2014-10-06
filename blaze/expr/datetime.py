from __future__ import absolute_import, division, print_function

from blaze.expr import Expr, ElemWise
from datashape import dshape, Record, DataShape, Unit, Option, date_, datetime_
import datashape

__all__ = ['DateTime', 'Date', 'date', 'Year', 'year', 'Month', 'month', 'Day',
        'day', 'Hour', 'hour', 'Second', 'second', 'Millisecond',
        'millisecond', 'Microsecond', 'microsecond', 'Date', 'date', 'Time',
        'time']

class DateTime(ElemWise):
    __slots__ = 'child',

    def __str__(self):
        return '%s.%s' % (str(self.child), type(self).__name__.lower())

    @property
    def schema(self):
        return dshape(self._dtype)

    @property
    def _name(self):
        return '%s_%s' % (self.child._name, self.attr)

    @property
    def attr(self):
        return type(self).__name__.lower()


class Date(DateTime):
    _dtype = datashape.date_

def date(expr):
    return Date(expr)

class Year(DateTime):
    _dtype = datashape.int32

def year(expr):
    return Year(expr)

class Month(DateTime):
    _dtype = datashape.int32

def month(expr):
    return Month(expr)

class Day(DateTime):
    _dtype = datashape.int32

def day(expr):
    return Day(expr)

class Time(DateTime):
    _dtype = datashape.time_

def time(expr):
    return Time(Expr)

class Hour(DateTime):
    _dtype = datashape.int32

def hour(expr):
    return Hour(expr)

class Minute(DateTime):
    _dtype = datashape.int32

def minute(expr):
    return Minute(expr)

class Second(DateTime):
    _dtype = datashape.int32

def second(expr):
    return Second(expr)

class Millisecond(DateTime):
    _dtype = datashape.int64

def millisecond(expr):
    return Millisecond(expr)

class Microsecond(DateTime):
    _dtype = datashape.int64

def microsecond(expr):
    return Microsecond(expr)



def isdatelike(ds):
    """

    >>> isdatelike('int32')
    False
    >>> isdatelike('datetime')
    True
    >>> isdatelike('?datetime')
    True
    """
    if isinstance(ds, str):
        ds = dshape(ds)
    if isinstance(ds, DataShape):
        ds = ds[0]
    if isinstance(ds, Option):
        return isdatelike(ds.ty)
    if isinstance(ds, Record) and len(ds.dict) == 1:
        return isdatelike(ds.types[0])
    return ds in (date_, datetime_)


from .expr import schema_method_list, method_properties

schema_method_list.extend([
    (isdatelike, set([year, month, day, hour, minute, date, time, second,
                      millisecond, microsecond]))
    ])

method_properties |= set([year, month, day, hour, minute, second, millisecond,
                          microsecond, date, time])
