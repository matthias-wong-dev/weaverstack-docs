/*
Table ID: Parcel.ServiceLevel

Description: Service levels used to classify parcel deliveries.

Lineage: Reference data maintained in this project.

Dependencies: []

Primary key: Service level

Schema:
  Service level: string
  Target days: integer
*/
select *
from values
    ('Express', 1),
    ('Standard', 3)
as service_level(`Service level`, `Target days`);
