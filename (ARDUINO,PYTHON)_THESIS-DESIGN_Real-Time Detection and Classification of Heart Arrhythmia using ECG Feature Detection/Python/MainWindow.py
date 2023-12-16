import csv
import os
import statistics
import sys
import time
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import serial
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets, uic

from CustomLib.CustomQtWidgets import CustomQtWidgets
from ECG import ECG


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

    def closeEvent(self, event):
        is_close = CustomQtWidgets.do_get_question(
            self, "Quit", "Are you sure want to quit?"
        )

        if is_close:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


class MainWindow(Window):
    def __init__(self):
        super().__init__()
        uic.loadUi("MainWindow.ui", self)
        self.setFixedSize(self.size())
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()

        # CONSTANTS
        self.TIMER_SECONDS = 10
        self.REFERENCE_VOLTAGE = 3.3
        self.VOLTAGE_CALIBRATION = 10  # mm/mV
        self.PAPER_SPEED = 25  # mm/s
        self.BAUDRATE = 9600

        # BUTTONS
        self.pushButton_Input.clicked.connect(self.pushButton_Input_Clicked)
        self.pushButton_Start.clicked.connect(self.pushButton_Start_Clicked)
        self.pushButton_ClearSelection.clicked.connect(
            self.pushButton_ClearSelection_Clicked
        )
        self.pushButton_SaveData.clicked.connect(self.pushButton_SaveData_Clicked)
        self.pushButton_IndexConfirm.clicked.connect(
            self.pushButton_IndexConfirm_Clicked
        )

        # CREAET FIG, CANVAS, AXES
        self.fig_raw, self.canvas_raw, self.ax_raw = self.create_canvas(
            self.verticalLayout_ECGRaw
        )
        self.fig_cleaned, self.canvas_cleaned, self.ax_cleaned = self.create_canvas(
            self.verticalLayout_ECGCleaned
        )
        (
            self.fig_delineate,
            self.canvas_delineate,
            self.ax_delineate,
        ) = self.create_canvas(self.verticalLayout_ECGDelineate)

    def display_graph_features(self):
        # SHOW COMPUTED SAMPLING RATE
        self.lineEdit_SamplingRate.setText(str(self.sampling_rate))

        # PROCESS THE RAW ECG DATA
        self.ECG_SIGNAL = ECG(self.ecg_raw, sampling_rate=self.sampling_rate)

        # SHOW GRAPH
        self.ECG_SIGNAL.ecg_raw_plot(self.ecg_raw, self.ax_raw)
        self.canvas_raw.draw()
        self.ECG_SIGNAL.ecg_cleaned_plot(self.ax_cleaned)
        self.canvas_cleaned.draw()
        self.ECG_SIGNAL.ecg_delineate_plot(self.ax_delineate)
        self.canvas_delineate.draw()

        # SHOW FEATURES
        self.lineEdit_HeartRate.setText(
            str(round(self.ECG_SIGNAL.Heart_Rate, 4)) + " bpm"
        )
        self.lineEdit_PPeakAve.setText(
            str(
                round(
                    self.ECG_SIGNAL.ECG["Peaks_Ave"]["P"] * self.VOLTAGE_CALIBRATION,
                    4,
                )
            )
            + " mm"
        )
        self.lineEdit_QPeakAve.setText(
            str(
                round(
                    self.ECG_SIGNAL.ECG["Peaks_Ave"]["Q"] * self.VOLTAGE_CALIBRATION,
                    4,
                )
            )
            + " mm"
        )
        self.lineEdit_QRSCompInterval.setText(
            str(round(self.ECG_SIGNAL.ECG["QRS_Interval_Ave"], 4)) + " s"
        )
        self.lineEdit_RRInterval.setText(
            str(round(self.ECG_SIGNAL.ECG["RR_Interval_Ave"], 4)) + " s"
        )
        self.lineEdit_TPeakAve.setText(
            str(
                round(
                    self.ECG_SIGNAL.ECG["Peaks_Ave"]["T"] * self.VOLTAGE_CALIBRATION,
                    4,
                )
            )
            + " mm"
        )
        self.lineEdit_STInterval.setText(
            str(round(self.ECG_SIGNAL.ECG["ST_Interval_Ave"], 4)) + " s"
        )
        self.lineEdit_QSInterval.setText(
            str(round(self.ECG_SIGNAL.ECG["QS_Interval_Ave"], 4)) + " s"
        )

    def display_findings(self):
        ECG_SIGNAL = self.ECG_SIGNAL
        VOLTS_TO_METERS_FACTOR = self.VOLTAGE_CALIBRATION
        PAPER_SPEED = self.PAPER_SPEED

        FINDINGS = ""

        # EXTRACTED FEATURES
        HEART_RATE = self.ECG_SIGNAL.Heart_Rate
        ST_PEAK_AVE = (
            (ECG_SIGNAL.ECG["Offsets_Ave"]["R"] + ECG_SIGNAL.ECG["Onsets_Ave"]["T"]) / 2
        ) * VOLTS_TO_METERS_FACTOR
        P_PEAK_AVE = ECG_SIGNAL.ECG["Peaks_Ave"]["P"] * VOLTS_TO_METERS_FACTOR
        T_PEAK_AVE = ECG_SIGNAL.ECG["Peaks_Ave"]["T"] * VOLTS_TO_METERS_FACTOR
        R_PEAK_AVE = ECG_SIGNAL.ECG["Peaks_Ave"]["R"] * VOLTS_TO_METERS_FACTOR
        PWAVE_INTERVAL_AVE = ECG_SIGNAL.ECG["PWave_Interval_Ave"]
        TWAVE_INTERVAL_AVE = ECG_SIGNAL.ECG["TWave_Interval_Ave"]
        QS_INTERVAL_AVE = ECG_SIGNAL.ECG["QS_Interval_Ave"]
        PR_INTERVAL_AVE = ECG_SIGNAL.ECG["PR_Interval_Ave"]
        QT_INTERVAL_AVE = ECG_SIGNAL.ECG["QT_Interval_Ave"]
        QS_INTERVAL_AVE_METERS = ECG_SIGNAL.ECG["QS_Interval_Ave"] * PAPER_SPEED
        RR_INTERVAL_AVE_METERS = ECG_SIGNAL.ECG["RR_Interval_Ave"] * PAPER_SPEED
        QS_STDEV = statistics.stdev(ECG_SIGNAL.ECG["QS_Interval"])
        RR_STDEV = statistics.stdev(ECG_SIGNAL.ECG["RR_Interval"])

        # FINDINGS
        FINDINGS += f"HEART_RATE: {round(HEART_RATE, 4)} bpm\n"
        FINDINGS += f"ST_PEAK_AVE: {round(ST_PEAK_AVE, 4)} mm\n"
        FINDINGS += f"P_PEAK_AVE: {round(P_PEAK_AVE, 4)} mm\n"
        FINDINGS += f"T_PEAK_AVE: {round(T_PEAK_AVE, 4)} mm\n"
        FINDINGS += f"R_PEAK_AVE: {round(R_PEAK_AVE, 4)} mm\n"
        FINDINGS += f"PWAVE_INTERVAL_AVE: {round(PWAVE_INTERVAL_AVE, 4)} s\n"
        FINDINGS += f"TWAVE_INTERVAL_AVE: {round(TWAVE_INTERVAL_AVE, 4)} s\n"
        FINDINGS += f"QS_INTERVAL_AVE: {round(QS_INTERVAL_AVE, 4)} s\n"
        FINDINGS += f"PR_INTERVAL_AVE: {round(PR_INTERVAL_AVE, 4)} s\n"
        FINDINGS += f"QT_INTERVAL_AVE: {round(QT_INTERVAL_AVE, 4)} s\n"
        FINDINGS += f"QS_INTERVAL_AVE_METERS: {round(QS_INTERVAL_AVE_METERS, 4)} mm\n"
        FINDINGS += f"RR_INTERVAL_AVE_METERS: {round(RR_INTERVAL_AVE_METERS, 4)} mm\n"
        FINDINGS += f"QS_STDEV: {round(QS_STDEV, 4)} s\n"
        FINDINGS += f"RR_STDEV: {round(RR_STDEV, 4)} s\n"

        # Measure Cardiac Ischemia
        Cardiac_Ischemia_Threholds = [
            # 1ST CRITERIA ABNORMAL
            # not (
            #     PWAVE_INTERVAL_AVE < 0.12
            #     and P_PEAK_AVE < 2.5
            #     and QS_INTERVAL_AVE < 0.12
            #     and QS_INTERVAL_AVE_METERS < 3
            #     and R_PEAK_AVE > 5
            #     and TWAVE_INTERVAL_AVE < 0.2
            #     and T_PEAK_AVE < 5
            #     and PR_INTERVAL_AVE >= 0.12
            #     and PR_INTERVAL_AVE <= 0.20
            #     and QT_INTERVAL_AVE < 0.44
            # ),
            # 2ND CRITERIA ELEVATION
            ST_PEAK_AVE > 1,
            # 3RD CRITERIA DEPRESSION
            ST_PEAK_AVE < -0.5,
        ]
        for criteria in Cardiac_Ischemia_Threholds:
            if criteria:
                FINDINGS += "Detection: Cardiac Ischemia\n"
                break

        # Measure Ventricular Tachycardia
        Ventricular_Tachycardia_Threholds = [
            # 1ST CRITERIA
            P_PEAK_AVE < 1
            and T_PEAK_AVE < 1
            and QS_INTERVAL_AVE >= 0.10
            and RR_INTERVAL_AVE_METERS > 30,
            # 2ND CRITERIA
            P_PEAK_AVE < 1 and T_PEAK_AVE < 1 and QS_STDEV < 0.02 and RR_STDEV < 0.02,
            # 3RD CRITERIA
            P_PEAK_AVE < 1 and T_PEAK_AVE < 1 and (QS_STDEV > 0.1 or RR_STDEV > 0.1),
        ]
        for criteria in Ventricular_Tachycardia_Threholds:
            if criteria:
                FINDINGS += "Detection: Ventricular Tachycardia\n"
                break

        # Measure Atrial Fibrillation
        Atrial_Fibrillation_Thresholds = [
            # 1ST CRITERIA
            P_PEAK_AVE < 1.2
            and RR_STDEV > 0.1
            and (HEART_RATE < 60 or HEART_RATE > 100)
            and QS_STDEV > 0.1,
        ]
        for criteria in Atrial_Fibrillation_Thresholds:
            if criteria:
                FINDINGS += "Detection: Atrial Fibrillation\n"
                break

        self.plainTextEdit_Findings.setPlainText(FINDINGS)

    def reset_graph(self):
        # FIG RAW
        self.fig_raw.clf()
        self.ax_raw = self.fig_raw.add_subplot(111)
        self.fig_raw.tight_layout()
        self.canvas_raw.draw()
        # FIG CLEANED
        self.fig_cleaned.clf()
        self.ax_cleaned = self.fig_cleaned.add_subplot(111)
        self.fig_cleaned.tight_layout()
        self.canvas_cleaned.draw()
        # FIG DELINEATE
        self.fig_delineate.clf()
        self.ax_delineate = self.fig_delineate.add_subplot(111)
        self.fig_delineate.tight_layout()
        self.canvas_delineate.draw()

    def pushButton_IndexConfirm_Clicked(self):
        # INDEX THE SAMPLE | TO REMOVE THE NOISY PART
        get_index_start = self.spinBox_IndexStart.value()
        get_index_stop = self.spinBox_IndexStop.value()
        self.ecg_raw = self.ecg_raw_orig_copy[get_index_start:get_index_stop]
        self.reset_graph()
        self.display_graph_features()
        self.display_findings()

    def pushButton_Input_Clicked(self):
        file = CustomQtWidgets.do_get_filename(
            self,
            caption="Open ECG_Raw.csv",
            directory=os.getcwd(),
            filter="CSV (ECG_Raw.csv)",
        )
        if not file:
            return

        # CLEAR SELECTIONS FIRST
        self.pushButton_ClearSelection_Clicked()

        # DISPLAY INFO OF FILE
        path_names = file.split("/")
        start_time, end_time, sampling_rate = path_names[-2].split(" ")
        name, age = path_names[-3].split("-")
        self.lineEdit_Name.setText(name)
        self.lineEdit_Age.setText(age)
        self.lineEdit_StartTime.setText(start_time)
        self.lineEdit_EndTime.setText(end_time)
        self.lineEdit_SamplingRate.setText(sampling_rate)

        # DISPLAY MEDICAL INFORMATIONS
        parent = os.path.dirname(file)
        med_info_file = os.path.join(parent, "Medical_Information.csv")
        if os.path.isfile(med_info_file):
            with open(med_info_file, "r") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")
                for i, row in enumerate(csv_reader):
                    if i == 0:
                        self.lineEdit_NicotineLevels.setText(row[1])
                    if i == 1:
                        self.lineEdit_MonthsOfSmoking.setText(row[1])
                    if i == 2:
                        self.plainTextEdit_MedicalBackground.setPlainText(row[1])

        # GET ECG RAW DATA
        self.ecg_raw = np.genfromtxt(file, delimiter=",")
        self.ecg_raw_orig_copy = self.ecg_raw.copy()
        self.sampling_rate = float(sampling_rate)

        # DISPLAY GRAPH AND FINDINGS
        self.display_graph_features()
        self.display_findings()

        # INPUT START AND STOP INDEX
        self.spinBox_IndexStart.setValue(0)
        self.spinBox_IndexStop.setValue(len(self.ecg_raw))

    def pushButton_Start_Clicked(self):
        # GET START DATE/TIME
        dt_string = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        self.lineEdit_StartTime.setText(dt_string)

        # PUT CODE FOR ECG RAW DATA GATHERING
        COMPORT = self.lineEdit_COMPORT.text()
        ser = serial.Serial(port=COMPORT, baudrate=self.BAUDRATE)
        self.ecg_raw = []
        t_end = time.time() + self.TIMER_SECONDS
        while time.time() < t_end:
            try:
                incoming = ser.readline().decode().strip()
                if incoming:
                    self.ecg_raw.append(int(incoming))
            except Exception as e:
                continue
        ser.close()

        self.ecg_raw = np.array(self.ecg_raw) / 1023 * self.REFERENCE_VOLTAGE
        self.ecg_raw_orig_copy = self.ecg_raw.copy()
        self.sampling_rate = len(self.ecg_raw) / self.TIMER_SECONDS

        # DISPLAY GRAPH AND FINDINGS
        self.display_graph_features()
        self.display_findings()

        # INPUT START AND STOP INDEX
        self.spinBox_IndexStart.setValue(0)
        self.spinBox_IndexStop.setValue(len(self.ecg_raw))

        # GET END DATE/TIME
        dt_string = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        self.lineEdit_EndTime.setText(dt_string)

    def pushButton_ClearSelection_Clicked(self):
        # RESET GRAPH
        self.reset_graph()

        # CLEAR ALL INPUTS / QLineEdit / QPlainTextEdit
        self.plainTextEdit_Findings.clear()
        self.plainTextEdit_MedicalBackground.clear()
        for child in self.findChildren(QtWidgets.QLineEdit):
            if "COMPORT" not in child.objectName():
                child.clear()

    def pushButton_SaveData_Clicked(self):
        # VERIFY IF NAME, AGE, START/END DATE/TIME HAVE VALUES BEFORE SAVING
        if not (
            self.lineEdit_Name.text()
            and self.lineEdit_Age.text()
            and self.lineEdit_StartTime.text()
            and self.lineEdit_EndTime.text()
        ):
            CustomQtWidgets.do_message(
                self, text="Please input name, age, and time before save data."
            )
            return

        # CREATE DIRECTORY
        dir = str(
            QtWidgets.QFileDialog.getExistingDirectory(
                self, caption="Select Directory", directory=os.getcwd()
            )
        )
        if not dir:
            return
        name_dir = os.path.join(
            dir, f"{self.lineEdit_Name.text()}-{self.lineEdit_Age.text()}"
        )
        get_start_time = self.lineEdit_StartTime.text()
        get_end_time = self.lineEdit_EndTime.text()
        name_date_dir = os.path.join(
            name_dir, f"{get_start_time} {get_end_time} {self.sampling_rate}"
        )
        try:
            os.makedirs(name_date_dir)
        except:
            pass

        # SAVE MEDICAL INFORMATIONS
        with open(
            os.path.join(name_date_dir, "Medical_Information.csv"), "w", newline=""
        ) as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerows(
                [
                    ["Nicotine Levels", self.lineEdit_NicotineLevels.text()],
                    ["Months Of Smoking", self.lineEdit_MonthsOfSmoking.text()],
                    [
                        "Medical Background",
                        self.plainTextEdit_MedicalBackground.toPlainText(),
                    ],
                ]
            )

        # SAVE RAW DATA
        ecg_raw = pd.DataFrame(self.ecg_raw)
        ecg_raw.to_csv(
            os.path.join(name_date_dir, "ECG_Raw.csv"), index=False, header=False
        )

        # SAVE CLEANED DATA
        self.ECG_SIGNAL.ecg_clean.to_csv(
            os.path.join(name_date_dir, "ECG_Cleaned.csv"),
            index=False,
            header=False,
        )

        # SAVE FIGURES
        self.fig_raw.savefig(os.path.join(name_date_dir, "ECG_Raw_Plot.png"))
        self.fig_cleaned.savefig(os.path.join(name_date_dir, "ECG_Cleaned_Plot.png"))
        self.fig_delineate.savefig(
            os.path.join(name_date_dir, "ECG_Delineate_Plot.png")
        )

        # SAVE FEATURES
        with open(
            os.path.join(name_date_dir, "ECG_Findings_Features.txt"), "w"
        ) as file:
            file.write("Findings:\n" + self.plainTextEdit_Findings.toPlainText() + "\n")
            file.write("Heart Rate:" + self.lineEdit_HeartRate.text() + "\n")
            file.write("P Peak Ave:" + self.lineEdit_PPeakAve.text() + "\n")
            file.write("Q Peak Ave:" + self.lineEdit_QPeakAve.text() + "\n")
            file.write("QRS Comp Int:" + self.lineEdit_QRSCompInterval.text() + "\n")
            file.write("R-R Interval:" + self.lineEdit_RRInterval.text() + "\n")
            file.write("T Peak Ave:" + self.lineEdit_TPeakAve.text() + "\n")
            file.write("ST Interval:" + self.lineEdit_STInterval.text() + "\n")
            file.write("QS Interval:" + self.lineEdit_QSInterval.text() + "\n")

    def create_canvas(self, verticalLayout):
        # Instantiate FigureCanvas Start #
        figure = plt.figure()
        canvas = FigureCanvas(figure)
        toolbar = NavigationToolbar(canvas, self)
        verticalLayout.addWidget(toolbar)
        verticalLayout.addWidget(canvas)
        ax = figure.add_subplot(111)
        figure.tight_layout()
        canvas.draw()
        # Instantiate FigureCanvas End #
        return figure, canvas, ax


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
