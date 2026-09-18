/*
Table ID: Parcel.Event

Description: One row per parcel tracking event.

Lineage: A deterministic carrier feed represented by this example.

Dependencies: []

Primary key: Parcel ID, Event sequence

Schema:
  Parcel ID: string
  Event sequence: integer
  Status: string
*/
select *
from values
    ('P-1001', 1, 'Accepted'),
    ('P-1001', 2, 'In transit'),
    ('P-1002', 1, 'Delivered')
as event(`Parcel ID`, `Event sequence`, `Status`);
