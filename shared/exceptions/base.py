class MediaPulseError(Exception):
    """Root exception for the entire project."""


class ScrapingError(MediaPulseError):
    """Raised when a spider fails to fetch or parse an article."""


class IngestionError(MediaPulseError):
    """Raised when publishing or consuming messages fails."""


class StorageError(MediaPulseError):
    """Raised when reading or writing to the data lake fails."""


class ProcessingError(MediaPulseError):
    """Raised when a transformation step fails."""


class QualityError(MediaPulseError):
    """Raised when a data quality check encounters an internal error."""


class WarehouseError(MediaPulseError):
    """Raised when a warehouse operation fails."""
