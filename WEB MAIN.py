import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtNetwork import QNetworkProxy
from PyQt5.QtNetwork import QNetworkProxy
def set_vpn_proxy(self):
    proxy, ok = QInputDialog.getText(self, 'Set VPN Proxy', 'Enter proxy address (e.g., socks5://127.0.0.1:9150):') 
    if ok and proxy:
        try:
            proxy_url = QUrl(proxy)
            if proxy_url.isValid():
                proxy = QNetworkProxy()
                proxy_type = QNetworkProxy.Socks5Proxy if proxy_url.scheme() == 'socks5' else QNetworkProxy.HttpProxy
                proxy.setType(proxy_type)
                proxy.setHostName(proxy_url.host())
                proxy.setPort(proxy_url.port())
                QNetworkProxy.setApplicationProxy(proxy)
                QMessageBox.information(self, "Proxy Set", f"VPN Proxy set to {proxy}")
            else:
                QMessageBox.warning(self, "Invalid Proxy", "The entered proxy address is invalid.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to set proxy: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)


        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)


        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.tabs.currentChanged.connect(self.current_tab_changed)



        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join('icons', 'cil-arrow-circle-left.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        navtb.addAction(back_btn)

        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())





        next_btn = QAction(QIcon(os.path.join('icons', 'cil-arrow-circle-right.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        navtb.addAction(next_btn)

        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())





        reload_btn = QAction(QIcon(os.path.join('icons', 'cil-reload.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        navtb.addAction(reload_btn)

        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())





        home_btn = QAction(QIcon(os.path.join('icons', 'cil-home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        navtb.addAction(home_btn)

        home_btn.triggered.connect(self.navigate_home)






        navtb.addSeparator()


        self.httpsicon = QLabel()  
        self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cil-lock-unlocked.png')))
        navtb.addWidget(self.httpsicon)


        self.urlbar = QLineEdit()
        navtb.addWidget(self.urlbar)

        self.urlbar.returnPressed.connect(self.navigate_to_url)




        stop_btn = QAction(QIcon(os.path.join('icons', 'cil-media-stop.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        navtb.addAction(stop_btn)

        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())



        file_menu = self.menuBar().addMenu("&File")

        new_tab_action = QAction(QIcon(os.path.join('icons', 'cil-library-add.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        file_menu.addAction(new_tab_action)

        new_tab_action.triggered.connect(lambda _: self.add_new_tab())

        vpn_proxy_action = QAction(QIcon(os.path.join('icons', 'cil-vpn.png')), "VPN Proxy", self)
        vpn_proxy_action.setStatusTip("Set VPN Proxy")
        file_menu.addAction(vpn_proxy_action)
        vpn_proxy_action.triggered.connect(self.set_vpn_proxy)



        help_menu = self.menuBar().addMenu("&Help")

        navigate_home_action = QAction(QIcon(os.path.join('icons', 'cil-exit-to-app.png')),
                                            "Homepage", self)
        navigate_home_action.setStatusTip("Go to google")
        help_menu.addAction(navigate_home_action)

        navigate_home_action.triggered.connect(self.navigate_home)

        self.setWindowTitle("Infinix Browser")
        self.setWindowIcon(QIcon(os.path.join('icons', 'cil-screen-desktop.png')))



        self.setStyleSheet("""QWidget{
           background-color: rgb(48, 48, 48);
           color: rgb(255, 255, 255);
        }
        QTabWidget::pane { /* The tab widget frame */
            border-top: 2px solid rgb(90, 90, 90);
            position: absolute;
            top: -0.5em;
            color: rgb(255, 255, 255);
            padding: 5px;
        }

        QTabWidget::tab-bar {
            alignment: left;
        }

        /* Style the tab using the tab sub-control. Note that
            it reads QTabBar _not_ QTabWidget */
        QLabel, QToolButton, QTabBar::tab {
            background: rgb(90, 90, 90);
            border: 2px solid rgb(90, 90, 90);
            /*border-bottom-color: #C2C7CB; /* same as the pane color */
            border-radius: 10px;
            min-width: 8ex;
            padding: 5px;
            margin-right: 2px;
            color: rgb(255, 255, 255);
        }

        QLabel:hover, QToolButton::hover, QTabBar::tab:selected, QTabBar::tab:hover {
            background: rgb(49, 49, 49);
            border: 2px solid rgb(0, 36, 36);
            background-color: rgb(0, 36, 36);
        }

        QLineEdit {
            border: 2px solid rgb(0, 36, 36);
            border-radius: 10px;
            padding: 5px;
            background-color: rgb(0, 36, 36);
            color: rgb(255, 255, 255);
        }
        QLineEdit:hover {
            border: 2px solid rgb(0, 66, 124);
        }
        QLineEdit:focus{
            border: 2px solid rgb(0, 136, 255);
            color: rgb(200, 200, 200);
        }
        QPushButton{
            background: rgb(49, 49, 49);
            border: 2px solid rgb(0, 36, 36);
            background-color: rgb(0, 36, 36);
            padding: 5px;
            border-radius: 10px;
        }""")




        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')


        self.show()


    def add_new_tab(self, qurl=None, label="Blank"):

        if qurl is None:
            qurl = QUrl('')


        browser = QWebEngineView()
        browser.setUrl(qurl)


        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)


        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))



    def tab_open_doubleclick(self, i):
        if i == -1:  
            self.add_new_tab()


    def close_current_tab(self, i):
        if self.tabs.count() < 2: 
            return

        self.tabs.removeTab(i)



    def update_urlbar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            return
        if q.scheme() == 'https':
            self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cil-lock-locked.png')))

        else:

            self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cil-lock-unlocked.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)




    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()

        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())



    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(title)



    def navigate_to_url(self):
        user_input=self.urlbar.text().strip()
        user_input="https://"+user_input+".com/"
        q=QUrl(user_input)
        self.tabs.currentWidget().setUrl(q)



    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://sprightly-dusk-ad7b95.netlify.app/"))

    def set_vpn_proxy(self):
        proxy, ok = QInputDialog.getText(self, 'Set VPN Proxy', 'Enter proxy address (e.g., socks5://127.0.0.1:9150):')
        if ok and proxy:
            try:
                proxy_url = QUrl(proxy)
                if proxy_url.isValid():
                    proxy = QNetworkProxy()
                    proxy.setType(QNetworkProxy.Socks5Proxy)
                    proxy.setHostName(proxy_url.host())
                    proxy.setPort(proxy_url.port())
                    QNetworkProxy.setApplicationProxy(proxy)
                    QMessageBox.information(self, "Proxy Set", f"VPN Proxy set to {proxy}")
                else:
                    QMessageBox.warning(self, "Invalid Proxy", "The entered proxy address is invalid.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to set proxy: {str(e)}")






app = QApplication(sys.argv)

app.setApplicationName("Infinix Browser")

app.setOrganizationName("Race to infinity")

app.setOrganizationDomain("Infinix.org")

window = MainWindow()
app.exec_()
