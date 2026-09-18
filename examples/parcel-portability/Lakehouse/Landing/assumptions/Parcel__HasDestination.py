"""
Assumption ID: Parcel.HasDestination

Description: Every parcel event names a depot.
"""

from Tables.Parcel__Event import Parcel__Event
from weaver import Assumption


class Parcel__HasDestination(Assumption):
    def read(self):
        return Parcel__Event(self).dataframe().where("Depot is null")
