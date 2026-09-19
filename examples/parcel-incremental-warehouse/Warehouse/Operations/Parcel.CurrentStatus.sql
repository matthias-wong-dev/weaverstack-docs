/*
Table ID: Parcel.CurrentStatus

Description: Current state of active parcels.

Lineage: Parcel records supplied through the physical Source.Parcel Shortcut.

Primary key: Parcel ID

Incremental: true

Dependencies: []

Schema:
  Parcel ID: varchar(20)
  Status: varchar(30)
  Depot: varchar(30)
*/
declare @bookmark_datetime datetime2(6);
set @bookmark_datetime = coalesce(
    (
        select [Bookmark datetime]
        from [_].[Bookmark]
        where [Item type] = N'Warehouse'
          and [Item name] = N'Operations'
          and [Schema name] = N'Parcel'
          and [Object name] = N'CurrentStatus'
    ),
    cast('1900-01-01' as datetime2(6))
);

-- Rows to insert or update
select [Parcel ID]
     , [Status]
     , [Depot]
from [Source].[Parcel]
where [Row update datetime] > @bookmark_datetime
  and [Status] <> 'Cancelled';

-- Keys to delete
select [Parcel ID]
from [Source].[Parcel]
where [Row update datetime] > @bookmark_datetime
  and [Status] = 'Cancelled';
