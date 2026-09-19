delete from [Source].[Parcel];

insert into [Source].[Parcel] (
    [Parcel ID],
    [Status],
    [Depot],
    [Row update datetime]
)
values
    ('P-1001', 'In transit', 'Central', sysutcdatetime()),
    ('P-1002', 'Delivered', 'South', sysutcdatetime());
