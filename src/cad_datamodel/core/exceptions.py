"""Exception hierarchy for the CAD datamodel.

This module defines custom exceptions for various error conditions
that can occur in the CAD system.
"""

from typing import Any, Optional


class CADError(Exception):
    """Base exception for all CAD-related errors.

    All custom exceptions in the CAD system should inherit from this class
    to allow for easy exception handling at the application level.
    """

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        """Initialize CAD error.

        Args:
            message: Human-readable error message
            details: Optional dictionary with additional error context
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ShapeValidationError(CADError):
    """Raised when shape validation fails.

    This exception is raised when a shape's properties violate
    constraints such as negative dimensions, invalid coordinates,
    or missing required attributes.
    """

    def __init__(self, shape_type: str, validation_error: str,
                 shape_id: Optional[str] = None):
        """Initialize shape validation error.

        Args:
            shape_type: Type of shape that failed validation
            validation_error: Specific validation error message
            shape_id: Optional ID of the shape
        """
        message = f"Shape validation failed for {shape_type}: {validation_error}"
        details = {
            "shape_type": shape_type,
            "validation_error": validation_error,
            "shape_id": shape_id
        }
        super().__init__(message, details)


class LayerError(CADError):
    """Raised for layer-related operations errors.

    This includes errors such as duplicate layer names, missing layers,
    or invalid layer operations.
    """

    def __init__(self, operation: str, layer_id: Optional[str] = None,
                 reason: Optional[str] = None):
        """Initialize layer error.

        Args:
            operation: The operation that failed
            layer_id: Optional ID of the layer
            reason: Optional reason for the failure
        """
        message = f"Layer operation '{operation}' failed"
        if reason:
            message += f": {reason}"

        details = {
            "operation": operation,
            "layer_id": layer_id,
            "reason": reason
        }
        super().__init__(message, details)


class TransformError(CADError):
    """Raised for transformation-related errors.

    This includes errors such as singular matrices, invalid transform
    parameters, or transform composition failures.
    """

    def __init__(self, transform_type: str, error: str):
        """Initialize transform error.

        Args:
            transform_type: Type of transform that failed
            error: Specific error message
        """
        message = f"Transform error in {transform_type}: {error}"
        details = {
            "transform_type": transform_type,
            "error": error
        }
        super().__init__(message, details)


class SerializationError(CADError):
    """Raised for serialization/deserialization errors.

    This includes errors during saving, loading, importing, or exporting
    CAD data to various formats.
    """

    def __init__(self, operation: str, format: str, error: str,
                 entity_type: Optional[str] = None):
        """Initialize serialization error.

        Args:
            operation: Either "serialize" or "deserialize"
            format: The format being used (e.g., "JSON", "SVG")
            error: Specific error message
            entity_type: Optional type of entity being processed
        """
        message = f"Failed to {operation} {entity_type or 'data'} to/from {format}: {error}"
        details = {
            "operation": operation,
            "format": format,
            "error": error,
            "entity_type": entity_type
        }
        super().__init__(message, details)


class GroupError(CADError):
    """Raised for group-related operation errors.

    This includes circular reference errors, invalid nesting,
    or group constraint violations.
    """

    def __init__(self, group_id: str, operation: str, reason: str):
        """Initialize group error.

        Args:
            group_id: ID of the group
            operation: The operation that failed
            reason: Reason for the failure
        """
        message = f"Group operation '{operation}' failed for group {group_id}: {reason}"
        details = {
            "group_id": group_id,
            "operation": operation,
            "reason": reason
        }
        super().__init__(message, details)


class DocumentError(CADError):
    """Raised for document-level errors.

    This includes document validation errors, version incompatibilities,
    or document structure violations.
    """

    def __init__(self, error_type: str, message: str,
                 document_id: Optional[str] = None):
        """Initialize document error.

        Args:
            error_type: Type of document error
            message: Detailed error message
            document_id: Optional document ID
        """
        full_message = f"Document error ({error_type}): {message}"
        details = {
            "error_type": error_type,
            "document_id": document_id
        }
        super().__init__(full_message, details)


class ReferenceError(CADError):
    """Raised when entity references are invalid.

    This includes dangling references, missing entities,
    or invalid ID references.
    """

    def __init__(self, reference_type: str, reference_id: str,
                 source_entity: Optional[str] = None):
        """Initialize reference error.

        Args:
            reference_type: Type of reference (e.g., "layer", "shape")
            reference_id: The invalid reference ID
            source_entity: Optional ID of the entity containing the reference
        """
        message = f"Invalid {reference_type} reference: {reference_id}"
        if source_entity:
            message += f" in entity {source_entity}"

        details = {
            "reference_type": reference_type,
            "reference_id": reference_id,
            "source_entity": source_entity
        }
        super().__init__(message, details)


class GeometryError(CADError):
    """Raised for geometric calculation errors.

    This includes errors in intersection calculations, invalid geometries,
    or numerical computation failures.
    """

    def __init__(self, operation: str, error: str,
                 shape_ids: Optional[list[str]] = None):
        """Initialize geometry error.

        Args:
            operation: The geometric operation that failed
            error: Specific error message
            shape_ids: Optional list of shape IDs involved
        """
        message = f"Geometry operation '{operation}' failed: {error}"
        details = {
            "operation": operation,
            "error": error,
            "shape_ids": shape_ids or []
        }
        super().__init__(message, details)
