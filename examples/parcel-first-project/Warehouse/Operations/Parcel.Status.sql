/*
Table ID: Parcel.Status

Description: Current status for the parcels in this example.

Lineage: A deterministic VALUES seed.

Primary key: Parcel ID

Schema:
  Parcel ID: varchar(20)
  Status: varchar(30)
*/
select v.ParcelId as [Parcel ID]
     , v.ParcelStatus as [Status]
from (values
    ('P-1001', 'In transit'),
    ('P-1002', 'Delivered')
) as v (ParcelId, ParcelStatus)
