"""
Folder ID: Parcel.StatusFiles

Description: Current parcel status snapshots, one CSV file per parcel.

Lineage: A carrier snapshot represented by this example.

File key: "*.csv"

Incremental: false
"""

from weaver import Folder

SNAPSHOT = {
    "P-1001.csv": "Parcel ID,Status,Depot\nP-1001,In transit,Central\n",
    "P-1002.csv": "Parcel ID,Status,Depot\nP-1002,Delivered,South\n",
}


class Parcel__StatusFiles(Folder):
    def read(self):
        staging = self.staging_folder()
        for name, content in SNAPSHOT.items():
            (staging.path / name).write_text(content, encoding="utf-8")
        return staging
