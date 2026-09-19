update [Source].[Parcel]
set [Status] = 'Delivered',
    [Row update datetime] = sysdatetime()
where [Parcel ID] = 'P-1001';

update [Source].[Parcel]
set [Status] = 'Cancelled',
    [Row update datetime] = sysdatetime()
where [Parcel ID] = 'P-1002';
