update [Source].[Parcel]
set [Status] = 'Delivered',
    [Row update datetime] = sysutcdatetime()
where [Parcel ID] = 'P-1001';

update [Source].[Parcel]
set [Status] = 'Cancelled',
    [Row update datetime] = sysutcdatetime()
where [Parcel ID] = 'P-1002';
