from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFileDialog, QInputDialog, QFrame, QListWidget)
from PyQt6.QtCore import Qt
from src.ui.widgets import FileListWidget
from src.utils.logger import logger
import os

class BasePage(QWidget):
    def __init__(self, title, description):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(25)
        self.layout.setContentsMargins(40, 40, 40, 40)
        
        # Header
        header = QLabel(title)
        header.setObjectName("pageHeader") # For styling
        self.layout.addWidget(header)
        
        desc = QLabel(description)
        desc.setObjectName("pageDesc")
        desc.setWordWrap(True)
        self.layout.addWidget(desc)
        
        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("color: #444;")
        self.layout.addWidget(line)
        
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(20)
        self.layout.addLayout(self.content_layout)
        self.layout.addStretch()

    def add_staging_area(self, height=200):
        # Helper to add standard file list
        self.file_list = FileListWidget()
        self.file_list.setMinimumHeight(height)
        self.content_layout.addWidget(QLabel("Files:"))
        self.content_layout.addWidget(self.file_list)
        
        controls = QHBoxLayout()
        controls.setSpacing(15)
        
        btn_add = QPushButton("Add Files")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setStyleSheet("""
            QPushButton { background-color: #333; color: white; border: 1px solid #555; padding: 10px 20px; border-radius: 6px; font-weight: 600; font-size: 14px; }
            QPushButton:hover { background-color: #444; border-color: #4DAAF9; }
        """)
        btn_add.clicked.connect(self.on_add_files)
        
        btn_clear = QPushButton("Clear")
        btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear.setStyleSheet("""
            QPushButton { background-color: #2D2D2D; color: #AAA; border: 1px solid #444; padding: 10px 20px; border-radius: 6px; font-size: 14px; }
            QPushButton:hover { background-color: #333; color: white; }
        """)
        btn_clear.clicked.connect(self.file_list.clear)
        
        controls.addWidget(btn_add)
        controls.addWidget(btn_clear)
        controls.addStretch()
        self.content_layout.addLayout(controls)

    def add_action_button(self, text, callback, icon=None):
        # Helper to add a centered, reasonably sized action button
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 10, 0, 10)
        
        btn = QPushButton(text)
        btn.setObjectName("actionButton")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if icon: btn.setIcon(icon)
        btn.clicked.connect(callback)
        btn.setFixedWidth(280) # Fixed professional width (bigger than 240)
        btn.setMinimumHeight(50) # Taller
        
        layout.addStretch()
        layout.addWidget(btn)
        layout.addStretch()
        
        self.content_layout.addWidget(container)
        return btn

    def on_add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Add Files", "", "All Files (*.*)")
        if files:
            for f in files:
                self.file_list.add_file_item(f)

class HomePage(BasePage):
    def __init__(self, switcher_callback):
        super().__init__("Welcome", "Manage your PDF documents with professional tools.")
        self.switcher = switcher_callback
        
        # Dashboard Content
        import platform
        sys_info = f"System: {platform.system()} {platform.release()} | User: {os.getlogin()}"
        lbl_info = QLabel(sys_info)
        lbl_info.setStyleSheet("color: #666; font-size: 13px; margin-bottom: 25px; font-weight: 500;")
        self.content_layout.addWidget(lbl_info)
        
        # Quick Actions Grid
        from PyQt6.QtWidgets import QGridLayout
        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        grid.setSpacing(20) # More spacing
        grid.setContentsMargins(0, 0, 0, 0)
        
        # Helper to make card
        def make_card(text, idx):
            btn = QPushButton(text)
            btn.setObjectName("homeCard")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(100) # Taller cards
            btn.clicked.connect(lambda: self.switcher(idx))
            return btn
        
        grid.addWidget(make_card("📂  Merge PDFs\nCombine multiple files.", 1), 0, 0)
        grid.addWidget(make_card("✂️  Split PDF\nExtract pages or ranges.", 2), 0, 1)
        grid.addWidget(make_card("📉  Compress PDF\nReduce file size.", 3), 1, 0)
        grid.addWidget(make_card("🖼️  Images to PDF\nConvert JPG/PNG to PDF.", 4), 1, 1)
        grid.addWidget(make_card("🔒  Protection\nLock or Unlock PDFs.", 5), 2, 0)
        grid.addWidget(make_card("📑  Visual Editor\nRotate, delete & reorder.", 6), 2, 1)
        
        self.content_layout.addWidget(grid_container)
        self.content_layout.addStretch()

class MergePage(BasePage):
    def __init__(self, worker_callback):
        super().__init__("Merge PDF", "Combine multiple PDF files into a single document.")
        self.worker_callback = worker_callback
        self.add_staging_area()
        self.add_action_button("Merge Files", self.run)

    def run(self):
        files = self.file_list.get_all_files()
        if len(files) < 2:
            logger.log("Need at least 2 files to merge.")
            return
        out, _ = QFileDialog.getSaveFileName(self, "Save Merged PDF", "", "PDF (*.pdf)")
        if out:
            from src.modules.pdf_ops import PDFOps
            self.worker_callback(PDFOps.merge_pdfs, files, out)

class SplitPage(BasePage):
    def __init__(self, worker_callback):
        super().__init__("Split PDF", "Split a PDF into separate pages or ranges.")
        self.worker_callback = worker_callback
        
        self.content_layout.addWidget(QLabel("Select PDF to Split:"))
        self.file_list = FileListWidget()
        self.file_list.setMinimumHeight(150) 
        self.content_layout.addWidget(self.file_list)
        
        # Browse Button (Styled like staging buttons)
        btn_browse = QPushButton("Browse PDF")
        btn_browse.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_browse.setFixedWidth(150)
        btn_browse.setStyleSheet("""
            QPushButton { background-color: #333; color: white; border: 1px solid #555; padding: 10px; border-radius: 6px; font-weight: 600; }
            QPushButton:hover { background-color: #444; border-color: #4DAAF9; }
        """)
        btn_browse.clicked.connect(self.browse)
        self.content_layout.addWidget(btn_browse)
        
        # Direct Input
        from PyQt6.QtWidgets import QLineEdit
        self.content_layout.addSpacing(25)
        self.content_layout.addWidget(QLabel("Page Range:"))
        self.inp_range = QLineEdit()
        self.inp_range.setPlaceholderText("e.g. 1-5, 8, 11-13 (Leave empty for all)")
        self.content_layout.addWidget(self.inp_range)
        
        self.content_layout.addSpacing(10)
        self.add_action_button("Split PDF", self.run)
    
    def browse(self):
        self.file_list.clear() # Single file mode
        f, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF (*.pdf)")
        if f: self.file_list.add_file_item(f)

    def run(self):
        items = self.file_list.get_all_files()
        if not items: 
            logger.log("Please select a PDF first.")
            return
        input_file = items[0]
        out_dir = QFileDialog.getExistingDirectory(self, "Output Folder")
        if not out_dir: return
        range_str = self.inp_range.text().strip()
        from src.modules.pdf_ops import PDFOps
        self.worker_callback(PDFOps.split_pdf, input_file, out_dir, range_str if range_str else None)

class CompressPage(BasePage):
    def __init__(self, worker_callback):
        super().__init__("Compress PDF", "Reduce PDF file size.")
        self.worker_callback = worker_callback
        
        self.content_layout.addWidget(QLabel("Select PDF:"))
        self.file_list = FileListWidget()
        self.file_list.setMinimumHeight(150)
        self.content_layout.addWidget(self.file_list)
        
        btn_browse = QPushButton("Browse PDF")
        btn_browse.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_browse.setFixedWidth(150)
        btn_browse.setStyleSheet("""
            QPushButton { background-color: #333; color: white; border: 1px solid #555; padding: 10px; border-radius: 6px; font-weight: 600; }
            QPushButton:hover { background-color: #444; border-color: #4DAAF9; }
        """)
        btn_browse.clicked.connect(self.browse)
        self.content_layout.addWidget(btn_browse)
        
        # Direct Input
        from PyQt6.QtWidgets import QComboBox
        self.content_layout.addSpacing(25)
        self.content_layout.addWidget(QLabel("Compression Level:"))
        self.combo_level = QComboBox()
        self.combo_level.addItems(["Low", "Medium", "High"])
        self.combo_level.setCurrentIndex(1) # Default Medium
        self.content_layout.addWidget(self.combo_level)
        
        self.content_layout.addSpacing(10)
        self.add_action_button("Compress PDF", self.run)

    def browse(self):
        self.file_list.clear()
        f, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF (*.pdf)")
        if f: self.file_list.add_file_item(f)

    def run(self):
        items = self.file_list.get_all_files()
        if not items:
            logger.log("Please select a PDF first.")
            return
        input_file = items[0]
        out, _ = QFileDialog.getSaveFileName(self, "Save Compressed", "", "PDF (*.pdf)")
        if not out: return
        lvl = self.combo_level.currentText().lower()
        from src.modules.pdf_ops import PDFOps
        self.worker_callback(PDFOps.compress_pdf, input_file, out, lvl)

class ConvertPage(BasePage):
    def __init__(self, worker_callback):
        super().__init__("Images to PDF", "Convert JPG/PNG images into a PDF.")
        self.worker_callback = worker_callback
        self.add_staging_area()
        self.add_action_button("Convert Images", self.run)

    def run(self):
        files = self.file_list.get_all_files()
        if not files: 
            logger.log("Please add images first.")
            return
        out, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF (*.pdf)")
        if out:
            from src.modules.img_ops import ImageOps
            self.worker_callback(ImageOps.images_to_pdf, files, out)

class ExtractPage(BasePage):
    def __init__(self, worker_callback):
        super().__init__("Extract Text", "Extract plain text from PDF.")
        self.worker_callback = worker_callback
        
        self.content_layout.addWidget(QLabel("Select PDF:"))
        self.file_list = FileListWidget()
        self.file_list.setMinimumHeight(150) 
        self.content_layout.addWidget(self.file_list)
        
        btn_browse = QPushButton("Browse PDF")
        btn_browse.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_browse.setFixedWidth(150)
        btn_browse.setStyleSheet("""
            QPushButton { background-color: #333; color: white; border: 1px solid #555; padding: 10px; border-radius: 6px; font-weight: 600; }
            QPushButton:hover { background-color: #444; border-color: #4DAAF9; }
        """)
        btn_browse.clicked.connect(self.browse)
        self.content_layout.addWidget(btn_browse)
        
        self.add_action_button("Extract Text", self.run)

    def browse(self):
        self.file_list.clear()
        f, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF (*.pdf)")
        if f: self.file_list.add_file_item(f)

    def run(self):
        items = self.file_list.get_all_files()
        if not items: return
        input_file = items[0]
        out, _ = QFileDialog.getSaveFileName(self, "Save Text", "", "Text (*.txt)")
        if out:
            from src.modules.pdf_ops import PDFOps
            self.worker_callback(PDFOps.extract_text, input_file, out)

class ProtectionPage(BasePage):
    def __init__(self, worker_callback):
        super().__init__("Protection", "Encrypt (Lock) or Decrypt (Unlock) your PDFs.")
        self.worker_callback = worker_callback
        
        self.content_layout.addWidget(QLabel("Select PDF:"))
        self.file_list = FileListWidget()
        self.file_list.setMinimumHeight(120)
        self.content_layout.addWidget(self.file_list)
        
        btn_browse = QPushButton("Browse PDF")
        btn_browse.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_browse.setFixedWidth(150)
        btn_browse.setStyleSheet("""
            QPushButton { background-color: #333; color: white; border: 1px solid #555; padding: 10px; border-radius: 6px; font-weight: 600; }
            QPushButton:hover { background-color: #444; border-color: #4DAAF9; }
        """)
        btn_browse.clicked.connect(self.browse)
        self.content_layout.addWidget(btn_browse)
        
        self.content_layout.addSpacing(20)
        
        # Mode Selection
        from PyQt6.QtWidgets import QButtonGroup, QRadioButton, QHBoxLayout, QLineEdit
        self.mode_group = QButtonGroup(self)
        mode_layout = QHBoxLayout()
        mode_layout.setSpacing(20)
        
        self.rb_encrypt = QRadioButton("Lock (Encrypt)")
        self.rb_encrypt.setChecked(True)
        self.rb_decrypt = QRadioButton("Unlock (Decrypt)")
        
        # Increase Radio Button Size
        rb_style = "QRadioButton { font-size: 16px; color: #EEE; } QRadioButton::indicator { width: 20px; height: 20px; }"
        self.rb_encrypt.setStyleSheet(rb_style)
        self.rb_decrypt.setStyleSheet(rb_style)
        
        self.mode_group.addButton(self.rb_encrypt)
        self.mode_group.addButton(self.rb_decrypt)
        mode_layout.addWidget(self.rb_encrypt)
        mode_layout.addWidget(self.rb_decrypt)
        mode_layout.addStretch()
        self.content_layout.addLayout(mode_layout)
        
        # Password Input
        self.content_layout.addSpacing(15)
        self.content_layout.addWidget(QLabel("Password:"))
        self.inp_password = QLineEdit()
        self.inp_password.setPlaceholderText("Enter password")
        self.inp_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.content_layout.addWidget(self.inp_password)
        
        self.content_layout.addSpacing(20)
        self.add_action_button("Run Operation", self.run)

    def browse(self):
        self.file_list.clear() # Single file
        f, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF (*.pdf)")
        if f: self.file_list.add_file_item(f)

    def run(self):
        items = self.file_list.get_all_files()
        if not items:
            logger.log("Please select a PDF.")
            return
        input_file = items[0]
        password = self.inp_password.text().strip()
        
        if not password:
            logger.log("Please enter a password.")
            return
            
        out, _ = QFileDialog.getSaveFileName(self, "Save Result", "", "PDF (*.pdf)")
        if not out: return
        
        is_encrypt = self.rb_encrypt.isChecked()
        from src.modules.pdf_ops import PDFOps
        
        if is_encrypt:
            self.worker_callback(PDFOps.encrypt_pdf, input_file, out, password)
        else:
            self.worker_callback(PDFOps.decrypt_pdf, input_file, out, password)


class VisualPage(BasePage):
    def __init__(self, worker_callback):
        super().__init__("Visual Editor", "Organize pages: Rotate, Delete, Reorder.")
        self.worker_callback = worker_callback
        self.input_file = None
        self.page_data = [] # List of {'index': original_idx, 'rotate': 0, 'label': 'Page 1'}

        # Top Toolbar
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)
        
        self.lbl_file = QLabel("No file loaded")
        self.lbl_file.setStyleSheet("color: #888; font-style: italic;")
        
        btn_load = QPushButton("Load PDF")
        btn_load.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_load.setFixedWidth(120)
        btn_load.setStyleSheet("""
            QPushButton { background-color: #333; color: white; border: 1px solid #555; padding: 8px; border-radius: 6px; font-weight: 600; }
            QPushButton:hover { background-color: #444; border-color: #4DAAF9; }
        """)
        btn_load.clicked.connect(self.load_pdf)
        
        top_bar.addWidget(btn_load)
        top_bar.addWidget(self.lbl_file)
        top_bar.addStretch()
        self.content_layout.addLayout(top_bar)
        
        # Main Area: List + Controls
        main_area = QHBoxLayout()
        main_area.setSpacing(20)
        
        # Page List
        self.page_list = QListWidget()
        self.page_list.setStyleSheet("""
            QListWidget { background-color: #252525; border: 2px solid #333; border-radius: 8px; font-size: 16px; padding: 10px; }
            QListWidget::item { padding: 10px; border-bottom: 1px solid #333; }
            QListWidget::item:selected { background-color: #0066CC; color: white; }
        """)
        self.page_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        main_area.addWidget(self.page_list, stretch=1)
        
        # Controls Sidebar
        controls = QVBoxLayout()
        controls.setSpacing(15)
        
        def make_ctrl_btn(text, func):
            b = QPushButton(text)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setFixedWidth(160)
            b.setStyleSheet("""
                QPushButton { background-color: #2D2D2D; color: #BBB; border: 1px solid #444; padding: 12px; border-radius: 6px; font-weight: 600; }
                QPushButton:hover { background-color: #383838; color: white; border-color: #666; }
            """)
            b.clicked.connect(func)
            return b

        controls.addWidget(make_ctrl_btn("🔄 Rotate CW", lambda: self.rotate_page(90)))
        controls.addWidget(make_ctrl_btn("🔄 Rotate CCW", lambda: self.rotate_page(-90)))
        controls.addWidget(make_ctrl_btn("⬆️ Move Up", self.move_up))
        controls.addWidget(make_ctrl_btn("⬇️ Move Down", self.move_down))
        controls.addWidget(make_ctrl_btn("🗑️ Delete Page", self.delete_page))
        controls.addStretch()
        
        # Save Button (Bottom of controls)
        self.btn_save = QPushButton("Save PDF")
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.setFixedWidth(160)
        self.btn_save.setStyleSheet("""
            QPushButton { background-color: #007ACC; color: white; border: none; padding: 15px; border-radius: 6px; font-weight: 700; font-size: 16px; }
            QPushButton:hover { background-color: #008AE6; }
            QPushButton:disabled { background-color: #333; color: #555; }
        """)
        self.btn_save.clicked.connect(self.save_pdf)
        self.btn_save.setEnabled(False)
        controls.addWidget(self.btn_save)
        
        main_area.addLayout(controls)
        self.content_layout.addLayout(main_area)
        
    def load_pdf(self):
        f, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF (*.pdf)")
        if f:
            self.input_file = f
            self.lbl_file.setText(os.path.basename(f))
            self.lbl_file.setStyleSheet("color: #EEE; font-weight: bold;")
            
            # Read PDF and populate list
            from pypdf import PdfReader
            try:
                reader = PdfReader(f)
                count = len(reader.pages)
                self.page_data = [] # Reset
                self.page_list.clear()
                
                for i in range(count):
                    self.page_data.append({'index': i, 'rotate': 0, 'label': f"Page {i+1}"})
                    self.page_list.addItem(f"Page {i+1}")
                
                self.btn_save.setEnabled(True)
            except Exception as e:
                logger.log(f"Error reading PDF: {e}")

    def refresh_list(self):
        # Re-render list based on page_data
        # Preserve selection if possible? Hard with reorder.
        # Just repaint names
        for i in range(self.page_list.count()):
            data = self.page_data[i]
            rot_text = f" [Rotated {data['rotate']}°]" if data['rotate'] != 0 else ""
            self.page_list.item(i).setText(f"{data['label']}{rot_text}")

    def rotate_page(self, angle):
        rows = [x.row() for x in self.page_list.selectedIndexes()]
        if not rows: return
        for r in rows:
            self.page_data[r]['rotate'] = (self.page_data[r]['rotate'] + angle) % 360
        self.refresh_list()

    def delete_page(self):
        rows = sorted([x.row() for x in self.page_list.selectedIndexes()], reverse=True)
        if not rows: return
        for r in rows:
            self.page_data.pop(r)
            self.page_list.takeItem(r)

    def move_up(self):
        row = self.page_list.currentRow()
        if row <= 0: return
        # Swap data
        self.page_data[row], self.page_data[row-1] = self.page_data[row-1], self.page_data[row]
        # Swap list widget items
        cur_item = self.page_list.takeItem(row)
        self.page_list.insertItem(row-1, cur_item)
        self.page_list.setCurrentRow(row-1)
        
    def move_down(self):
        row = self.page_list.currentRow()
        if row < 0 or row >= self.page_list.count() - 1: return
        # Swap data
        self.page_data[row], self.page_data[row+1] = self.page_data[row+1], self.page_data[row]
        # Swap list items
        cur_item = self.page_list.takeItem(row)
        self.page_list.insertItem(row+1, cur_item)
        self.page_list.setCurrentRow(row+1)

    def save_pdf(self):
        if not self.input_file or not self.page_data: return
        
        out, _ = QFileDialog.getSaveFileName(self, "Save Modified PDF", "", "PDF (*.pdf)")
        if out:
            from src.modules.pdf_ops import PDFOps
            # Prepare config
            config = [{'index': p['index'], 'rotate': p['rotate']} for p in self.page_data]
            self.worker_callback(PDFOps.organize_pages, self.input_file, out, config)