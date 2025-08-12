# PmagDir-Cones

**PmagDir-Cones** is a QGIS plugin for visualizing directional paleomagnetic data as projected cones.

## 🧭 What it does

This plugin reads a table with:
- Site name
- Coordinates (X, Y) in geographic or projected system
- Declination (°) indicating the azimuth direction
- Cone angle (°) as the apex angle of the projected cone

It draws a triangle (projected cone) from each point in the direction of the declination, with an opening angle defined by the cone apex angle.

## 🧪 Usage

1. Load a point vector layer with the required fields.
2. Ensure your project CRS reflects the coordinate type (geographic or UTM).
3. Go to `Plugins > PmagDir-Cones > Generate directional cones`.
4. Select the appropriate fields and cone length.
5. Press "Create cones" to generate a new polygon layer.

## ⚠️ Considerations

- Coordinate type (degrees or meters) is inferred from the project's CRS.
- Declination is interpreted as 0° = North, increasing clockwise.
- Cone length must be appropriate for the unit system (e.g. 2000 m for UTM).
- Ensure input values are numeric and correctly formatted.

## 📄 License

This project is licensed under the MIT License.

<img width="708" height="487" alt="imagen" src="https://github.com/user-attachments/assets/a526f031-2a64-4df4-be39-f4fca5d64375" />

