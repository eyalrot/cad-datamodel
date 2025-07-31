# CAD Drawing Application - Data Model Requirements

## 1. Overview

Define a comprehensive data model for a CAD drawing application that supports geometric shapes, layers, groups, styling, and SVG rendering/persistence.

## 2. Core Data Model Requirements

### 2.1 Shape System

#### Base Shape Requirements

- **Unique Identification**: Every shape must have a globally unique identifier
- **Type Classification**: Explicit type identification for each shape
- **Hierarchical Relationships**: Support parent-child relationships for grouping
- **Layer Association**: Each shape belongs to exactly one layer
- **Visibility Control**: Independent visibility flag per shape
- **Lock State**: Prevent modifications when locked
- **Metadata Storage**: Extensible metadata for future features

#### Supported Shape Types

- **Rectangle**: Position (x,y), dimensions (width, height), optional corner radius
- **Circle**: Center point (cx, cy), radius
- **Line**: Start point (x1, y1), end point (x2, y2)
- **Polygon**: Ordered list of vertices, closed/open flag
- **Polyline**: Ordered list of points for connected segments
- **Group**: Container for other shapes (including nested groups)

#### Shape Geometry Requirements

- **Coordinate System**: Floating-point precision for all coordinates
- **Bounding Box**: Calculable bounds for every shape
- **Transform Support**: Independent transformation matrix per shape
- **Relative Positioning**: Shapes within groups use relative coordinates

### 2.2 Layer System

#### Layer Structure

- **Layer Identification**: Unique ID and human-readable name
- **Layer Ordering**: Explicit z-order index for rendering
- **Layer State**: Visibility, lock status, and opacity
- **Shape Assignment**: Bidirectional reference between layers and shapes
- **Default Layer**: Always have at least one layer present

#### Layer Constraints

- **No Orphan Shapes**: Every shape must belong to a layer
- **Layer Deletion**: Handle shape reassignment when layer deleted
- **Rendering Order**: Lower index layers render first (bottom)
- **Independent Properties**: Layer properties don't override shape properties

### 2.3 Group System

#### Group Structure

- **Group as Shape**: Groups are shapes that contain other shapes
- **Nested Groups**: Groups can contain other groups
- **Member List**: Ordered list of child shape IDs
- **Transform Inheritance**: Child shapes inherit group transformations
- **Bounding Box**: Computed from all child shapes

#### Group Behavior

- **Coordinate System**: Children use group-relative coordinates
- **Property Inheritance**: Optional style inheritance from group
- **Maintain Hierarchy**: Preserve structure during operations
- **Circular Reference Prevention**: Groups cannot contain themselves

### 2.4 Style System

#### Style Properties

- **Fill Properties**: Color, opacity, patterns (future)
- **Stroke Properties**: Color, width, opacity, dash pattern, line caps, joins
- **Inheritance Model**: Shapes can inherit styles from groups
- **Style Presets**: Named style configurations for reuse
- **Default Styles**: Per-shape-type default styling

#### Color Model

- **Color Formats**: Support hex, RGB, RGBA, named colors
- **Transparency**: Separate alpha channel for fill and stroke
- **Color Space**: sRGB as default color space

### 2.5 Transform System

#### Transform Components

- **Translation**: X and Y offset
- **Rotation**: Angle in degrees, rotation center point
- **Scale**: Non-uniform scaling (X and Y factors)
- **Transform Order**: Defined order of operations
- **Matrix Representation**: 2D affine transformation matrix

#### Transform Behavior

- **Cumulative Transforms**: Child inherits parent transforms
- **Local vs World**: Distinguish between local and world coordinates
- **Transform Origin**: Configurable origin point for rotations/scaling

### 2.6 Document Structure

#### Document Container

- **Document Metadata**: Version, creation date, last modified
- **Canvas Properties**: Dimensions, units, background
- **Layer Collection**: Ordered list of all layers
- **Shape Registry**: All shapes in the document
- **Group Hierarchy**: Tree structure of groups
- **Style Library**: Reusable style definitions

#### Document Constraints

- **Referential Integrity**: No dangling references
- **ID Uniqueness**: Enforce unique IDs across document
- **Version Compatibility**: Handle older document versions

## 3. Data Relationships

### 3.1 Entity Relationships

```
Document 1 --> N Layers
Document 1 --> N Shapes
Document 1 --> N Styles
Layer 1 --> N Shapes
Group 1 --> N Shapes (children)
Shape N --> 1 Layer
Shape N --> 0..1 Group (parent)
Shape 1 --> 1 Style
```

### 3.2 Hierarchy Rules

- **Single Parent**: Shape can only belong to one group
- **Layer Assignment**: Shape must belong to exactly one layer
- **Group Layer**: All shapes in a group must be on same layer
- **Deletion Cascading**: Deleting group doesn't delete children

## 4. Persistence Requirements

### 4.1 Serialization Format

- **Human Readable**: JSON-based format for version control
- **Compact Storage**: Efficient encoding for large drawings
- **Partial Loading**: Support loading only visible layers
- **Incremental Save**: Save only changes for performance

### 4.2 SVG Mapping

- **Direct Mapping**: Data model maps cleanly to SVG elements
- **Preserve Fidelity**: No data loss in SVG export/import
- **SVG Extensions**: Use namespaced attributes for extra data
- **Optimization**: Minimize redundant data in SVG output

### 4.3 Data Validation

- **Schema Validation**: Enforce data structure on load
- **Constraint Checking**: Validate relationships and references
- **Coordinate Validation**: Ensure numeric values are valid
- **Error Recovery**: Handle corrupted data gracefully

## 5. Performance Considerations

### 5.1 Memory Efficiency

- **Lazy Loading**: Load shapes on demand for large files
- **Shared Styles**: Reference common styles vs duplication
- **Efficient Storage**: Optimize coordinate precision
- **Memory Pooling**: Reuse objects where possible

### 5.2 Query Performance

- **Spatial Indexing**: Fast shape lookup by location
- **Layer Caching**: Cache computed layer properties
- **Bounding Box Cache**: Store computed bounds
- **Hit Testing**: Efficient point-in-shape detection

## 6. Extensibility Requirements

### 6.1 Shape Extensibility

- **Plugin Shapes**: Allow custom shape types
- **Property Extensions**: Add custom properties to shapes
- **Behavior Hooks**: Extensible shape behaviors
- **Backward Compatibility**: New shapes work in old versions

### 6.2 Future Considerations

- **Animation Data**: Keyframes and transitions
- **Constraint System**: Parametric relationships
- **3D Extension**: Z-coordinate support
- **Raster Integration**: Embedded images
- **Text Support**: Font data and text layout

## 7. Data Integrity

### 7.1 Consistency Rules

- **ID Uniqueness**: Enforce across entire document
- **Reference Validity**: All IDs reference existing objects
- **Coordinate Bounds**: Shapes within canvas bounds
- **Layer Integrity**: No shapes without layers

### 7.2 Operations Safety

- **Atomic Operations**: Group operations are atomic
- **Undo/Redo Support**: All changes must be reversible
- **Validation on Modify**: Check constraints on changes
- **Transaction Support**: Batch changes with rollback

## 8. Example Use Cases

### 8.1 Technical Drawing

- Mechanical parts with precise dimensions
- Architectural floor plans with layers
- Electrical schematics with grouped components
- Engineering diagrams with annotations

### 8.2 Data Model Challenges

- Handle 100,000+ shapes efficiently
- Complex nested group hierarchies
- Layer merging and splitting
- Style inheritance through multiple levels
- Maintain performance during transformations
