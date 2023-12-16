import os
import sys

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets, uic

from Device import Device, Reader, Tag
from Formulas import distance_formula, rssi_to_distance, trilateration_3d
from KalmanFilter import KalmanFilter

max_xlimit = 3.6  # in meters
max_ylimit = 2.0

marker_size_readers = 35
marker_size_tags = 10

# KalmanFilter R and Q parameters
# R and Q are same to all readers
KalmanFilter_R = 0.1
KalmanFilter_Q = 20


readers = (
    Reader(
        "Reader1",
        "Reader1",
        (0, 2.0, 1.5),
        color="orange",
        A=-31,
        n=2.54,
    ),
    Reader(
        "Reader2",
        "Reader2",
        (0, 0, 1.5),
        color="green",
        A=-34,
        n=2.65,
    ),
    Reader(
        "Reader3",
        "Reader3",
        (3.6, 2.0, 1.5),
        color="violet",
        A=-33,
        n=2.00,
    ),
)

tags = (
    Tag(
        "Tag1",
        "Tag1",
        (0, 0, 0),
        color="blue",
    ),
    Tag(
        "Tag2",
        "Tag2",
        (0, 0, 0),
        color="yellow",
    ),
    # Tag(
    #     "Tag3",
    #     "Tag3",
    #     (0, 0, 0),
    #     color="red",
    # ),
)


# Multithreading
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


# Main
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.getcwd() + "/Thesis.ui", self)
        self.setFixedSize(self.size())
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.show()

        # connections
        self.toolButton.clicked.connect(self.tool_button_clicked)

        # public variables
        self.chosen_tag_index = None

        # Instantiate FigureCanvas
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.verticalLayout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)
        self.figure.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)

        self.plot()

        # Bottom legends #
        box = self.ax.get_position()

        self.ax.set_position(
            [box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9]
        )

        self.figure.legend(
            loc="upper center",
            markerscale=0.25,
            bbox_to_anchor=(0.5, 0.10),
            ncol=Device.total,
        )
        ####################

        # run in background
        self.thread_locate_tags = DoThreading(self.locate_tags)
        self.thread_locate_tags.start()

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(
            self,
            "QUIT",
            "Are you sure want to quit?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if close == QtWidgets.QMessageBox.Yes:
            del self.thread_locate_tags
            event.accept()
        else:
            event.ignore()

    def locate_tags(self):
        while 1:
            f = open(os.getcwd() + "/Data.txt", "r")
            line = f.readline()

            while line:
                reader_address, tag_address, rssi = line.split(",")

                line = f.readline()

                for reader in readers:
                    for tag in tags:
                        if (
                            reader_address == reader.address
                            and tag_address == tag.address
                        ):
                            if (
                                tag.linked_readers_kalman_filter.get(reader.name)
                                is None
                            ):
                                tag.linked_readers_kalman_filter[
                                    reader.name
                                ] = KalmanFilter(KalmanFilter_R, KalmanFilter_Q)
                            tag.linked_readers_filtered_rssi[
                                reader.name
                            ] = tag.linked_readers_kalman_filter[reader.name].filter(
                                float(rssi)
                            )

                            tag.linked_readers_rssi[reader.name] = float(rssi)

                for tag in tags:
                    if len(tag.linked_readers_rssi) == len(readers):
                        for reader in readers:
                            filtered_rssi = tag.linked_readers_filtered_rssi[
                                reader.name
                            ]
                            rssi = tag.linked_readers_rssi[reader.name]
                            distance = rssi_to_distance(
                                filtered_rssi, reader.A, reader.n
                            )
                            # distance = tag.linked_readers_rssi[reader.name]

                            tag.linked_readers_rssi[reader.name] = distance

                        readers1, readers2, readers3 = (
                            readers[0],
                            readers[1],
                            readers[2],
                        )

                        x, y, z = trilateration_3d(
                            *readers1.position,
                            tag.linked_readers_rssi[readers1.name],
                            *readers2.position,
                            tag.linked_readers_rssi[readers2.name],
                            *readers3.position,
                            tag.linked_readers_rssi[readers3.name]
                        )

                        tag.position = (float(abs(x)), float(abs(y)), z)

                        self.plot()

                        tag.reset_linked_readers_rssi()
                        tag.reset_linked_readers_filtered_rssi()

                for tag1 in tags:
                    for tag2 in tags:
                        if tag1.name != tag2.name:
                            x1, y1 = tag1.position[0:2]
                            x2, y2 = tag2.position[0:2]
                            tag_distance = distance_formula(x1, y1, x2, y2)
                            tag1.linked_tags_distance[tag2.name] = round(
                                float(tag_distance), 2
                            )

                if self.chosen_tag_index is not None:
                    self.update_tag_labels()

    def plot(self):
        # Clear plot
        self.ax.clear()

        # gridlines
        self.ax.grid()

        # Set x and y limit
        self.ax.set_xlim([0, max_xlimit])
        self.ax.set_ylim([0, max_ylimit])

        # Plot readers
        for reader in readers:
            self.ax.plot(
                *reader.position[0:2],
                color=reader.color,
                marker="s",
                markersize=marker_size_readers,
                linestyle="None",
                label=reader.name
            )

        # Plot all tags
        for tag in tags:
            self.ax.plot(
                *tag.position[0:2],
                color=tag.color,
                marker="o",
                markersize=marker_size_tags,
                linestyle="None",
                label=tag.name
            )

        # draw plot
        self.canvas.draw()

    def update_tag_labels(self):
        if self.chosen_tag_index is not None:
            x, y, z = tags[self.chosen_tag_index].position
            self.label.setText("X: " + str(round(x, 4)))
            self.label_2.setText("Y: " + str(round(y, 4)))

            while self.tableWidget.rowCount() > 0:
                self.tableWidget.removeRow(0)

            linked_tags_distance = tags[self.chosen_tag_index].linked_tags_distance

            for linked_tag_distance in linked_tags_distance:
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)

                self.tableWidget.setItem(
                    row_position, 0, QtWidgets.QTableWidgetItem(linked_tag_distance)
                )
                self.tableWidget.setItem(
                    row_position,
                    1,
                    QtWidgets.QTableWidgetItem(
                        str(linked_tags_distance[linked_tag_distance])
                    ),
                )

    def tool_button_clicked(self):
        self.chosen_tag, self.chosen_tag_index = self.do_get_item(
            [tag.name for tag in tags], "Choose a TAG:", "TAG"
        )
        if self.chosen_tag is not None and self.chosen_tag_index is not None:
            self.label_3.setText("Coordinates of: " + self.chosen_tag)
            self.update_tag_labels()

    # Tools
    def center(self):
        frame_gm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(
            QtWidgets.QApplication.desktop().cursor().pos()
        )
        center_point = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def do_message(self, text, title="Info"):
        msg = QtWidgets.QMessageBox(self)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.show()
        return msg

    def do_get_question(self, text, title="Question"):
        return QtWidgets.QMessageBox.question(
            self,
            title,
            text,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )

    def do_get_item(self, items, label, title="Input"):
        inputted, ok_pressed = QtWidgets.QInputDialog.getItem(
            self, title, label, items, 0, False
        )
        index = items.index(inputted)
        if inputted and ok_pressed:
            return inputted, index
        else:
            return None, None


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    app.exec_()
