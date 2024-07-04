from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Qt
import sys

class BraytonCycleGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Brayton Cycle Calculator")

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Form layout for inputs
        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        # Input fields
        self.p1_input = QLineEdit()
        self.t1_input = QLineEdit()
        self.cp_input = QLineEdit()
        self.cv_input = QLineEdit()
        self.compressor_efficiency_input = QLineEdit()
        self.turbine_efficiency_input = QLineEdit()

        # Add input fields to the form
        self.form_layout.addRow("P1 (kPa):", self.p1_input)
        self.form_layout.addRow("T1 (K):", self.t1_input)
        self.form_layout.addRow("Cp (kJ/kgK):", self.cp_input)
        self.form_layout.addRow("Cv (kJ/kgK):", self.cv_input)
        self.form_layout.addRow("Compressor Efficiency (%):", self.compressor_efficiency_input)
        self.form_layout.addRow("Turbine Efficiency (%):", self.turbine_efficiency_input)

        # Calculate button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_brake_cycle)
        self.layout.addWidget(self.calculate_button)

        # Result labels
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.result_label)

    def calculate_brake_cycle(self):
        try:
            # Get inputs
            P1 = float(self.p1_input.text())
            T1 = float(self.t1_input.text())
            Cp = float(self.cp_input.text())
            Cv = float(self.cv_input.text())
            compressor_efficiency = float(self.compressor_efficiency_input.text()) / 100
            turbine_efficiency = float(self.turbine_efficiency_input.text()) / 100

            # Calculate gamma
            gamma = Cp / Cv

            # Calculate P2 and T2 (assuming isentropic compression)
            P2 = P1 * (T1 * (gamma - 1) / gamma)
            T2 = T1 * ((P2 / P1) ** ((gamma - 1) / gamma))

            # Calculate work done by the compressor
            compressor_work = Cp * (T2 - T1) / compressor_efficiency

            # Calculate T3 and P3 (assuming isentropic expansion)
            P3 = P1
            T3 = T2 / ((P3 / P2) ** ((gamma - 1) / gamma))

            # Calculate work done by the turbine
            turbine_work = Cp * (T2 - T3) * turbine_efficiency

            # Calculate net work done
            net_work_done = turbine_work - compressor_work

            # Calculate thermal efficiency
            thermal_efficiency = 1 - (1 / (P2 / P1) ** ((gamma - 1) / gamma))

            # Display results
            result_text = (f"Net Work Done: {net_work_done:.2f} kJ/kg\n"
                           f"Thermal Efficiency: {thermal_efficiency * 100:.2f}%")
            self.result_label.setText(result_text)

        except ValueError:
            self.result_label.setText("Please enter valid numerical values.")

def main():
    app = QApplication(sys.argv)
    window = BraytonCycleGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
