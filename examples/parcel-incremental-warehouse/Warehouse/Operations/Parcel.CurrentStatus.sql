/*
Table ID: Parcel.CurrentStatus

Description: Current parcel state from an external change feed.

Lineage: staging.ParcelChanges.

Primary key: Parcel ID

Incremental: true

Dependencies: []
*/
select [Parcel ID]
     , [Status]
     , [Depot]
from [staging].[ParcelChanges]
where [Operation] <> 'DELETE';

select [Parcel ID]
from [staging].[ParcelChanges]
where [Operation] = 'DELETE';
