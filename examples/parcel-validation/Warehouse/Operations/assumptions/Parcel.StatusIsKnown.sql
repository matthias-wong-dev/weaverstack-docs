/*
Assumption ID: Parcel.StatusIsKnown

Description: Every parcel has a status recognised by this example.

Dependencies:
  - Parcel.Status
*/
select [Parcel ID]
     , [Status]
from [Parcel].[Status]
where [Status] is null
   or [Status] not in ('Accepted', 'In transit', 'Delivered');
