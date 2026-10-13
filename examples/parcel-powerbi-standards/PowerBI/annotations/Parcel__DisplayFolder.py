"""Place an annotated measure in a native display folder."""

from weaver.semantic_models import Annotation


class Parcel__DisplayFolder(Annotation):
    scopes = frozenset({"measure"})

    def apply(self, target):
        if not self.value:
            self.error("requires a non-empty display folder")
        target.displayFolder = self.value
