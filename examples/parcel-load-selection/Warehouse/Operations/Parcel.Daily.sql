/*
Table ID: Parcel.Daily
Description: Small parcel example table.
Lineage: $Parcel.Events
*/
SELECT e.DepotId, SUM(e.Delivered) AS DeliveryCount FROM [Parcel].[Events] AS e JOIN [Reference].[Depot] AS d ON e.DepotId = d.DepotId GROUP BY e.DepotId
