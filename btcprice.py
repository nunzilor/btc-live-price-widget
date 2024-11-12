import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

class BitcoinPriceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.last_price = None  # To track the previous price
        self.bitcoin_balance = 0.11319928  # Amount of Bitcoin owned
        self.refresh_interval = 10  # Refresh interval in seconds (default)
        self.initUI()
        self.create_tray_icon()
        self.update_price()  # Fetch the price immediately on start
        self.start_timer()

    def initUI(self):
        self.setWindowTitle('Bitcoin Price and Total Value')
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout()
        
        # Label for Bitcoin price
        self.price_label = QLabel('Loading price...', self)
        self.layout.addWidget(self.price_label)
        
        # Label for total value in USD
        self.total_value_label = QLabel('Loading total value...', self)
        self.layout.addWidget(self.total_value_label)
        
        # Input field for refresh interval
        self.interval_input = QLineEdit(self)
        self.interval_input.setPlaceholderText('Refresh interval (seconds)')
        self.layout.addWidget(self.interval_input)
        
        # Button to set the refresh interval
        self.set_interval_button = QPushButton('Set Interval', self)
        self.set_interval_button.clicked.connect(self.set_refresh_interval)
        self.layout.addWidget(self.set_interval_button)

        self.setLayout(self.layout)

    def create_tray_icon(self):
        # Create the tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("bitcoin_icon.png"))  # Use an icon of your choice
        self.tray_icon.setToolTip("Loading Bitcoin price...")  # Initial tooltip
        
        # Tray icon menu
        tray_menu = QMenu()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        tray_menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # Single left-click
            self.show()  # Show the window when the tray icon is clicked

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_price)
        self.timer.start(self.refresh_interval * 1000)  # Convert seconds to milliseconds

    def set_refresh_interval(self):
        try:
            interval = int(self.interval_input.text())
            if interval > 0:
                self.refresh_interval = interval
                self.timer.setInterval(self.refresh_interval * 1000)
        except ValueError:
            self.interval_input.setText('Please enter a valid number')

    def update_price(self):
        try:
            # API request for live price
            response = requests.get('https://api.coindesk.com/v1/bpi/currentprice/USD.json')
            data = response.json()
            price = float(data['bpi']['USD']['rate'].replace(',', ''))  # Live Bitcoin price in USD
            
            # Calculate total value
            total_value = self.bitcoin_balance * price
            
            # Determine price direction (▲ or ▼)
            if self.last_price is not None:
                if price > self.last_price:
                    direction = " ▲"  # Green arrow
                elif price < self.last_price:
                    direction = " ▼"  # Red arrow
                else:
                    direction = ""  # No change
            else:
                direction = ""  # No change on first update

            # Update the labels with values
            self.price_label.setText(f'Bitcoin Price: ${price:.2f} USD{direction}')
            self.total_value_label.setText(f'Total Value: ${total_value:.2f} USD')

            # Update the tray icon tooltip
            self.tray_icon.setToolTip(f'Bitcoin Price: ${price:.2f} USD')
            
            # Update the previous price
            self.last_price = price
        except Exception as e:
            self.price_label.setText('Error fetching price')
            self.total_value_label.setText('---')
            self.tray_icon.setToolTip('Error fetching price')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # App keeps running even if the main window is closed
    ex = BitcoinPriceApp()
    ex.show()
    sys.exit(app.exec_())
