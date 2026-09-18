/*
Table ID: Parcel.Status

Description: Current status for the parcel automation example.

Lineage: A deterministic parcel feed represented by this example.

Primary key: Parcel ID

Schema:
  Parcel ID: varchar(20)
  Status: varchar(30)
*/
select v.[Parcel ID]
     , v.[Status]
from (values
    ('P-1001', 'In transit'),
    ('P-1002', 'Delivered')
) as v ([Parcel ID], [Status]);
