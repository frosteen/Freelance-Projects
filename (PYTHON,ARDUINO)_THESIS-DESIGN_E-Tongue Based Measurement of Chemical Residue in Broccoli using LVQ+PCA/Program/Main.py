import os
import pickle
import sys
import warnings

warnings.filterwarnings("ignore", message=r"Passing", category=FutureWarning)

import matplotlib.pyplot as plt
import pandas as pd
import serial
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtCore, QtWidgets, uic

import Utils.ReadWriteCSV as RWCSV
from Utils.CustomQtWidgets import CustomQtWidgets
from Utils.LVQ import Process_LVQ
from Utils.PCA import Process_PCA
from Utils.QTableWidgetUtils import QTableWidgetUtils
from Utils.QTThreading import DoThreading


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

    def center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def Gather_TestData(self, filename):
        with open("Training/SavedObjects/COMPORT.txt", "r") as file:
            COMPORT = file.readline()
        ser = serial.Serial(port=COMPORT, baudrate=9600)

        try:
            # STABILIZING
            self.statusbar.showMessage("Stabilizing... Please wait.")
            for _ in range(10):
                incoming = ser.readline()

            # START
            self.statusbar.showMessage("Gathering 10 samples... Please wait to finish.")
            for _ in range(10):
                incoming = ser.readline()
                incoming = incoming.decode()
                incoming = incoming.strip()
                if incoming:
                    final_data = incoming + ",UNKNOWN"
                    PH, N, P, K, CLASS = final_data.split(",")
                    RWCSV.write_csv_dict(
                        filename,
                        {
                            "pH": PH,
                            "N": N,
                            "P": P,
                            "K": K,
                            "Class": CLASS,
                        },
                    )
                    self.statusbar.showMessage(final_data)
        except Exception as e:
            print("!Error: " + e)
        finally:
            print("Done.")
            ser.close()

    def Generate_Measurement(self, filename):
        df_test = pd.read_csv(filename)
        df_test = df_test.drop_duplicates().reset_index(drop=True)
        df_test.insert(0, "Sample Name", os.path.basename(filename))
        mean_df_test = df_test.groupby("Sample Name").mean().round(4).reset_index()
        QTableWidgetUtils.fill_table(self.tableWidget, mean_df_test.values)

        return mean_df_test

    def Graph_2DPCA_PYQT(self, df, title):
        # Instantiate FigureCanvas Start #
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)
        # Instantiate FigureCanvas End #

        # Plot Start #
        targets = df.iloc[:, (len(df.columns) - 1)].unique()
        for target in targets:
            indicesToKeep = df.iloc[:, len(df.columns) - 1] == target
            self.ax.scatter(
                df.loc[indicesToKeep, df.columns[0]],
                df.loc[indicesToKeep, df.columns[1]],
                s=50,
            )
        self.ax.set_xlabel(df.columns[0], fontsize=15)
        self.ax.set_ylabel(df.columns[1], fontsize=15)
        self.ax.set_title(f"PCA {title}", fontsize=20)
        self.ax.legend(targets, loc="center left", bbox_to_anchor=(1, 0.5))
        self.ax.grid()
        self.figure.tight_layout()
        self.canvas.draw()
        # Plot End #

    def Process_PCA_LVQ_Test(self, filename):
        # Read Test Data
        df_test = pd.read_csv(filename)
        df_test_drop_ph = df_test.drop("pH", axis=1)
        df_test_drop_ph = df_test_drop_ph.drop_duplicates().reset_index(drop=True)

        # PCA Test Data
        df_pca_test = Process_PCA(
            df_test_drop_ph.iloc[:, :-1],
            df_test_drop_ph.iloc[:, -1],
            normalizer_joblib_path="Training/SavedObjects/Normalizer.joblib",
            pca_joblib_path="Training/SavedObjects/PCA.joblib",
        )

        # Predicting
        with open("Training/SavedObjects/Classes.pickle", "rb") as f:
            targets = pickle.load(f)
        inv_targets = {v: k for k, v in targets.items()}
        predict_classes = Process_LVQ(
            df_pca_test.iloc[:, :-1], lvq_joblib_path="Training/SavedObjects/LVQ.joblib"
        )
        df_pca_test["Class"] = predict_classes
        df_pca_test["Class"] = df_pca_test["Class"].map(inv_targets)

        # Final Predicted Test DF
        df_test["Class"] = df_pca_test["Class"]

        # Graph 2DPCA
        self.Graph_2DPCA_PYQT(df_pca_test, os.path.basename(filename))

        return df_test

    def Generate_Output(self, df_output, filename):
        df_output = df_output.drop("pH", axis=1)
        # df_output = df_output[df_output["Class"] != "NONE"]
        mean_df_output = df_output.groupby("Class").mean().reset_index()
        sample_mass = 0.010  # kg
        pesticide_amount = 1  # ml
        mean_df_output[["N", "P", "K"]] = (
            mean_df_output[["N", "P", "K"]] * 0.001 * sample_mass / pesticide_amount
        ) * 100
        mean_df_output = mean_df_output.round(4)
        mean_df_output.insert(0, "Sample Name", os.path.basename(filename))
        final_df = mean_df_output[["Sample Name", "N", "P", "K", "Class"]]

        # populate table
        QTableWidgetUtils.fill_table(self.tableWidget, final_df.values)

        return final_df


class BootScreen(Window):
    def __init__(self):
        super().__init__()
        uic.loadUi("WindowUI/BootScreen.ui", self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton_Exit.clicked.connect(self.close)
        self.pushButton_Minimize.clicked.connect(self.showMinimized)
        self.pushButton_Start.clicked.connect(self.show_MainMenu)

    def show_MainMenu(self):
        self.w = MainMenu()
        self.close()


class MainMenu(Window):
    def __init__(self):
        super().__init__()
        uic.loadUi("WindowUI/MainMenu.ui", self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton_Exit.clicked.connect(self.close)
        self.pushButton_Minimize.clicked.connect(self.showMinimized)
        self.pushButton_NewTest.clicked.connect(self.show_NewTest)
        self.pushButton_LoadTestFiles.clicked.connect(self.do_LoadTestFiles)

    def show_NewTest(self):
        self.w = NewTest()
        self.close()

    def show_Measurement_Window(self, filename):
        self.w = Measurement(filename)
        self.close()

    def do_LoadTestFiles(self):
        filename = CustomQtWidgets.do_get_filename(
            self,
            caption="Load Test File",
            directory="TestFiles",
            filter="CSV Files (*.csv)",
        )
        if filename != "":
            self.show_Measurement_Window(filename)


class NewTest(Window):
    def __init__(self):
        super().__init__()
        uic.loadUi("WindowUI/NewTest.ui", self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton_Exit.clicked.connect(self.close)
        self.pushButton_Minimize.clicked.connect(self.showMinimized)
        self.pushButton_Return.clicked.connect(self.show_MainMenu)
        self.pushButton_StartTesting.clicked.connect(self.do_testing)
        self.pushButton_Rename.clicked.connect(self.do_rename)

        self.comboBox_Files_List()

    def show_MainMenu(self):
        self.w = MainMenu()
        self.close()

    def show_Measurement_Window(self, filename):
        self.w = Measurement(filename)
        self.close()

    def do_testing(self):
        if self.lineEdit_Filename.text() != "":
            self.pushButton_Return.setEnabled(False)
            self.pushButton_StartTesting.setEnabled(False)
            self.pushButton_Rename.setEnabled(False)
            self.lineEdit_Filename.setEnabled(False)
            self.comboBox_Files.setEnabled(False)
            filename = os.path.join("TestFiles", f"{self.lineEdit_Filename.text()}.csv")
            self.th = DoThreading(
                lambda: self.Gather_TestData(filename),
                lambda: self.show_Measurement_Window(filename),
            )
            self.th.start()

    def do_rename(self):
        if (
            self.comboBox_Files.currentText() != ""
            and self.lineEdit_Filename.text() != ""
        ):
            new_name = os.path.join("TestFiles", f"{self.lineEdit_Filename.text()}.csv")
            os.rename(
                os.path.join("TestFiles", self.comboBox_Files.currentText()),
                new_name,
            )
            self.comboBox_Files.clear()
            self.comboBox_Files_List()

    def comboBox_Files_List(self):
        for file in os.listdir("TestFiles"):
            if file.endswith(".csv"):
                self.comboBox_Files.addItem(file)


class Measurement(Window):
    def __init__(self, filename):
        super().__init__()
        uic.loadUi("WindowUI/Measurement.ui", self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton_Exit.clicked.connect(self.close)
        self.pushButton_Minimize.clicked.connect(self.showMinimized)
        self.pushButton_Return.clicked.connect(self.show_MainMenu)
        self.pushButton_ShowPCA.clicked.connect(self.show_PCA_Window)
        self.pushButton_SaveTestResult.clicked.connect(self.do_save_test_result)

        self.filename = filename
        self.df = self.Generate_Measurement(filename)

    def show_MainMenu(self):
        self.w = MainMenu()
        self.close()

    def show_PCA_Window(self):
        self.w = PCA_Window(self.filename)
        self.close()

    def do_save_test_result(self):
        filename = CustomQtWidgets.do_save_filename(
            self, "Save Test Result", "MeasurementFiles", "All CSV (*.csv)"
        )
        if filename != "":
            self.df.to_csv(filename, index=False, encoding="utf-8")


class PCA_Window(Window):
    def __init__(self, filename):
        super().__init__()
        uic.loadUi("WindowUI/PCA_Window.ui", self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton_Exit.clicked.connect(self.close)
        self.pushButton_Minimize.clicked.connect(self.showMinimized)
        self.pushButton_Return.clicked.connect(self.show_MainMenu)
        self.pushButton_ShowOutput.clicked.connect(self.show_Output_Window)
        self.pushButton_SaveTestResult.clicked.connect(self.do_save_test_result)

        self.filename = filename
        self.df = self.Process_PCA_LVQ_Test(filename)

    def show_MainMenu(self):
        self.w = MainMenu()
        self.close()

    def show_Output_Window(self):
        self.w = Output_Window(self.df, self.filename)
        self.close()

    def do_save_test_result(self):
        filename = CustomQtWidgets.do_save_filename(
            self, "Save Test Result", "PCAFiles", "All CSV (*.csv)"
        )
        if filename != "":
            self.df.to_csv(filename, index=False, encoding="utf-8")


class Output_Window(Window):
    def __init__(self, df_test, filename):
        super().__init__()
        uic.loadUi("WindowUI/Output_Window.ui", self)
        self.setFixedSize(self.size())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()
        self.pushButton_Exit.clicked.connect(self.close)
        self.pushButton_Minimize.clicked.connect(self.showMinimized)
        self.pushButton_Return.clicked.connect(self.show_MainMenu)
        self.pushButton_SaveTestResult.clicked.connect(self.do_save_test_result)

        self.output_df = self.Generate_Output(df_test, filename)

    def show_MainMenu(self):
        self.w = MainMenu()
        self.close()

    def do_save_test_result(self):
        self.output_df.rename(
            columns={"Class": "Pesticide Classifcation"}, inplace=True
        )
        filename = CustomQtWidgets.do_save_filename(
            self, "Save Test Result", "OutputFiles", "All CSV (*.csv)"
        )
        if filename != "":
            self.output_df.to_csv(filename, index=False, encoding="utf-8")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = BootScreen()
    app.exec_()
