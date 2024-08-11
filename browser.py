import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the title of the window
        self.setWindowTitle("151D Browser")

        # Set the initial size of the browser window
        self.setGeometry(100, 100, 1200, 800)  # (x, y, width, height)

        # Create a browser widget
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))  # Default home page

        # Set the browser as the central widget of the window
        self.setCentralWidget(self.browser)

        # Create navigation bar
        self.navbar = QToolBar()
        self.addToolBar(self.navbar)

        # Add back button
        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.browser.back)
        self.navbar.addAction(back_btn)

        # Add forward button
        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(self.browser.forward)
        self.navbar.addAction(forward_btn)

        # Add reload button
        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        self.navbar.addAction(reload_btn)

        # Add stop button
        stop_btn = QAction("Stop", self)
        stop_btn.triggered.connect(self.browser.stop)
        self.navbar.addAction(stop_btn)

        # Add URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar)

        # Update URL bar when the URL changes
        self.browser.urlChanged.connect(self.update_url_bar)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("151D Browser")
    window = Browser()
    window.show()
    sys.exit(app.exec_())
