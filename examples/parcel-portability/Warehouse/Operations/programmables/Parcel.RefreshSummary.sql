create or alter procedure Parcel.RefreshSummary
as
begin
    set nocount on;

    select count(*) as [Parcel count]
    from Parcel.CurrentStatus;
end;
