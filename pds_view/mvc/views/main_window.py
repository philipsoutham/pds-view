import os

# os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.qpa.*=false"
os.environ["QT_LOGGING_RULES"] = "qt.qpa.*=false"
import typing
from pathlib import Path

import matplotlib as mpl
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from pds4_tools.reader import pds4_read
from pds4_tools.reader.array_objects import ArrayStructure
from pds4_tools.reader.data import PDS_ndarray
from pds4_tools.reader.header_objects import HeaderStructure
from PyQt5 import uic
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QWidget

from ..models import SummaryTableModel, TableModel

_IMAGE_TYPES = (
    "Array_2D_Image",
    "Array_3D_Image",
    "Array_3D_Spectrum",
    "Array_2D_Map",
)


def _load_summary_df(
    structures: list[typing.Union[HeaderStructure, ArrayStructure]]
) -> pd.DataFrame:
    return pd.DataFrame(
        data=[
            (
                s.id,
                s.type,
                (
                    "x".join(map(str, s.data.shape))
                    if len(s.data.shape) > 1
                    else f"{len(s.fields)}x{len(s.data)}"
                )
                if isinstance(s.data, PDS_ndarray)
                else "---",
            )
            for s in structures
        ],
        columns=["Name", "Type", "Dimension"],
    )


class MainWindow(QMainWindow):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        """See ui/main.ui for inherited variable names"""
        super().__init__(parent=parent)
        uic.loadUi(Path(__file__).parent.joinpath("ui", "main.ui"), self)
        self._is_3d = False
        self._is_rgb = False

        self.current_obj_name.setText("Open a file with 'Ctrl-O'")
        self.current_summary_fpath.setText("Open a file with 'Ctrl-O'")
        self._configure_tabs()

    def _control_tab_family(self, idx: int, enabled: bool):
        self.tab_display.setTabEnabled(idx, enabled)
        self.tab_display.setTabVisible(idx, enabled)

    def _configure_tabs(self):
        self._control_tab_family(1, self._is_3d)
        self._control_tab_family(3, self._is_rgb)
        self._control_tab_family(4, False)
        self._control_tab_family(2, False)

        self.tab_display.setCurrentWidget(
            self.tab_display.widget(self.tab_display.count() - 1)
        )

    def _select_pds_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Select PDS file...",
            "",
            "PDS Files (*lbl *.xml);;PDS3 Files (*.lbl);;PDS4 Files (*.xml)",
            options=options,
        )

        if fileName:
            self._load_file(fileName)

    def _load_file(self, fname):
        self.structure_list = pds4_read(
            fname, lazy_load=True, decode_strings=True, quiet=True
        )
        df = _load_summary_df(self.structure_list.structures)
        tm = SummaryTableModel(df)
        self.summary_table_view.setModel(tm)
        self.summary_table_view.resizeColumnsToContents()
        self.current_summary_fpath.setText(fname)
        self.action_save_image_as.setEnabled(False)
        self.action_save_table_as.setEnabled(False)
        self.current_obj_name.setText("")
        self._configure_tabs()

    def _quit(self):
        self.close()

    def _summary_table_row_clicked(self, idx: QModelIndex):
        m = idx.model()
        d = m.index(idx.row(), 0).data()
        self.current_obj_name.setText(d)
        tbl_data = next(s.data for s in self.structure_list.structures if s.id == d)
        df = pd.DataFrame(
            data=tbl_data,
        )
        tm = TableModel(df)
        self.data_table_view.setModel(tm)
        self._control_tab_family(2, True)
        # self.data_table_view.resizeColumnsToContents()
        self.action_save_table_as.setEnabled(True)

        # if w := self.image_grid_layout.itemAt(0):
        if w := self.image_view_layout.itemAt(0):
            # self.image_grid_layout.removeWidget(w.widget())
            self.image_view_layout.removeWidget(w.widget())

        if m.index(idx.row(), 1).data() in _IMAGE_TYPES:
            figure = Figure((40.0, 32.0), dpi=72.0)
            imageWidget = FigureCanvas(figure)

            axes = figure.add_subplot(111)
            axes.autoscale_view(True, True, True)
            axes.imshow(
                df.to_numpy(),
                origin="lower",
                interpolation="none",
                norm=mpl.colors.Normalize(clip=False),
                aspect="equal",
                cmap="gray",
            )
            self.image_view_layout.addWidget(imageWidget)
            # self.image_grid_layout.addWidget(imageWidget)

            self._control_tab_family(4, True)
            self.tab_display.setCurrentWidget(self.tab_display.widget(4))
            self.action_save_image_as.setEnabled(True)
        else:
            self._control_tab_family(4, False)
            self.tab_display.setCurrentWidget(self.tab_display.widget(2))
            self.action_save_image_as.setEnabled(False)

    def _export_csv(self):
        fname, _ = QFileDialog.getSaveFileName(
            self, "Save CSV file...", "/tmp", "CSV Files (*.csv)"
        )
        self.data_table_view.model().to_csv(fname)

    def _export_image(self, *args):
        print(f"export image {args}")

    def _tab_changed(self, idx: int):
        print(f"here in tab {idx}")


if __name__ == "__main__":
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    my = MainWindow()
    my.show()
    sys.exit(app.exec())
