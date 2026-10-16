/*
Table ID: Parcel.Delivery
Description: Small parcel example table.
Lineage: Constant
Schema:
  ParcelId: int
  DepotId: int
  Delivered: int
*/
SELECT ParcelId, DepotId, Delivered FROM (VALUES (1, 10, 1), (2, 10, 1), (3, 20, 0)) AS p(ParcelId, DepotId, Delivered)
