import sys

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtWidgets, uic

from Forecasting import Forecasting
from Tools import Tools


class DoThreading(QtCore.QThread):
    def __init__(self, _func, _finished_func=None):
        QtCore.QThread.__init__(self)
        self.func = _func
        self.daemon = True
        self.finished_func = _finished_func
        if self.finished_func is not None:
            self.finished.connect(_finished_func)

    def __del__(self):
        self.wait()

    def run(self):
        self.func()


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(
            self,
            "Quit",
            "Are you sure want to quit?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if close == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


class MainWindow(Window):
    def __init__(self, ui):
        super().__init__()
        uic.loadUi(ui, self)
        self.center()
        self.show()
        self.filename = None
        self.forecasting = None

        # Event Handling
        self.pushButton_file_input.clicked.connect(self.pushButton_file_input_clicked)
        self.pushButton_submit.clicked.connect(self.pushButton_submit_clicked)
        self.pushButton_forecast.clicked.connect(self.pushButton_forecast_clicked)
        self.pushButton_save_file.clicked.connect(self.pushButton_save_file_clicked)
        self.pushButton_delete.clicked.connect(
            lambda: self.remove_last_row(self.tableWidget_data)
        )

    def do_forecast(self, periods):

        # Waiting cursor
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        # Forecasting using NeuralProphet
        (
            m_Enrollees,
            df_Predict,
            m_Enrollees_Future_df_Predict,
        ) = self.forecasting.forecast(
            epochs=1000,
            periods=int(periods),
        )

        # convert to np.int64
        for column in df_Predict.columns:
            if df_Predict.loc[:, column].dtype == np.float64:
                df_Predict.loc[:, column] = (
                    df_Predict.loc[:, column].apply(np.int64).apply(np.abs)
                )

        # convert to np.int64
        for column in m_Enrollees_Future_df_Predict.columns:
            if m_Enrollees_Future_df_Predict.loc[:, column].dtype == np.float64:
                m_Enrollees_Future_df_Predict.loc[:, column] = (
                    m_Enrollees_Future_df_Predict.loc[:, column]
                    .apply(np.int64)
                    .apply(np.abs)
                )

        # show data in tablewidget_predicted
        df_copy = m_Enrollees_Future_df_Predict.copy(deep=True)

        df_copy["ds"] = df_copy["ds"].dt.strftime("%Y-%m-%d")

        self.show_data(
            self.tableWidget_predicted,
            df_copy.loc[
                :,
                [
                    "ds",
                    "yhat1",
                    "future_regressor_Graduates",
                    "future_regressor_Passers",
                ],
            ].values,
        )

        # Remove waiting cursor
        QtWidgets.QApplication.restoreOverrideCursor()

        # PLOT Data and Forecast using matplotlib
        m_Enrollees.plot(df_Predict, xlabel="Date", ylabel="Enrollees")
        plt.title("Data")
        m_Enrollees.plot_components(df_Predict)

        m_Enrollees.plot(
            m_Enrollees_Future_df_Predict, xlabel="Date", ylabel="Enrollees"
        )
        plt.title("Forecast")
        m_Enrollees.plot_components(m_Enrollees_Future_df_Predict)

        concat_df = pd.concat(
            [
                df_Predict,
                m_Enrollees_Future_df_Predict,
            ]
        )

        m_Enrollees.plot(concat_df)
        plt.title("Data + Forecast")
        m_Enrollees.plot_components(concat_df)

        plt.show()

    def pushButton_save_file_clicked(self):

        # convert tablewidget data to pandas dataframe
        df_tableWidget_data = pd.DataFrame(
            self.get_rows(self.tableWidget_data),
            columns=self.forecasting.df.columns,
        )

        # convert tablewidget data to pandas dataframe
        df_tableWidget_predicted = pd.DataFrame(
            self.get_rows(self.tableWidget_predicted),
            columns=self.forecasting.df.columns,
        )

        # save file
        filename = Tools.do_save_filename(self, filter="csv file (*.csv)")

        # check if user inputted a filename
        if filename != "":
            pd.concat([df_tableWidget_data, df_tableWidget_predicted,]).to_csv(
                filename, index=False
            )  # concat 2 dataframes then save as csv without index

    def pushButton_forecast_clicked(self):
        # periods used for neuralprophet
        periods = self.lineEdit_periods.text()

        if self.forecasting:  # check if user input a file before forcasting
            if not periods.isdigit():  # check if period is a digit
                Tools.do_message(self, text="Input a valid period.")
                return

            # get tableWidget_data then convert to pandas dataframe
            self.forecasting.df = pd.DataFrame(
                self.get_rows(self.tableWidget_data),
                columns=self.forecasting.df.columns,
            )

            # use threading in forecasting to avoid not responding window
            DoThreading(lambda: self.do_forecast(periods)).run()

        else:
            Tools.do_message(self, text="Please input a file first.")

    def pushButton_submit_clicked(self):
        # get items separated by comma
        items = self.lineEdit_input_data.text().split(",")

        if self.forecasting:
            if len(items) != len(
                self.forecasting.df.columns
            ):  # check if total items are same with column
                Tools.do_message(
                    self,
                    text=f"Too much data. Only requires {len(self.forecasting.df.columns)}.",
                )
                return
            self.add_row(self.tableWidget_data, items)
        else:
            Tools.do_message(self, text="Please input a file first.")

    def pushButton_file_input_clicked(self):
        filename = Tools.do_get_filename(
            self, "Open csv file", filter="csv file (*.csv)"
        )

        if filename != "":  # check if user inputted a filename
            self.filename = filename
            self.forecasting = Forecasting(self.filename)
            df_copy = self.forecasting.df.copy(deep=True)
            df_copy["Date"] = df_copy["Date"].dt.strftime("%Y-%m-%d")
            self.show_data(self.tableWidget_data, df_copy.values)

    # QTableWdiget manipulation functions
    def add_row(self, tableWidget, items):
        row = tableWidget.rowCount()
        tableWidget.setRowCount(row + 1)

        col = 0
        for y in items:
            cell = QtWidgets.QTableWidgetItem(str(y))
            tableWidget.setItem(row, col, cell)
            col += 1

    def get_rows(self, tableWidget):
        total_row = tableWidget.rowCount()
        total_columns = tableWidget.columnCount()

        row_items = []
        for row in range(0, total_row):
            column_items = []
            for column in range(0, total_columns):
                column_items.append(tableWidget.item(row, column).text())
            row_items.append(column_items)

        return row_items

    def remove_last_row(self, tableWidget):
        total_row = tableWidget.rowCount()
        tableWidget.removeRow(total_row - 1)

    def show_data(self, tableWidget, items):
        total_row = tableWidget.rowCount()

        if total_row > 0:
            for _ in range(0, total_row):
                self.remove_last_row(tableWidget)
            total_row = 0

        for item in items:
            self.add_row(tableWidget, item)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow("MainWindow.ui")
    app.exec_()
