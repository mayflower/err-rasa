import arrow
import config

class DateConverter:
    """Format Date Strings
    Class to build a formated date string as expected in config from abritrary
    strings.
    """

    def fromString (self, value, default='today'):
        if value is None:
            value = default
        if value == 'today':
            date = arrow.utcnow()
        else:
            date = arrow.get(value, 'dddd')

        return date.format(config.DATE_FORMAT)

    def fromFirstAndDuration(self, first, last, duration):
        """When we have a date starting today and a duration we do have
          to evalutation the last day by duration
        """
        first = first if first is not None else 'today'
        first_date_string = self.fromString(first)
        last_date_string = self.fromString(last) if self.fromString(last) is not None else None
        if last_date_string is not None:
            return first_date_string, last_date_string

        last_date_string = arrow.get(first_date_string, config.DATE_FORMAT).shift(days=+duration)

        return first_date_string, last_date_string
