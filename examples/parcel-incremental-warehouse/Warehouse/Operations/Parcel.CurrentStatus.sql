/*
Table ID: Parcel.CurrentStatus

Description: Current state of active parcels.

Lineage: Source.Parcel.

Primary key: Parcel ID

Incremental: true

Dependencies: []
*/
declare @bookmark datetime2(6);

set @bookmark = coalesce(
    (
        select [Bookmark datetime]
        from [_].[Bookmark]
        where [Item type] = 'Warehouse'
          and [Item name] = 'Operations'
          and [Schema name] = 'Parcel'
          and [Object name] = 'CurrentStatus'
    ),
    cast('1900-01-01T00:00:00' as datetime2(6))
);

-- Rows to insert or update
select [Parcel ID]
     , [Status]
     , [Depot]
     , [Row update datetime]
from [Source].[Parcel]
where [Row update datetime] > @bookmark
  and [Status] <> 'Cancelled';

-- Keys to delete
select [Parcel ID]
from [Source].[Parcel]
where [Row update datetime] > @bookmark
  and [Status] = 'Cancelled';
