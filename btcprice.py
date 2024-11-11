import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer

class BitcoinPriceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.last_price = None  # Per tenere traccia del prezzo precedente
        self.bitcoin_balance = 0.11319928  # Quantità di Bitcoin posseduti
        self.initUI()
        self.update_price()  # Aggiorna subito il prezzo all'avvio
        self.start_timer()

    def initUI(self):
        self.setWindowTitle('Prezzo Bitcoin e Valore Totale')
        self.setGeometry(100, 100, 400, 150)
        self.layout = QVBoxLayout()
        
        # Etichetta per il prezzo del Bitcoin
        self.price_label = QLabel('Caricamento prezzo...', self)
        self.layout.addWidget(self.price_label)
        
        # Etichetta per il valore totale in USD
        self.total_value_label = QLabel('Caricamento valore totale...', self)
        self.layout.addWidget(self.total_value_label)
        
        self.setLayout(self.layout)

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_price)
        self.timer.start(10000)  # 10.000 millisecondi = 10 secondi

    def update_price(self):
        try:
            # Richiesta API per il prezzo live
            response = requests.get('https://api.coindesk.com/v1/bpi/currentprice/USD.json')
            data = response.json()
            price = float(data['bpi']['USD']['rate'].replace(',', ''))  # Prezzo live del Bitcoin in USD
            
            # Calcolo del valore totale
            total_value = self.bitcoin_balance * price
            
            # Determina direzione del prezzo (▲ o ▼)
            if self.last_price is not None:
                if price > self.last_price:
                    direction = " ▲"  # Freccia verde
                elif price < self.last_price:
                    direction = " ▼"  # Freccia rossa
                else:
                    direction = ""  # Nessun cambiamento
            else:
                direction = ""  # Nessun cambiamento al primo aggiornamento

            # Aggiorna le etichette con i valori
            self.price_label.setText(f'Prezzo Bitcoin: ${price:.2f} USD{direction}')
            self.total_value_label.setText(f'valore dei miei btc: ${total_value:.2f} USD')
            
            # Aggiorna il prezzo precedente
            self.last_price = price
        except Exception as e:
            self.price_label.setText('Errore nel recupero del prezzo')
            self.total_value_label.setText('---')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BitcoinPriceApp()
    ex.show()
    sys.exit(app.exec_())
