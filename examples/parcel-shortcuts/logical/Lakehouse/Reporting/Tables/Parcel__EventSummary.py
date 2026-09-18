"""
Table ID: Parcel.EventSummary

Description: Tracking events read through the local Shortcut destination.

Lineage: Parcel events exposed through the local Shortcut destination.

Primary key: Parcel ID, Event sequence

Schema:
  Parcel ID: string
  Event sequence: integer
  Status: string
"""

from shortcuts import Parcel__Event

from weaver import Table


class Parcel__EventSummary(Table):
    def read(self):
        return Parcel__Event(self).dataframe().select(*self.columns())
