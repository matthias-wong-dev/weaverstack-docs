"""
Folder ID: Parcel.StatusFiles

Description: Current parcel status snapshots, one CSV file per parcel.

Lineage: A carrier snapshot represented by this example.

File key: "*.csv"

Incremental: false
"""

from pathlib import Path
import shutil

from weaver import Folder


class Parcel__StatusFiles(Folder):
    def read(self):
        source_root = Path(self.lakehouse.files_root()) / "parcel-source" / "parcel-status"
        if not source_root.is_dir():
            raise FileNotFoundError(
                f"Parcel status source directory not found: {source_root}"
            )

        staging = self.staging_folder()
        for source in source_root.glob("*.csv"):
            shutil.copy2(source, staging.path / source.name)
        return staging
