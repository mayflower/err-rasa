import arrow
import config
import logging

class DateConverter:
    """Format Date Strings
    Class to build a formated date string as expected in config from abritrary
    strings.
    """

    def fromString (self, value, default='today'):
        today = arrow.utcnow()

        if value is None:
            value = default
        if value == 'today':
            date = arrow.utcnow()
        else:
            return value
        return date.format(config.DATE_FORMAT)

    def _stringToGeneralDay(self, value):
        if value is None or value == 'today':
            return value
        list = {
            'freitag': 'Friday',
            'montag': 'Monday',
            'diesntag': 'Tuesday',
            'mittwoch': 'Wednesday',
            'donnerstag': 'Thursday',
            'samstag': 'Saturday',
            'sonntag': 'Sunday',
            'heute': 'today'
            }
        if list[value] is not None:
            return list[value]
        return value

    def fromFirstAndDuration(self, first, last, duration):
        """When we have a date starting today and a duration we do have
          to evalutation the last day by duration
        """
        first = first if first is not None else 'today'
        first = self._stringToGeneralDay(first)
        first_date_string = self.fromString(first)

        last_date_string = None
        last = self._stringToGeneralDay(last)
        if len(last) > 0 and last is not None:
            last = last[0].upper() + last[1:]
            last_date_string = self.fromString(last)

        if last_date_string is not None:
            return first_date_string, last_date_string

        last_date_string = arrow.get(first_date_string, config.DATE_FORMAT).shift(days=+duration)

        return first_date_string, last_date_string
