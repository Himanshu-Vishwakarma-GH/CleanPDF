from PyQt6.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction

class FileListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        
        # Styles are now handled by the central Theme manager
        self.setObjectName("fileListWidget")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path:
                    self.add_file_item(file_path)
        else:
            super().dropEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            self.remove_selected_items()
        else:
            super().keyPressEvent(event)

    def add_file_item(self, path):
        # Prevent duplicates? (Optional, but user might want same file twice for merge)
        # Let's allow duplicates for now as per simple reqs, or can check if needed.
        item = QListWidgetItem(path)
        # Set icon based on extension?
        item.setToolTip(path)
        self.addItem(item)

    def remove_selected_items(self):
        for item in self.selectedItems():
            self.takeItem(self.row(item))

    def get_all_files(self):
        files = []
        for i in range(self.count()):
            files.append(self.item(i).text())
        return files
