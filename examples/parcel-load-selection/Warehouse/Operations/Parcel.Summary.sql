/*
Table ID: Parcel.Summary
Description: Small parcel example table.
Lineage: $Parcel.Daily
*/
SELECT SUM(DeliveryCount) AS DeliveryCount FROM [Parcel].[Daily]
