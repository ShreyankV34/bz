import sys
import numpy as np
import matplotlib.pyplot as plt
import qtawesome as qta

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtCore import Qt


# Class to represent the Matplotlib Plot
class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_data(self, x, y_list, labels, title):
        self.ax.clear()  # Clear previous data
        for y, label in zip(y_list, labels):
            self.ax.plot(x, y, label=label)  # Plot each y series with its label
        self.ax.set_title(title)
        self.ax.legend()  # Add legend for multiple lines
        self.canvas.draw()  # Redraw canvas


# Main Window Class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main layout
        self.setWindowTitle("Engine Plot Toggle")
        self.setGeometry(100, 100, 1000, 600)
        main_layout = QVBoxLayout()

        # Create two matplotlib widgets for comparison
        self.engine1_plot = MatplotlibWidget()
        self.engine2_plot = MatplotlibWidget()

        # Plot sample data
        x = np.linspace(0, 10, 100)

        # Engine 1 has multiple plots (e.g., torque, speed, temperature)
        y1_list = [np.sin(x), np.cos(x), np.sin(x) * np.cos(x)]
        labels1 = ['Torque', 'Speed', 'Temperature']

        # Engine 2 has multiple plots (e.g., torque, speed, temperature)
        y2_list = [np.cos(x), np.sin(x), np.cos(x)**2]
        labels2 = ['Torque', 'Speed', 'Temperature']

        self.engine1_plot.plot_data(x, y1_list, labels1, 'Engine 1 Data')
        self.engine2_plot.plot_data(x, y2_list, labels2, 'Engine 2 Data')

        # Horizontal layout for plots
        plots_layout = QHBoxLayout()
        plots_layout.addWidget(self.engine1_plot)
        plots_layout.addWidget(self.engine2_plot)

        # Add the layout to the main layout
        main_layout.addLayout(plots_layout)

        # Create a toggle button with qtawesome icon
        self.toggle_button = QPushButton()
        self.toggle_button.setIcon(qta.icon('fa.exchange', color='blue'))
        self.toggle_button.setToolTip("Toggle between comparison and stacked view")
        self.toggle_button.clicked.connect(self.toggle_comparison)

        # Add the toggle button in the top right corner
        top_layout = QHBoxLayout()
        top_layout.addStretch()  # Push the button to the right
        top_layout.addWidget(self.toggle_button)

        main_layout.addLayout(top_layout)

        # Create a central widget and set the main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Initialize toggle state
        self.comparison_mode = True  # Start in comparison mode

        # Save the data to use for toggling
        self.x = x
        self.y1_list = y1_list
        self.labels1 = labels1
        self.y2_list = y2_list
        self.labels2 = labels2

    def toggle_comparison(self):
        """Toggle between comparison and stacked views."""
        if self.comparison_mode:
            # Switch to stacked view (combine both engines into the same graph)
            combined_y_list = [y1 + y2 for y1, y2 in zip(self.y1_list, self.y2_list)]
            combined_labels = [f'{label1} + {label2}' for label1, label2 in zip(self.labels1, self.labels2)]
            self.engine1_plot.plot_data(self.x, combined_y_list, combined_labels, 'Combined Engine Data')
            self.engine2_plot.setVisible(False)  # Hide the second plot
        else:
            # Switch back to side-by-side comparison
            self.engine1_plot.plot_data(self.x, self.y1_list, self.labels1, 'Engine 1 Data')
            self.engine2_plot.plot_data(self.x, self.y2_list, self.labels2, 'Engine 2 Data')
            self.engine2_plot.setVisible(True)  # Show the second plot

        self.comparison_mode = not self.comparison_mode  # Toggle the state


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())