/*
Test ID: Parcel.StatusMatches

Description: Current parcel status matches the independently stated expected rows.

Primary key: Parcel ID

Dependencies:
  - Parcel.Status
*/
select v.[Parcel ID]
     , v.[Status]
from (values
    ('P-1001', 'In transit'),
    ('P-1002', 'Delivered')
) as v ([Parcel ID], [Status]);

select [Parcel ID]
     , [Status]
from [Parcel].[Status];
