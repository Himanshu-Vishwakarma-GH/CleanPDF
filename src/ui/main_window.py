from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QListWidget, QListWidgetItem, QStackedWidget, QStatusBar, QMessageBox, QPushButton)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from src.ui.styles import Theme
from src.ui.pages import HomePage, MergePage, SplitPage, CompressPage, ConvertPage, ExtractPage
from src.utils.workers import WorkerThread
from src.utils.logger import logger
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Simple Toolset")
        self.resize(1100, 700)
        
        # State
        self.is_dark = True
        self.current_theme = Theme.DARK
        
        # Central Layout (Horizontal: Sidebar | Content)
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar Area (VBox: List)
        sidebar_container = QWidget()
        sidebar_container.setFixedWidth(240)
        sidebar_container.setObjectName("sidebarContainer")
        sidebar_layout = QVBoxLayout(sidebar_container)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        self.sidebar = QListWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sidebar.currentRowChanged.connect(self.change_page)
        sidebar_layout.addWidget(self.sidebar)
        
        
        # No Toggle Button (Dark Mode Locked)
        # sidebar_layout.addStretch() 
        
        
        main_layout.addWidget(sidebar_container)
        
        # Content Area
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)
        
        # Initialize Pages
        self.pages = []
        self.init_pages()
        
        # Status Bar (Replaces Log TextEdit)
        self.status_bar = QStatusBar()
        self.status_bar.setObjectName("statusBar")
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready.")
        
        # Worker Bridge
        # We pass a callback to pages so they can start workers in MainWindow context
        
        # Theme Toggle (Bottom of sidebar via trick or just an item?)
        # For simplicity in listwidget, we'll add it as a regular item for now or a button below sidebar
        # Let's actually put Sidebar in a VBox to spawn a toggle button at bottom
        
        logger.signaller.log_signal.connect(self.on_log_message)
        
        self.apply_theme()
        
        # Select Home
        self.sidebar.setCurrentRow(0)

    def init_pages(self):
        # Define Navigation Items
        from src.ui.pages import HomePage, MergePage, SplitPage, CompressPage, ConvertPage, ExtractPage, ProtectionPage, VisualPage
        
        items = [
            ("Home", HomePage),
            ("Merge PDF", MergePage),
            ("Split PDF", SplitPage),
            ("Compress PDF", CompressPage),
            ("Images to PDF", ConvertPage),
            ("Protection", ProtectionPage),
            ("Visual Editor", VisualPage),
            ("Extract Text", ExtractPage)
        ]
        
        for name, PageClass in items:
            item = QListWidgetItem(name)
            item.setSizeHint(QSize(200, 50))
            self.sidebar.addItem(item)
            
            if PageClass == HomePage:
                page = PageClass(self.change_page)
            else:
                page = PageClass(self.start_worker) # Inject worker starter
            
            self.content_stack.addWidget(page)
            self.pages.append(page)

    def change_page(self, index):
        self.content_stack.setCurrentIndex(index)
        self.sidebar.setCurrentRow(index) # Sync sidebar

    def start_worker(self, func, *args, **kwargs):
        self.status_bar.showMessage("Processing...")
        self.centralWidget().setEnabled(False) # Lock UI
        
        # Extract output path for UI usage, remove from kwargs so it doesn't break PDFOps
        self.last_output = kwargs.pop('created_file', None)
        
        self.worker = WorkerThread(func, *args, **kwargs)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()

    def on_worker_finished(self, success, msg):
        self.centralWidget().setEnabled(True)
        self.status_bar.clearMessage()
        
        if success:
            # Create a custom success dialog
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Success")
            dlg.setText(f"Operation Complete!\n\n{msg}")
            dlg.setIcon(QMessageBox.Icon.Information)
            
            btn_ok = dlg.addButton("OK", QMessageBox.ButtonRole.AcceptRole)
            btn_open = None
            
            if self.last_output:
                # Determine what to open
                target = self.last_output
                target_label = "Open File"
                if os.path.isdir(target):
                    target_label = "Open Folder"
                else:
                    target_label = "Open Folder" # Usually better to open folder with file selected
                    
                btn_open = dlg.addButton(target_label, QMessageBox.ButtonRole.ActionRole)
            
            dlg.exec()
            
            if dlg.clickedButton() == btn_open:
                self.open_last_output()
                
            self.status_bar.showMessage("Ready.", 5000)
        else:
            QMessageBox.critical(self, "Error", msg)
            self.status_bar.showMessage("Error occurred.", 5000)

    def open_last_output(self):
        if hasattr(self, 'last_output') and os.path.exists(os.path.dirname(self.last_output)):
            folder = os.path.dirname(self.last_output)
            if os.name == 'nt':
                os.startfile(folder)
            else:
                import subprocess
                subprocess.Popen(['xdg-open', folder])


    def on_log_message(self, msg):
        # Also catch logger output to status bar for debug
        # But prioritize success/fail messages
        if "Error" in msg or "Success" in msg:
            return 
        self.status_bar.showMessage(msg, 3000)

    def apply_theme(self):
        theme = self.current_theme
        
        # Base Styles
        style = theme["window"]
        
        # Add Component Styles
        # Sidebar background hardcoded to Dark Sidebar color since we are locked
        style += f"\nQWidget#sidebarContainer {{ background-color: #252526; border-right: 1px solid #333; }}"
        
        # Page Styles
        style += f"\nQLabel#pageHeader {{ {theme['pageHeader']} }}"
        style += f"\nQLabel#pageDesc {{ {theme['pageDesc']} }}"
        style += f"\nQPushButton#actionButton {{ {theme['actionButton']} }}"
        style += f"\nQPushButton#homeCard {{ {theme['homeCard']} }}"
        style += f"\nQLineEdit {{ {theme['inputField']} }}"
        style += f"\nQComboBox {{ {theme['inputField']} }}"
        
        # List Widget
        style += f"\n{theme['list_widget']}"
        
        self.setStyleSheet(style)
        
        self.sidebar.setStyleSheet(theme["sidebar"]) 
        self.status_bar.setStyleSheet(theme["statusBar"])
