# pip install PySide6
import sys, threading, time
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QProgressBar, QMessageBox
)
from PySide6.QtCore import Signal, QObject

class Worker(QObject):
    done = Signal()

    def run(self):
        time.sleep(3)
        self.done.emit()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 GUI 範例")
        self.resize(520, 200)

        v = QVBoxLayout(self)

        # 檔案選擇
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("選擇檔案："))
        self.path_edit = QLineEdit()
        btn_browse = QPushButton("瀏覽…")
        btn_browse.clicked.connect(self.choose_file)
        row1.addWidget(self.path_edit)
        row1.addWidget(btn_browse)
        v.addLayout(row1)

        # 輸入與執行
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("輸入文字："))
        self.text_edit = QLineEdit()
        self.run_btn = QPushButton("執行長任務")
        self.run_btn.clicked.connect(self.long_task)
        row2.addWidget(self.text_edit)
        row2.addWidget(self.run_btn)
        v.addLayout(row2)

        # 進度與狀態
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # 不確定時間 → 無限動畫
        self.progress.setVisible(False)
        v.addWidget(self.progress)

        self.status = QLabel("就緒")
        v.addWidget(self.status)

    def choose_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "選擇檔案")
        if path:
            self.path_edit.setText(path)

    def long_task(self):
        self.run_btn.setEnabled(False)
        self.progress.setVisible(True)
        self.status.setText("執行中…")

        worker = Worker()
        worker.done.connect(self.finish_task)

        t = threading.Thread(target=worker.run, daemon=True)
        t.start()
        self._worker = worker  # 保持引用，避免被 GC

    def finish_task(self):
        self.progress.setVisible(False)
        self.run_btn.setEnabled(True)
        self.status.setText("完成 ✅")
        QMessageBox.information(self, "完成", "長任務已結束！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = App()
    w.show()
    sys.exit(app.exec())
