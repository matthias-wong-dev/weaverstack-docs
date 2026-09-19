if schema_id(N'Source') is null
    exec(N'create schema [Source]');

if object_id(N'[Source].[Parcel]', N'U') is null
begin
    create table [Source].[Parcel] (
        [Parcel ID] varchar(20) not null,
        [Status] varchar(30) not null,
        [Depot] varchar(30) not null,
        [Row update datetime] datetime2(6) not null
    );
end;
