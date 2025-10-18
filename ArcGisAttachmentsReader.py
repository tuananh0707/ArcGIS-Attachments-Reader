# -*- coding: utf-8 -*-
"""
ArcGisAttachmentsReader.py - QGIS plugin module
- Click trên bản đồ để identify (không cần chọn trước)
- Hiển thị kết quả trong Dock widget giống Identify Results
- Hiển thị thumbnail từ ATTACH, danh sách tệp (ATT_NAME), preview/open/save
- Highlight đúng theo geometry (point/line/polygon) và clear khi đóng dock
- Bảng thuộc tính có màu xen kẽ và căn trái
"""

# Qt version compatibility
import qgis.PyQt
QT_VERSION = int(qgis.PyQt.QtCore.QT_VERSION_STR.split('.')[0])

# Compatibility constants for Qt5/Qt6
if QT_VERSION >= 6:
    from qgis.PyQt.QtWidgets import QSizePolicy
    from qgis.PyQt.QtCore import Qt
    from qgis.PyQt.QtGui import QPalette
    
    # SizePolicy
    SIZE_EXPANDING = QSizePolicy.Policy.Expanding
    SIZE_FIXED = QSizePolicy.Policy.Fixed
    SIZE_IGNORED = QSizePolicy.Policy.Ignored
    
    # Palette
    PALETTE_BASE = QPalette.ColorRole.Base
    PALETTE_ALTERNATE_BASE = QPalette.ColorRole.AlternateBase
    PALETTE_WINDOW = QPalette.ColorRole.Window
    
    # Alignment
    ALIGN_LEFT = Qt.AlignmentFlag.AlignLeft
    ALIGN_CENTER = Qt.AlignmentFlag.AlignCenter
    ALIGN_VCENTER = Qt.AlignmentFlag.AlignVCenter
    ALIGN_TOP = Qt.AlignmentFlag.AlignTop
    ALIGN_BOTTOM = Qt.AlignmentFlag.AlignBottom
    
    # Mouse and Key
    MOUSE_LEFT_BUTTON = Qt.MouseButton.LeftButton
    KEY_ESCAPE = Qt.Key.Key_Escape
    
    # Cursors
    POINTING_HAND_CURSOR = Qt.CursorShape.PointingHandCursor
    CLOSED_HAND_CURSOR = Qt.CursorShape.ClosedHandCursor
    ARROW_CURSOR = Qt.CursorShape.ArrowCursor
    
    # Text Interaction
    TEXT_BROWSER_INTERACTION = Qt.TextInteractionFlag.TextBrowserInteraction
    
    # Image Scaling
    KEEP_ASPECT_RATIO = Qt.AspectRatioMode.KeepAspectRatio
    SMOOTH_TRANSFORMATION = Qt.TransformationMode.SmoothTransformation
    
    # Item Flags
    ITEM_IS_ENABLED = Qt.ItemFlag.ItemIsEnabled
    ITEM_IS_SELECTABLE = Qt.ItemFlag.ItemIsSelectable
    
    # Dock Areas
    DOCK_LEFT = Qt.DockWidgetArea.LeftDockWidgetArea
    DOCK_RIGHT = Qt.DockWidgetArea.RightDockWidgetArea
    
    # Header Alignment
    HEADER_ALIGN_LEFT = Qt.AlignmentFlag.AlignLeft
    
else:
    from qgis.PyQt.QtWidgets import QSizePolicy
    from qgis.PyQt.QtCore import Qt
    from qgis.PyQt.QtGui import QPalette
    
    # Palette
    PALETTE_BASE = QPalette.Base
    PALETTE_ALTERNATE_BASE = QPalette.AlternateBase
    PALETTE_WINDOW = QPalette.Window
    
    # SizePolicy
    SIZE_EXPANDING = QSizePolicy.Expanding
    SIZE_FIXED = QSizePolicy.Fixed
    SIZE_IGNORED = QSizePolicy.Ignored
    
    # Alignment
    ALIGN_LEFT = Qt.AlignLeft
    ALIGN_CENTER = Qt.AlignCenter
    ALIGN_VCENTER = Qt.AlignVCenter
    ALIGN_TOP = Qt.AlignTop
    ALIGN_BOTTOM = Qt.AlignBottom
    
    # Mouse and Key
    MOUSE_LEFT_BUTTON = Qt.LeftButton
    KEY_ESCAPE = Qt.Key_Escape
    
    # Cursors
    POINTING_HAND_CURSOR = Qt.PointingHandCursor
    CLOSED_HAND_CURSOR = Qt.ClosedHandCursor
    ARROW_CURSOR = Qt.ArrowCursor
    
    # Text Interaction
    TEXT_BROWSER_INTERACTION = Qt.TextBrowserInteraction
    
    # Image Scaling
    KEEP_ASPECT_RATIO = Qt.KeepAspectRatio
    SMOOTH_TRANSFORMATION = Qt.SmoothTransformation
    
    # Item Flags
    ITEM_IS_ENABLED = Qt.ItemIsEnabled
    ITEM_IS_SELECTABLE = Qt.ItemIsSelectable
    
    # Dock Areas
    DOCK_LEFT = Qt.LeftDockWidgetArea
    DOCK_RIGHT = Qt.RightDockWidgetArea
    
    # Header Alignment
    HEADER_ALIGN_LEFT = Qt.AlignLeft

import qgis.PyQt
from qgis.PyQt.QtWidgets import (
    QAction, QWidget, QLabel, QVBoxLayout, QGroupBox,
    QHBoxLayout, QPushButton, QSizePolicy, QScrollArea,
    QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog,
    QDockWidget
)
from qgis.PyQt.QtGui import (
    QPixmap, QIcon, QCursor, QColor, QPalette
)
from qgis.PyQt.QtCore import Qt, QPoint, QUrl, QByteArray

# Handle Qt5/Qt6 compatibility
QT_VERSION = int(qgis.PyQt.QtCore.QT_VERSION_STR.split('.')[0])
if QT_VERSION >= 6:
    from qgis.PyQt.QtCore import Qt
    from qgis.PyQt.QtGui import QDesktopServices
    # Qt6 alignment constants
    ALIGN_LEFT = Qt.AlignmentFlag.AlignLeft
    ALIGN_CENTER = Qt.AlignmentFlag.AlignCenter
    ALIGN_VCENTER = Qt.AlignmentFlag.AlignVCenter
    MOUSE_LEFT_BUTTON = Qt.MouseButton.LeftButton
    KEY_ESCAPE = Qt.Key.Key_Escape
    POINTING_HAND_CURSOR = Qt.CursorShape.PointingHandCursor
    CLOSED_HAND_CURSOR = Qt.CursorShape.ClosedHandCursor
    ARROW_CURSOR = Qt.CursorShape.ArrowCursor
    TEXT_BROWSER_INTERACTION = Qt.TextInteractionFlag.TextBrowserInteraction
    KEEP_ASPECT_RATIO = Qt.AspectRatioMode.KeepAspectRatio
    SMOOTH_TRANSFORMATION = Qt.TransformationMode.SmoothTransformation
    NO_EDIT_TRIGGERS = QTableWidget.EditTrigger.NoEditTriggers
    SINGLE_SELECTION = QTableWidget.SelectionMode.SingleSelection
    ITEM_IS_ENABLED = Qt.ItemFlag.ItemIsEnabled
    ITEM_IS_SELECTABLE = Qt.ItemFlag.ItemIsSelectable
else:
    from qgis.PyQt.QtCore import Qt
    from qgis.PyQt.QtGui import QDesktopServices
    # Qt5 alignment constants
    ALIGN_LEFT = Qt.AlignLeft
    ALIGN_CENTER = Qt.AlignCenter
    ALIGN_VCENTER = Qt.AlignVCenter
    MOUSE_LEFT_BUTTON = Qt.LeftButton
    KEY_ESCAPE = Qt.Key_Escape
    POINTING_HAND_CURSOR = Qt.PointingHandCursor
    CLOSED_HAND_CURSOR = Qt.ClosedHandCursor
    ARROW_CURSOR = Qt.ArrowCursor
    TEXT_BROWSER_INTERACTION = Qt.TextBrowserInteraction
    KEEP_ASPECT_RATIO = Qt.KeepAspectRatio
    SMOOTH_TRANSFORMATION = Qt.SmoothTransformation
    NO_EDIT_TRIGGERS = QTableWidget.NoEditTriggers
    SINGLE_SELECTION = QTableWidget.SingleSelection
    ITEM_IS_ENABLED = Qt.ItemIsEnabled
    ITEM_IS_SELECTABLE = Qt.ItemIsSelectable
from qgis.core import (
    QgsProject, QgsWkbTypes, QgsGeometry, QgsRectangle,
    QgsFeatureRequest
)
from qgis.gui import QgsMapTool, QgsRubberBand, QgsVertexMarker
from qgis.utils import iface
import tempfile
import os
import sys

class ArcGisAttachmentsReader:
    def __init__(self, iface):
        self.iface = iface
        self.tool = None
        self.plugin_dir = os.path.dirname(__file__)
        icon_path = self.plugin_dir + '/icons/Identify.svg'   # đường dẫn tới icon tùy chỉnh
        self.action = QAction(QIcon(icon_path), "ArcGIS Attachments Reader", self.iface.mainWindow())
        self.action.setCheckable(True)
        self.action.triggered.connect(self.activate_tool)

        # highlight objects
        self.highlight_rb = None
        self.vertex_marker = None

        # dock
        self.dock = None

        # attachment map for link handling in dock (key -> {name,data})
        self._attachment_map = {}

    def initGui(self):
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("ArcGIS Attachments Reader", self.action)
        self.action.setToolTip("ArcGIS Attachments Identify")  # tooltip khi hover

    def unload(self):
        # remove dock and highlight
        self.clear_highlight()
        if self.dock:
            try:
                self.iface.removeDockWidget(self.dock)
            except Exception:
                pass
            try:
                self.dock.deleteLater()
            except Exception:
                pass
            self.dock = None

        try:
            self.iface.removeToolBarIcon(self.action)
            self.iface.removePluginToMenu("ArcGIS Attachments Reader", self.action)
        except Exception:
            pass

        if self.tool:
            try:
                self.iface.mapCanvas().unsetMapTool(self.tool)
            except Exception:
                pass
            self.tool = None

    def activate_tool(self):
        if self.action.isChecked():
            self.tool = IdentifyAttachmentsTool(self.iface, self)
            self.iface.mapCanvas().setMapTool(self.tool)
        else:
            # disable tool: clear highlight and unset
            self.clear_highlight()
            if self.tool:
                try:
                    self.iface.mapCanvas().unsetMapTool(self.tool)
                except Exception:
                    pass
                self.tool = None

    # ---------------- Helper: tìm layer attachment linh hoạt ----------------
    def get_attachment_layer(self, main_layer):
        """
        Tìm layer ATTACH tương ứng: tìm theo tên <name>__ATTACH, <name>_ATTACH,
        hoặc tên chứa main_layer.name() và 'attach', hoặc fallback tìm table có các trường đặc trưng.
        """
        if not main_layer:
            return None

        target1 = f"{main_layer.name()}__ATTACH".lower()
        target2 = f"{main_layer.name()}_ATTACH".lower()
        candidates = []

        for lyr in QgsProject.instance().mapLayers().values():
            try:
                lname = lyr.name().lower()
            except Exception:
                continue
            if lname == target1:
                return lyr
            if lname == target2:
                candidates.append(lyr)
            if main_layer.name().lower() in lname and "attach" in lname:
                candidates.append(lyr)

        if candidates:
            return candidates[0]

        # fallback: tìm table có trường REL_* và DATA/ATT_NAME
        for lyr in QgsProject.instance().mapLayers().values():
            try:
                fnames = [n.lower() for n in lyr.fields().names()]
            except Exception:
                fnames = []
            if (("rel_globalid" in fnames or "rel_objectid" in fnames or "rel_fid" in fnames) and
                ("att_name" in fnames or "name" in fnames) and
                ("data" in fnames or "attachment" in fnames or "att_data" in fnames)):
                return lyr

        return None

    # ---------------- Helper: chuyển blob -> bytes ----------------
    def _to_bytes(self, blob):
        if blob is None:
            return None
        if isinstance(blob, (bytes, bytearray)):
            return bytes(blob)
        try:
            if isinstance(blob, QByteArray):
                return bytes(blob)
        except Exception:
            pass
        try:
            d = blob.data()
            return bytes(d)
        except Exception:
            pass
        try:
            return bytes(blob)
        except Exception:
            return None

    # ---------------- Lấy attachments list ----------------
    def get_attachments_for_feature(self, main_layer, feature):
        """
        Trả về list dict: {"ATT_NAME": name, "data": bytes}
        Match rel_field với feature globalid/objectid.
        """
        # tìm field globalid/objectid trong feature
        globalid_field = None
        for f in feature.fields():
            if f.name().lower() == "globalid":
                globalid_field = f.name()
                break
        if not globalid_field:
            for f in feature.fields():
                if f.name().lower() in ("objectid", "fid", "id"):
                    globalid_field = f.name()
                    break
        if not globalid_field:
            return []

        globalid_value = feature[globalid_field]
        if globalid_value is None:
            return []

        attach_layer = self.get_attachment_layer(main_layer)
        if not attach_layer:
            return []

        attach_fields = [n for n in attach_layer.fields().names()]
        lower_fields = [n.lower() for n in attach_fields]

        name_candidates = ["att_name", "name", "filename", "file_name"]
        data_candidates = ["data", "attachment", "att_data", "blob"]
        rel_candidates = ["rel_globalid", "rel_objectid", "rel_fid", "parent_globalid", "relid"]

        name_field = None
        for c in name_candidates:
            if c in lower_fields:
                name_field = attach_fields[lower_fields.index(c)]
                break

        data_field = None
        for c in data_candidates:
            if c in lower_fields:
                data_field = attach_fields[lower_fields.index(c)]
                break

        rel_field = None
        for c in rel_candidates:
            if c in lower_fields:
                rel_field = attach_fields[lower_fields.index(c)]
                break

        attachments = []
        # iterate attachment table
        for att_feat in attach_layer.getFeatures():
            try:
                if rel_field:
                    rel_val = att_feat[rel_field]
                else:
                    continue
            except Exception:
                continue

            if rel_val is None:
                continue

            if str(rel_val).upper() != str(globalid_value).upper():
                continue

            # name
            fname = None
            if name_field:
                try:
                    fname = att_feat[name_field]
                except Exception:
                    fname = None
            if not fname:
                fname = f"attachment_{att_feat.id()}"

            # data
            blob = None
            if data_field:
                try:
                    blob = att_feat[data_field]
                except Exception:
                    blob = None

            raw = self._to_bytes(blob)
            if raw is None:
                continue

            attachments.append({
                "ATT_NAME": str(fname),
                "data": raw
            })

        return attachments

    # ---------------- Highlight management ----------------
    def clear_highlight(self):
        try:
            if self.highlight_rb:
                try:
                    self.highlight_rb.hide()
                except Exception:
                    pass
                try:
                    self.highlight_rb.reset()
                except Exception:
                    pass
                self.highlight_rb = None
        except Exception:
            self.highlight_rb = None

        try:
            if self.vertex_marker:
                try:
                    self.vertex_marker.hide()
                except Exception:
                    pass
                self.vertex_marker = None
        except Exception:
            self.vertex_marker = None

    def highlight_feature(self, layer, feature):
        # clear old
        self.clear_highlight()
        geom = feature.geometry()
        if geom is None or geom.isEmpty():
            return

        gtype = geom.type()

        if gtype == QgsWkbTypes.PointGeometry:
            try:
                if geom.isMultipart():
                    pts = geom.asMultiPoint()
                    pt = pts[0]
                else:
                    pt = geom.asPoint()
            except Exception:
                bbox = geom.boundingBox()
                pt = bbox.center()
            vm = QgsVertexMarker(self.iface.mapCanvas())
            vm.setCenter(pt)
            vm.setColor(QColor(255, 0, 0))
            vm.setIconSize(10)
            vm.setIconType(QgsVertexMarker.ICON_CIRCLE)
            vm.setPenWidth(2)
            self.vertex_marker = vm

        elif gtype == QgsWkbTypes.LineGeometry:
            rb = QgsRubberBand(self.iface.mapCanvas(), QgsWkbTypes.LineGeometry)
            rb.setToGeometry(geom, layer)
            rb.setColor(QColor(255, 0, 0))
            rb.setWidth(3)
            self.highlight_rb = rb
            rb.show()

        elif gtype == QgsWkbTypes.PolygonGeometry:
            rb = QgsRubberBand(self.iface.mapCanvas(), QgsWkbTypes.PolygonGeometry)
            rb.setToGeometry(geom, layer)
            rb.setColor(QColor(0, 128, 255))
            rb.setWidth(2)
            rb.setFillColor(QColor(0, 128, 255, 50))
            self.highlight_rb = rb
            rb.show()

        else:
            bbox = geom.boundingBox()
            ring = QgsGeometry.fromRect(bbox)
            rb = QgsRubberBand(self.iface.mapCanvas(), QgsWkbTypes.PolygonGeometry)
            rb.setToGeometry(ring, layer)
            rb.setColor(QColor(0, 128, 255))
            rb.setWidth(2)
            rb.setFillColor(QColor(0, 128, 255, 50))
            self.highlight_rb = rb
            rb.show()

    # ---------------- Dock UI (replace dialog) ----------------
    def show_feature_in_dock(self, layer, feature):
        """
        Tạo/Update Dock widget hiển thị kết quả identify.
        Nếu dock đã tồn tại, cập nhật nội dung (không tạo dock mới).
        """
        # Nếu dock chưa tồn tại, tạo mới và add vào main window
        if not self.dock:
            self.dock = QDockWidget("Identify - ArcGIS Attachments", self.iface.mainWindow())
            self.dock.setObjectName("ArcGisAttachmentsDock")
            
            # Use version-independent dock area constants
            self.dock.setAllowedAreas(DOCK_LEFT | DOCK_RIGHT)
            
            # ensure highlight cleared when dock closed
            self.dock.visibilityChanged.connect(lambda visible: (self.clear_highlight() if not visible else None))
            self.iface.addDockWidget(DOCK_RIGHT, self.dock)

        # container widget
        container = QWidget()
        layout = QVBoxLayout(container)

        # reset attachment map
        self._attachment_map = {}

        # get attachments
        attachments = self.get_attachments_for_feature(layer, feature)
        self.current_pixmap = None

        # --- Thumbnail area (if first attachment is image) ---
        thumb_label = QLabel()
        thumb_label.setAlignment(ALIGN_CENTER)
        thumb_label.setSizePolicy(SIZE_EXPANDING, SIZE_FIXED)

        if attachments and len(attachments) > 0:
            first = attachments[0]
            fname0 = first.get("ATT_NAME", "")
            data0 = first.get("data", b"")
            ext0 = os.path.splitext(fname0)[1].lower()
            if ext0 in (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tif", ".tiff"):
                pm = QPixmap()
                if pm.loadFromData(data0):
                    scaled = pm.scaledToWidth(420, SMOOTH_TRANSFORMATION)
                    thumb_label.setPixmap(scaled)
                    self.current_pixmap = pm
                    thumb_label.setCursor(POINTING_HAND_CURSOR)
                    thumb_label.mousePressEvent = lambda e: self.show_full_image(self.current_pixmap)
                    thumb_label.setMinimumHeight(200)
                    layout.addWidget(thumb_label)
            elif ext0 == ".pdf":
                btn_pdf = QPushButton(f"Mở PDF: {fname0}")
                def open_pdf0():
                    tmpf = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(fname0)[1])
                    try:
                        tmpf.write(data0)
                        tmpf.close()
                        QDesktopServices.openUrl(QUrl.fromLocalFile(tmpf.name))
                    except Exception as e:
                        QMessageBox.warning(None, "Lỗi", f"Không thể mở PDF: {e}")
                btn_pdf.clicked.connect(open_pdf0)
                layout.addWidget(btn_pdf)
            else:
                # no thumbnail for non-image
                pass

        # --- Files list (links) ---
        if attachments and len(attachments) > 0:
            files_label = QLabel()
            files_label.setTextInteractionFlags(TEXT_BROWSER_INTERACTION)
            files_label.setOpenExternalLinks(False)
            files_label.setWordWrap(True)
            html_parts = ['<b>Files attachment:</b> ']
            for i, att in enumerate(attachments):
                fname = att.get("ATT_NAME", f"attachment_{i+1}")
                key = f"attach://{i}"
                html_parts.append(f'<a href="{key}">{fname}</a>')
                if i < len(attachments)-1:
                    html_parts.append(", ")
                # store
                self._attachment_map[key] = {"name": fname, "data": att.get("data")}
            files_label.setText("".join(html_parts))

            def handle_link(url):
                info = self._attachment_map.get(url)
                if not info:
                    return
                fname = info["name"]
                data = info["data"]
                raw = data if isinstance(data, (bytes, bytearray)) else bytes(data)
                ext = os.path.splitext(fname)[1].lower()
                if ext in (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tif", ".tiff"):
                    pix = QPixmap()
                    if pix.loadFromData(raw):
                        self.show_full_image(pix)
                    else:
                        QMessageBox.warning(None, "Lỗi", "Không thể hiển thị ảnh.")
                    return
                if ext == ".pdf":
                    try:
                        tmpf = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
                        tmpf.write(raw)
                        tmpf.close()
                        QDesktopServices.openUrl(QUrl.fromLocalFile(tmpf.name))
                    except Exception as e:
                        QMessageBox.warning(None, "Lỗi", f"Không thể mở PDF: {e}")
                    return
                # other files -> save as
                path, _ = QFileDialog.getSaveFileName(None, "Lưu tệp", fname)
                if path:
                    try:
                        with open(path, "wb") as f:
                            f.write(raw)
                        QMessageBox.information(None, "Tải về", f"Đã lưu tệp:\n{path}")
                    except Exception as e:
                        QMessageBox.warning(None, "Lỗi", f"Không thể lưu tệp: {e}")

            files_label.linkActivated.connect(handle_link)
            layout.addWidget(files_label)

        # If no attachments => don't reserve large thumbnail space (so attributes fill)
        # --- Attribute table ---
        info_group = QGroupBox("Infomation")
        info_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #4a90e2;
                border-radius: 8px;
                margin-top: 10px;
                background-color: #f9f9f9;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #4a90e2;
            }
        """)

        table = QTableWidget()
        table.setColumnCount(2)
        # header left alignment
        table.setHorizontalHeaderLabels(["Field", "Value"])
        header = table.horizontalHeader()
        header.setDefaultAlignment(HEADER_ALIGN_LEFT | ALIGN_VCENTER)

        # Unified styling for all platforms and Qt versions
        table.setAlternatingRowColors(True)
        
        # Set base colors using both palette and stylesheet for maximum compatibility
        pal = table.palette()
        pal.setColor(PALETTE_BASE, QColor("#ffffff"))
        pal.setColor(PALETTE_ALTERNATE_BASE, QColor("#f7faff"))
        table.setPalette(pal)

        # Universal stylesheet that works on all platforms
        table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f7faff;
                gridline-color: #e0e0e0;
                font-size: 13px;
                border: 1px solid #d0d0d0;
                selection-background-color: #e0e9ff;
                selection-color: black;
            }
            QTableWidget::item {
                border-bottom: 1px solid #e0e0e0;
                padding: 2px;
                color: black;
            }
            QTableWidget::item:alternate {
                background-color: #f7faff;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                color: black;
                font-weight: bold;
                padding: 4px;
                border: 1px solid #ccc;
            }
            QHeaderView {
                background-color: #f0f0f0;
            }
            QTableWidget::item:selected {
                background-color: #e0e9ff;
                color: black;
            }
        """)

        table.verticalHeader().setVisible(False)
        table.setEditTriggers(NO_EDIT_TRIGGERS)
        table.setSelectionMode(SINGLE_SELECTION)
        table.setWordWrap(True)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setDefaultSectionSize(180)

        fields = layer.fields()
        table.setRowCount(len(fields))

        for row, field in enumerate(fields):
            field_name = field.alias() if field.alias() else field.name()
            try:
                value = feature[field.name()]
            except Exception:
                value = None
            if value in [None, ""]:
                value = "<Null>"

            key_item = QTableWidgetItem(str(field_name))
            val_item = QTableWidgetItem(str(value))

            key_item.setTextAlignment(ALIGN_LEFT | ALIGN_VCENTER)
            val_item.setTextAlignment(ALIGN_LEFT | ALIGN_VCENTER)

            key_item.setFlags(ITEM_IS_ENABLED)
            val_item.setFlags(ITEM_IS_ENABLED | ITEM_IS_SELECTABLE)

            table.setItem(row, 0, key_item)
            table.setItem(row, 1, val_item)

        table.resizeRowsToContents()

        layout_info = QVBoxLayout()
        layout_info.addWidget(table)
        info_group.setLayout(layout_info)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(info_group)
        scroll.setMinimumHeight(200)
        layout.addWidget(scroll)

        # bottom buttons (Close dock)
        btn_layout = QHBoxLayout()        
        def close_dock():
            if self.dock:
                try:
                    self.iface.removeDockWidget(self.dock)
                except Exception:
                    pass
                try:
                    self.dock.deleteLater()
                except Exception:
                    pass
                self.dock = None
            self.clear_highlight()
        
        btn_layout.addStretch()        
        layout.addLayout(btn_layout)
        container.setLayout(layout)
        self.dock.setWidget(container)
        self.dock.show()
        # ensure highlight shows and is cleared when dock closed (we connected visibility earlier)

    # ---------------- Image viewer (modal) ----------------
    def show_full_image(self, pixmap):
        """Modal image viewer - Fit / 1:1 / pan / scroll"""
        if pixmap is None:
            return

        from qgis.PyQt.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QSizePolicy

        class ImageViewer(QDialog):
            def __init__(self, pixmap, parent=None):
                super().__init__(parent)
                self.setWindowTitle("Zoom")
                self.resize(900, 700)
                self._pixmap_original = pixmap
                self._is_fit_mode = True
                self._panning = False
                self._pan_start_point = QPoint()
                self._scale_factor = 1.0

                self.layout = QVBoxLayout(self)

                self.img_label = QLabel()
                self.img_label.setAlignment(ALIGN_CENTER)
                self.img_label.setSizePolicy(SIZE_IGNORED, SIZE_IGNORED)
                self.img_label.setScaledContents(False)

                self.scroll = QScrollArea()
                self.scroll.setWidget(self.img_label)
                self.scroll.setWidgetResizable(False)  
                self.scroll.setAlignment(ALIGN_CENTER)
                self.layout.addWidget(self.scroll)

                self.toggle_btn = QPushButton("Fit")
                self.toggle_btn.clicked.connect(self.toggle_mode)
                self.close_btn = QPushButton("Close")
                self.close_btn.clicked.connect(self.close)

                btn_layout = QHBoxLayout()
                btn_layout.addWidget(self.toggle_btn)
                btn_layout.addStretch()
                btn_layout.addWidget(self.close_btn)
                self.layout.addLayout(btn_layout)

                self.update_scaled_image()

            def toggle_mode(self):
                self._is_fit_mode = not self._is_fit_mode
                self.toggle_btn.setText("Original" if self._is_fit_mode else "Fit")
                if self._is_fit_mode:
                    self._scale_factor = 1.0
                self.update_scaled_image()

            def update_scaled_image(self):
                if self._is_fit_mode:
                    area_size = self.scroll.viewport().size()
                    scaled = self._pixmap_original.scaled(
                        area_size, KEEP_ASPECT_RATIO, SMOOTH_TRANSFORMATION
                    )
                else:
                    size = self._pixmap_original.size() * self._scale_factor
                    scaled = self._pixmap_original.scaled(
                        size, KEEP_ASPECT_RATIO, SMOOTH_TRANSFORMATION
                    )

                self.img_label.setPixmap(scaled)
                self.img_label.resize(scaled.size())  

            def wheelEvent(self, event):
                if self._is_fit_mode:
                    self._is_fit_mode = False
                    self.toggle_btn.setText("Fit")

                # Qt6 compatible wheel delta
                if QT_VERSION >= 6:
                    delta = event.angleDelta().y()
                else:
                    delta = event.angleDelta().y()

                # Zoom in/out 15%
                if delta > 0:
                    self._scale_factor *= 1.15
                else:
                    self._scale_factor /= 1.15

                # Giới hạn zoom
                self._scale_factor = max(0.1, min(self._scale_factor, 20.0))

                self.update_scaled_image()
                event.accept()

            def mousePressEvent(self, event):
                if not self._is_fit_mode and event.button() == MOUSE_LEFT_BUTTON:
                    self._panning = True
                    self._pan_start_point = event.pos()
                    self.setCursor(CLOSED_HAND_CURSOR)
                    event.accept()

            def mouseMoveEvent(self, event):
                if self._panning:
                    delta = event.pos() - self._pan_start_point
                    self._pan_start_point = event.pos()
                    self.scroll.horizontalScrollBar().setValue(
                        self.scroll.horizontalScrollBar().value() - delta.x()
                    )
                    self.scroll.verticalScrollBar().setValue(
                        self.scroll.verticalScrollBar().value() - delta.y()
                    )
                    event.accept()

            def mouseReleaseEvent(self, event):
                if self._panning and event.button() == MOUSE_LEFT_BUTTON:
                    self._panning = False
                    self.setCursor(ARROW_CURSOR)
                    event.accept()

        viewer = ImageViewer(pixmap)
        # Qt6 compatible dialog execution
        if QT_VERSION >= 6:
            viewer.exec()
        else:
            viewer.exec_()

    def clear_results_panel(self):
        """
        Xóa nội dung hiện tại trong dock (nếu có) và đặt placeholder "Không có đối tượng được chọn".
        Tool vẫn giữ active; chỉ ẩn/đặt rỗng phần hiển thị kết quả.
        """
        # clear attachment map
        try:
            self._attachment_map = {}
        except Exception:
            self._attachment_map = {}

        if not self.dock:
            return

        try:
            old_widget = self.dock.widget()
            # tạo placeholder đơn giản
            placeholder = QWidget()
            ph_layout = QVBoxLayout(placeholder)
            lbl = QLabel("Không có đối tượng được chọn.")
            lbl.setAlignment(ALIGN_CENTER)
            lbl.setStyleSheet("color: gray; font-style: italic;")
            ph_layout.addStretch()
            ph_layout.addWidget(lbl)
            ph_layout.addStretch()

            # thay widget cũ bằng placeholder
            self.dock.setWidget(placeholder)

            # xóa widget cũ an toàn
            if old_widget is not None:
                try:
                    old_widget.deleteLater()
                except Exception:
                    pass
        except Exception:
            # nếu có lỗi, ẩn dock tạm
            try:
                self.dock.hide()
            except Exception:
                pass
        

# =================== Map tool ===================
class IdentifyAttachmentsTool(QgsMapTool):
    def keyPressEvent(self, event):
        """
        Bắt phím. Khi bấm ESC:
         - Xóa highlight (self.plugin.clear_highlight())
         - Làm trống panel kết quả (self.plugin.clear_results_panel())
         - Không unsetMapTool (tool vẫn active)
        """
        try:
            if event.key() == KEY_ESCAPE:
                # xóa highlight trên bản đồ
                try:
                    self.plugin.clear_highlight()
                except Exception:
                    pass

                # làm trống/ẩn nội dung panel (nhưng không thoát tool)
                try:
                    self.plugin.clear_results_panel()
                except Exception:
                    pass

                # chấp nhận event (không truyền tiếp)
                event.accept()
                return
        except Exception:
            pass

        # mặc định, gọi parent (nếu cần)
        try:
            super().keyPressEvent(event)
        except Exception:
            pass

    def __init__(self, iface, plugin):
        super().__init__(iface.mapCanvas())
        self.iface = iface
        self.plugin = plugin
        self.setCursor(QCursor(POINTING_HAND_CURSOR))

    def canvasReleaseEvent(self, event):
        # map coordinate
        point = self.toMapCoordinates(event.pos())
        layer = self.iface.activeLayer()
        if not layer:
            self.iface.messageBar().pushWarning("ArcGIS Attachments", "Chưa chọn lớp.")
            return

        # search a small rectangle around click (5 px)
        search_radius = self.iface.mapCanvas().mapUnitsPerPixel() * 5
        rect = QgsRectangle(
            point.x() - search_radius,
            point.y() - search_radius,
            point.x() + search_radius,
            point.y() + search_radius
        )

        request = QgsFeatureRequest().setFilterRect(rect)
        for feat in layer.getFeatures(request):
            # highlight feature
            try:
                self.plugin.highlight_feature(layer, feat)
            except Exception:
                pass
            # show in dock (update or create)
            try:
                self.plugin.show_feature_in_dock(layer, feat)
            except Exception as e:
                QMessageBox.warning(None, "Lỗi", f"Lỗi khi hiển thị kết quả: {e}")
            break
