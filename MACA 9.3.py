import sys
import os
import pandas as pd
import numpy as np
import yfinance as yf
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
    QLabel, QLineEdit, QPushButton, QSlider, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon
import matplotlib.pyplot as plt
import seaborn as sns
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QDialog,  QDialogButtonBox
figure_count = 1
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    
# Fetch live data for multiple assets (stocks, bonds, crypto)
def fetch_asset_data(tickers, start_date="2020-01-01", end_date="2024-01-01"):
    """
    Fetches historical data for multiple tickers (stocks, bonds, crypto) using Yahoo Finance.
    """
    try:
        data = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]
        return data
    except Exception as e:
        print(f"Error fetching data for tickers {tickers}: {e}")
        return None

# Calculate correlation matrix between assets
def calculate_correlation(data):
    """
    Calculate correlation matrix between multiple asset classes.
    """
    # Fill missing data before calculating pct_change
    data = data.ffill()  # Forward fill missing data

    return data.pct_change().corr()


# Visualize correlation matrix
# Visualize correlation matrix
 

def visualize_correlation(correlation_matrix, window):
    global figure_count
    fig, ax = plt.subplots(figsize=(10, 8))

    fig.canvas.manager.set_window_title(f"MACA {figure_count}")  # Set custom title

    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", vmin=-1, vmax=1, ax=ax)
    plt.title("Correlation Matrix")
    
    # Embed the figure in the PyQt window
    canvas = FigureCanvas(fig)
    window.layout.addWidget(canvas)  # Add the canvas to the PyQt window layout

    window.setWindowTitle("Multi-Asset Correlation Analyzer")  # Reset to your app's title

def on_analyze_button_clicked(self):
    """
    Fetches and analyzes data for multiple assets, calculates correlation, and displays the results.
    """
    tickers = self.tickers_input.text().strip().upper().split(",")
    if not tickers:
        QMessageBox.warning(self, "Invalid Input", "Please enter valid asset tickers.")
        return

    # Fetch asset data
    data = fetch_asset_data(tickers)
    if data is None or data.empty:
        QMessageBox.warning(self, "No Data", "No data available for the entered assets.")
        return

    # Calculate correlations
    correlation_matrix = calculate_correlation(data)
    
    # Update table with correlation values
    self.update_table(correlation_matrix)

    # Visualize correlation matrix and pass the main window (self)
    visualize_correlation(correlation_matrix, self)



class MultiAssetCorrelationAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-Asset Correlation Analyzer")
        self.setGeometry(100, 100, 900, 700)
        self.setWindowIcon(QIcon("logo.png"))
        self.set_theme()

        self.main_widget = QWidget(self)
        self.layout = QVBoxLayout(self.main_widget)

        self.add_widgets()
        self.setCentralWidget(self.main_widget)

    def set_theme(self):
        """
        Sets an enterprise blue theme for the application.
        """
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 68, 204))  # Enterprise blue
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

    def add_widgets(self):
        """
        Adds the main widgets to the GUI.
        """
        title = QLabel("Multi-Asset Correlation Analyzer", self)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16))
        self.layout.addWidget(title)

        # Ticker input for multiple assets
        self.tickers_input = QLineEdit(self)
        self.tickers_input.setPlaceholderText("Enter asset tickers (e.g., AAPL, BTC-USD, AGG)")
        self.layout.addWidget(self.tickers_input)

        # Analyze button
        self.analyze_button = QPushButton("Analyze Correlation", self)
        self.analyze_button.clicked.connect(self.on_analyze_button_clicked)
        self.layout.addWidget(self.analyze_button)

        # Table to display correlation results
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

        # Menu buttons for Help and About
        menu_layout = QHBoxLayout()
        help_button = QPushButton("Help", self)
        help_button.clicked.connect(self.show_help)
        about_button = QPushButton("About", self)
        about_button.clicked.connect(self.show_about)
        menu_layout.addWidget(help_button)
        menu_layout.addWidget(about_button)
        self.layout.addLayout(menu_layout)

    def on_analyze_button_clicked(self):
        """
        Fetches and analyzes data for multiple assets, calculates correlation, and displays the results.
        """
        tickers = self.tickers_input.text().strip().upper().split(",")
        if not tickers:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid asset tickers.")
            return
    
        # Fetch asset data
        data = fetch_asset_data(tickers)
        if data is None or data.empty:
            QMessageBox.warning(self, "No Data", "No data available for the entered assets.")
            return
    
        # Calculate correlations
        correlation_matrix = calculate_correlation(data)
        
        # Update table with correlation values
        self.update_table(correlation_matrix)
    
        # Visualize correlation matrix and pass the main window (self)
        visualize_correlation(correlation_matrix, self)  # This passes 'self' (the window) as the second argument

    def update_table(self, correlation_matrix):
        """
        Updates the table with the correlation results.
        """
        self.table.setColumnCount(len(correlation_matrix.columns))
        self.table.setRowCount(len(correlation_matrix.index))
        self.table.setHorizontalHeaderLabels(correlation_matrix.columns)
        self.table.setVerticalHeaderLabels(correlation_matrix.index)

        for i, row in enumerate(correlation_matrix.index):
            for j, col in enumerate(correlation_matrix.columns):
                self.table.setItem(i, j, QTableWidgetItem(f"{correlation_matrix.iloc[i, j]:.2f}"))

 
    
 
    
  
    
    def show_help(self):
        """
        Displays a detailed help section with information on how to use the application and interpret results.
        """
        help_text = """
        <b>How to Use the Multi-Asset Correlation Analyzer</b><br><br>
        1. <b>Enter Tickers:</b> In the text input field, enter the asset tickers separated by commas (e.g., AAPL, BTC-USD, AGG).<br>
        2. <b>Analyze Correlation:</b> Click the 'Analyze Correlation' button to fetch historical data for the entered assets.<br>
        3. <b>Correlation Matrix:</b> A correlation matrix will be calculated and displayed. This matrix shows how different asset classes move relative to each other.<br><br>
    
        <b>Interpreting the Results:</b><br>
        - Each cell in the correlation matrix represents the correlation coefficient between two assets.<br>
        - A value close to 1 means the assets are highly correlated (they move in the same direction).<br>
        - A value close to -1 means the assets are negatively correlated (they move in opposite directions).<br>
        - A value close to 0 means the assets are uncorrelated (their movements are independent).<br><br>
    
        <b>Correlation Example:</b><br>
        If you enter "AAPL, BTC-USD, AGG" and analyze, the table will show how each of these assets correlate with each other based on historical price data.<br>
        """
    
        # Create a QDialog window to display the help content
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Help")
        help_dialog.setWindowModality(Qt.ApplicationModal)
        help_dialog.setMinimumSize(1000, 800)  # Set a large initial size
        
        # Create the main layout for the dialog
        layout = QVBoxLayout(help_dialog)
    
        # Create a QLabel to display the help text
        help_label = QLabel(help_text, self)
        help_label.setWordWrap(True)
        help_label.setAlignment(Qt.AlignLeft)
    
        # Create a QScrollArea to allow scrolling if content overflows
        scroll_area = QScrollArea(help_dialog)
        scroll_area.setWidget(help_label)
        scroll_area.setWidgetResizable(True)  # Allow resizing of the widget inside the scroll area
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Always show vertical scroll bar
    
        # Add the scroll area to the dialog layout
        layout.addWidget(scroll_area)
    
        # Add a close button
        close_button = QPushButton("Close", help_dialog)
        close_button.clicked.connect(help_dialog.accept)  # Close the dialog when clicked
        layout.addWidget(close_button)
    
        help_dialog.setLayout(layout)  # Set the layout for the dialog
        
        help_dialog.exec_()  # Show the dialog

    def show_about(self):
        """
        Displays an about section with information about the application.
        """
        about_text = """
        <b>Multi-Asset Correlation Analyzer</b><br><br>
        Version: 9.3<br>
        (c) 2024 Peter De Ceuster<br><br>
        This application allows you to analyze the correlation between multiple assets, including stocks, bonds, and cryptocurrencies.<br>
        It fetches historical price data from Yahoo Finance, calculates correlations, and visualizes the results with a heatmap.<br>
        <br>Visit us at <a href='http://peterdeceuster.uk'>peterdeceuster.uk</a>
        """
        QMessageBox.information(self, "About", about_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MultiAssetCorrelationAnalyzer()
    window.showMaximized()  # Start the window maximized
    window.show()
    sys.exit(app.exec_())  # Only this line should call exec_()
