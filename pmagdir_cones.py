
from qgis.PyQt.QtWidgets import QAction, QDialog, QFormLayout, QComboBox, QDoubleSpinBox, QLabel, QPushButton, QVBoxLayout
from qgis.core import QgsProject, QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, QgsPointXY
from PyQt5.QtCore import QVariant
import math

class PmagDirCones:
    def __init__(self, iface):
        self.iface = iface
        self.action = None

    def initGui(self):
        self.action = QAction("Generate directional cones", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("&PmagDir-Cones", self.action)

    def unload(self):
        self.iface.removePluginMenu("&PmagDir-Cones", self.action)

    def run(self):
        layer = self.iface.activeLayer()
        if not layer or not layer.fields():
            self.iface.messageBar().pushWarning("PmagDir-Cones", "Please select an active vector layer with attributes.")
            return

        fields = [f.name() for f in layer.fields()]
        project_crs = QgsProject.instance().crs()
        is_geographic = project_crs.isGeographic()
        unit = "degrees" if is_geographic else "meters"

        dlg = QDialog()
        dlg.setWindowTitle("Generate directional cones")

        layout = QVBoxLayout()
        form = QFormLayout()

        cb_site = QComboBox(); cb_site.addItems(fields)
        cb_x = QComboBox(); cb_x.addItems(fields)
        cb_y = QComboBox(); cb_y.addItems(fields)
        cb_decl = QComboBox(); cb_decl.addItems(fields)
        cb_ang = QComboBox(); cb_ang.addItems(fields)

        scale_spin = QDoubleSpinBox()
        scale_spin.setDecimals(4)
        scale_spin.setValue(2000.0 if not is_geographic else 0.2)
        scale_spin.setMinimum(0.0001)
        scale_spin.setMaximum(100000)
        scale_spin.setSuffix(f" {unit}")

        msg = QLabel(f"⚠️ Coordinates will be treated as '{unit}' according to the project's CRS ({project_crs.authid()}).")

        form.addRow("Site name field", cb_site)
        form.addRow("X coordinate field", cb_x)
        form.addRow("Y coordinate field", cb_y)
        form.addRow("Declination (°) field", cb_decl)
        form.addRow("Cone angle (°) field", cb_ang)
        form.addRow("Cone length:", scale_spin)

        btn = QPushButton("Create cones")
        layout.addWidget(msg)
        layout.addLayout(form)
        layout.addWidget(btn)
        dlg.setLayout(layout)

        def create_cones():
            site_field = cb_site.currentText()
            x_field = cb_x.currentText()
            y_field = cb_y.currentText()
            decl_field = cb_decl.currentText()
            ang_field = cb_ang.currentText()
            scale = scale_spin.value()

            output = QgsVectorLayer(f"Polygon?crs={project_crs.authid()}", "Directional_Cones", "memory")
            output.dataProvider().addAttributes([
                QgsField("site", QVariant.String),
                QgsField("decl", QVariant.Double),
                QgsField("angle", QVariant.Double)
            ])
            output.updateFields()

            features = []

            for feat in layer.getFeatures():
                try:
                    site = str(feat[site_field])
                    x = float(feat[x_field])
                    y = float(feat[y_field])
                    decl = float(feat[decl_field])
                    ang = float(feat[ang_field])
                except Exception as e:
                    print(f"Error in feature {feat.id()}: {e}")
                    continue

                decl_rad = math.radians(90 - decl)
                half_angle = math.radians(ang / 2)

                dx1 = math.cos(decl_rad + half_angle) * scale
                dy1 = math.sin(decl_rad + half_angle) * scale
                dx2 = math.cos(decl_rad - half_angle) * scale
                dy2 = math.sin(decl_rad - half_angle) * scale

                p0 = QgsPointXY(x, y)
                p1 = QgsPointXY(x + dx1, y + dy1)
                p2 = QgsPointXY(x + dx2, y + dy2)

                geom = QgsGeometry.fromPolygonXY([[p0, p1, p2, p0]])
                f = QgsFeature()
                f.setFields(output.fields())
                f.setGeometry(geom)
                f["site"] = site
                f["decl"] = decl
                f["angle"] = ang
                features.append(f)

            output.dataProvider().addFeatures(features)
            output.updateExtents()
            QgsProject.instance().addMapLayer(output)
            dlg.accept()

        btn.clicked.connect(create_cones)
        dlg.exec_()
