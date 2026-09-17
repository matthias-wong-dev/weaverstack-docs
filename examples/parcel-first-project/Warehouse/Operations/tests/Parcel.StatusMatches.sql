/*
Test ID: Parcel.StatusMatches

Description: Parcel status contains the rows declared by this example.

Primary key: Parcel ID
*/
select v.ParcelId as [Parcel ID]
     , v.ParcelStatus as [Status]
from (values
    ('P-1001', 'In transit'),
    ('P-1002', 'Delivered')
) as v (ParcelId, ParcelStatus);

select [Parcel ID], [Status]
from [Parcel].[Status];
