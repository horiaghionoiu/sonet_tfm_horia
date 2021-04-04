"""
# ==============================================================================================
# ==============================================================================================
#
#
#                                    CLASS SonetPCPManagerQt
#
#
# ==============================================================================================
# ==============================================================================================
"""
# TODO Read PCP file .mat and convert it to dataframe.
# TODO Convert PCP file to dataframe.
# TODO Save it to .pkl file.

import numpy as np
import pandas as pd
from PySide2.QtWidgets import QDialog, QStatusBar, QFileDialog, QDialogButtonBox, QTreeWidgetItem
from scipy.io import loadmat

from src import database
from src import sonet_pcp_manager_ui  # The user interface, created with QtCreator.
from src.SonetUtils import SONET_MSG_TIMEOUT, SONET_PCP_DATA_DIR, TripType, reset_sc_filters_and_trajectories


class SonetPCPManagerQt(QDialog, sonet_pcp_manager_ui.Ui_sonet_pcp_manager):
    """
    Window in charge of managing the available PCP trajectories within the app,
    and also generates new ones, if desired.

    The matlab data is stored in .mat files, in matrix format.
    The app needs pcp data in table format. The tables are stored in .pkl files.
    """
    def __init__(self, *args, p_main_window=None, p_mat_eng=None):
        super(SonetPCPManagerQt, self).__init__(*args)
        self.setupUi(self)
        self.setModal(True)
        self.show()

        # Reference to the main window.
        self._p_main_window = p_main_window

        # Reference to matlab engine.
        self._p_matlab_engine = p_mat_eng

        # Some widgets settings.
        self.sonet_read_pcp_qtw.setHeaderLabels(['Selected .mat files',
                                                 'Total trajectories',
                                                 'Departure Dates',
                                                 'TOFs'])
        self.matrix_tw_outgoing_root_item = QTreeWidgetItem(self.sonet_read_pcp_qtw, ['Outgoing', '', '', ''])
        self.matrix_tw_incoming_root_item = QTreeWidgetItem(self.sonet_read_pcp_qtw, ['Incoming', '', '', ''])
        self.resize_matrix_tw_columns()

        self.sonet_working_pcp_qtw.setHeaderLabels(['Selected .pkl files',
                                                    'Rows',
                                                    'Columns'])
        self.table_tw_outgoing_root_item = QTreeWidgetItem(self.sonet_working_pcp_qtw, ['Outgoing', '', ''])
        self.table_tw_incoming_root_item = QTreeWidgetItem(self.sonet_working_pcp_qtw, ['Incoming', '', ''])
        self.resize_table_tw_columns()

        # Status bar,for messages to the user.
        self.status_bar = QStatusBar()
        self.status_bar.setBaseSize(580, 22)
        self.status_bar.setSizeGripEnabled(False)
        self.status_bar_HLayout.addWidget(self.status_bar)

        # Other members.
        self._pcp_mat_file_incoming = None
        self._pcp_mat_file_outgoing = None
        self._pcp_table_file_incoming = None
        self._pcp_table_file_outgoing = None

        # Signals and slots connect.
        self.sonet_read_pcp_outgoing_trajectories_matrix_qpb.clicked.connect(self.clicked_read_pcp_matrix_file_outgoing)
        self.sonet_read_pcp_incoming_trajectories_matrix_qpb.clicked.connect(self.clicked_read_pcp_matrix_file_incoming)
        self.sonet_dvt_limit_qcb.stateChanged.connect(self.clicked_dvt_limit_checkbox)
        self.sonet_convert_pcp_2_table_format_qpb.clicked.connect(self.clicked_convert_pcp_2_table_format)
        self.sonet_read_pcp_outgoing_trajectories_table_qpb.clicked.connect(self.clicked_read_pcp_table_file_outgoing)
        self.sonet_read_pcp_incoming_trajectories_table_qpb.clicked.connect(self.clicked_read_pcp_table_file_incoming)
        self.matlab_pcp_generator_pb.clicked.connect(self.clicked_matlab_pcp_generator)
        self.btn_OK = self.sonet_ok_cancel_qpb_group.button(QDialogButtonBox.Ok)
        self.btn_OK.clicked.connect(self.clicked_ok)
        self.btn_OK.clicked.connect(self.accept)

        self.btn_cancel = self.sonet_ok_cancel_qpb_group.button(QDialogButtonBox.Cancel)
        self.btn_cancel.clicked.connect(self.clicked_cancel)
        self.btn_cancel.clicked.connect(self.reject)

        # If there's a currently working pcp in the database, display it to the user.
        self.read_database_pcp()

        # sonet_log(SonetLogType.INFO, 'class_tal.method_tal')
        # self.status_bar.showMessage('tal.', SONET_MSG_TIMEOUT)

    def read_database_pcp(self):
        """
        If there's a currently working pcp in the database, display it to the user.

        """
        working_pcp_paths = database.get_working_pcp_paths()
        pkl_file_outgoing_path = working_pcp_paths[0]
        pkl_file_incoming_path = working_pcp_paths[1]
        # Fill the pkl files path line edit widgets.
        self.sonet__outgoing_trajectories_table_line_edit.setText(pkl_file_outgoing_path)
        self.sonet__incoming_trajectories_table_line_edit.setText(pkl_file_incoming_path)

        # Set the members pkl files & update the table tree view.
        if pkl_file_outgoing_path:
            self._pcp_table_file_outgoing = database.get_pcp_table(TripType.OUTGOING)
            self.update_table_tree_view(pkl_file_outgoing_path, p_trip='Outgoing')
        if pkl_file_incoming_path:
            self._pcp_table_file_incoming = database.get_pcp_table(TripType.INCOMING)
            self.update_table_tree_view(pkl_file_incoming_path, p_trip='Incoming')

    def clicked_ok(self):
        """
        Sets the current working pcp files (if any) & close the window.
        If we have changed the outgoing or incoming pkl files, all the currently set filters and trajectories
        are going to be reset.
        """

        pkl_file_path_outgoing = self.sonet__outgoing_trajectories_table_line_edit.text()
        pkl_file_path_incoming = self.sonet__incoming_trajectories_table_line_edit.text()
        has_changed_outgoing = database.set_working_pcp(TripType.OUTGOING, pkl_file_path_outgoing)
        has_changed_incoming = database.set_working_pcp(TripType.INCOMING, pkl_file_path_incoming)

        # Reset the filters and trajectories for ALL the s/c if necessary, AND inform to the user.
        if has_changed_outgoing or has_changed_incoming:
            reset_sc_filters_and_trajectories()
            self._p_main_window.statusbar.showMessage('Database has changed. Filter and trajectory reset  for ALL s/c',
                                                      SONET_MSG_TIMEOUT * 3)

    def clicked_cancel(self):
        """
        Abort all the operations & close the window.
        """
        pass

    def clicked_convert_pcp_2_table_format(self):
        """
        Converts matrix to tabular pcp data. .mat -> .pkl.
        - Reads all the current available .mat files.
        - Converts them to tabular format (pandas dataframes).
        - Saves the tables to pickle .pkl files.
        """
        # self.status_bar.showMessage('SonetPCPManagerQt.clicked_convert_pcp_2_table_format."Not implemented."',
        #                             SONET_MSG_TIMEOUT)

        # Check if user has limited the dvt value.
        dvt_widget = self.sonet_dvt_limit_qdoublespinbox
        if dvt_widget.isEnabled():
            dvt_limit_value = dvt_widget.value()
        else:
            dvt_limit_value = None

        # Convert mat obj to dataframe obj.
        result = []
        for mat_file in [self._pcp_mat_file_outgoing, self._pcp_mat_file_incoming]:
            if mat_file is None:
                result.append(None)
            else:
                result.append(self.convert_mat_2_dataframe(mat_file, dvt_limit_value))

        # Save the dataframes to pickle files.
        for df in result:
            df: pd.DataFrame
            if df is not None:
                file_path = df.attrs['file_name']
                file_name = file_path.split('/')[-2]
                self.status_bar.showMessage('Writing' + file_name + 'pkl file', 2*SONET_MSG_TIMEOUT)
                df.to_pickle(file_path)

        self.status_bar.showMessage('Pickle files written', 2*SONET_MSG_TIMEOUT)

        # Remove mat files and reset associated widgets.
        self.reset_matrix_widgets()

    def clicked_dvt_limit_checkbox(self):
        """
        Activate/deactivate the dvt limit line edit widget, depending of the check box state.
        """
        self.sonet_dvt_limit_qdoublespinbox.setEnabled(self.sonet_dvt_limit_qcb.isChecked())

    def clicked_matlab_pcp_generator(self):
        self._p_matlab_engine.PCPGenerator(nargout=0)

    def clicked_read_pcp_matrix_file_incoming(self):
        """
        Opens a select file dialog, the user has to select a valid matlab .mat file containing the pcp data.
        """
        file_path, filter_ = QFileDialog.getOpenFileName(parent=self, caption='Read PCP file (.mat)',
                                                        dir=SONET_PCP_DATA_DIR,
                                                        filter='*.mat')
        if file_path:
            self.sonet__incoming_trajectories_matrix_line_edit.setText(file_path)
        else:  # The user canceled the open file window.
            return
        self._pcp_mat_file_incoming = loadmat(file_path)
        self.status_bar.showMessage('PCP incoming .mat file read', SONET_MSG_TIMEOUT)

        file_name = file_path.split('/')[-2]
        my_mat_file_dep_dates = self._pcp_mat_file_incoming['departure_dates'].shape[1]
        my_mat_file_tofs = self._pcp_mat_file_incoming['tofs'].shape[1]
        my_mat_file_total_trajectories = my_mat_file_dep_dates * my_mat_file_tofs
        self.fill_matrix_QTreeWidget('Incoming', file_name,
                                     str(my_mat_file_total_trajectories),
                                     str(my_mat_file_dep_dates),
                                     str(my_mat_file_dep_dates))

    def clicked_read_pcp_matrix_file_outgoing(self):
        """
        Opens a select file dialog, the user has to select a valid matlab .mat file containing the pcp data.
        """

        # Read the .mat file.
        file_path, filter_ = QFileDialog.getOpenFileName(parent=self, caption='Read PCP file (.mat)',
                                                        dir=SONET_PCP_DATA_DIR,
                                                        filter='*.mat')
        if file_path:
            self.sonet__outgoing_trajectories_matrix_line_edit.setText(file_path)
        else:  # The user canceled the open file window.
            return

        self._pcp_mat_file_outgoing = loadmat(file_path)
        self.status_bar.showMessage('PCP outgoing .mat file read', SONET_MSG_TIMEOUT)

        file_name = file_path.split('/')[-2]
        my_mat_file_dep_dates = self._pcp_mat_file_outgoing['departure_dates'].shape[1]
        my_mat_file_tofs = self._pcp_mat_file_outgoing['tofs'].shape[1]
        my_mat_file_total_trajectories = my_mat_file_dep_dates * my_mat_file_tofs
        self.fill_matrix_QTreeWidget('Outgoing', file_name,
                                     str(my_mat_file_total_trajectories),
                                     str(my_mat_file_dep_dates),
                                     str(my_mat_file_dep_dates))

    def clicked_read_pcp_table_file_incoming(self):
        """
        Opens a select file dialog, the user has to select a valid pickle .pkl file containing the pcp data.
        """
        file_path, filter_ = QFileDialog.getOpenFileName(parent=self, caption='Read PCP file (.pkl)',
                                                        dir=SONET_PCP_DATA_DIR,
                                                        filter='*.pkl')
        if file_path:
            self.sonet__incoming_trajectories_table_line_edit.setText(file_path)
        else:  # The user canceled the open file window.
            return

        # Read the Python .pkl file.
        self._pcp_table_file_incoming = pd.read_pickle(file_path)
        self.status_bar.showMessage('PCP incoming .pkl file read', SONET_MSG_TIMEOUT)

        # Update the bottom tree view.
        self.update_table_tree_view(file_path, p_trip='Incoming')

    def update_table_tree_view(self, a_file_path, p_trip=''):
        a_file_name = a_file_path.split('/')[-2]

        if p_trip == 'Outgoing':
            my_pkl_file_rows = self._pcp_table_file_outgoing.shape[0]
            my_pkl_file_cols = self._pcp_table_file_outgoing.shape[1]
            self.fill_table_QTreeWidget('Outgoing', a_file_name,
                                        str(my_pkl_file_rows),
                                        str(my_pkl_file_cols))
        else:
            my_pkl_file_rows = self._pcp_table_file_incoming.shape[0]
            my_pkl_file_cols = self._pcp_table_file_incoming.shape[1]
            self.fill_table_QTreeWidget('Incoming', a_file_name,
                                        str(my_pkl_file_rows),
                                        str(my_pkl_file_cols))

    def clicked_read_pcp_table_file_outgoing(self):
        """
        Opens a select file dialog, the user has to select a valid pickle .pkl file containing the pcp data.
        """
        # Read the file name.
        file_path, filter_ = QFileDialog.getOpenFileName(parent=self, caption='Read PCP file (.pkl)',
                                                        dir=SONET_PCP_DATA_DIR,
                                                        filter='*.pkl')
        if file_path:
            self.sonet__outgoing_trajectories_table_line_edit.setText(file_path)
        else:  # The user canceled the open file window.
            return

        # Read the Python .pkl file.
        self._pcp_table_file_outgoing = pd.read_pickle(file_path)
        self.status_bar.showMessage('PCP outgoing .pkl file read', SONET_MSG_TIMEOUT)

        # Update the bottom tree view.
        self.update_table_tree_view(file_path, p_trip='Outgoing')

    def reset_matrix_widgets(self):
        self._pcp_mat_file_outgoing = None
        self._pcp_mat_file_incoming = None
        self.sonet_dvt_limit_qcb.setChecked(False)
        self.sonet__outgoing_trajectories_matrix_line_edit.clear()
        self.sonet__incoming_trajectories_matrix_line_edit.clear()
        self.matrix_tw_outgoing_root_item.takeChildren()
        self.matrix_tw_incoming_root_item.takeChildren()

    @staticmethod
    def convert_mat_2_dataframe(a_my_mat_file, a_dvt_limit=None) -> pd.DataFrame:
        """
        Converts the input mat file to tabular data, in the form of pandas dataframe obj.
        :param a_my_mat_file: input mat file.
        :param a_dvt_limit: the max dvt allowed for the output dataframe.
        """
        # TODO implement a_dvt_limit parameter.
        # Initialize the data structures.
        table_rows = a_my_mat_file['departure_dates'].shape[1]  # Table rows is N.
        table_size = table_rows ** 2  # Table size is N^2.

        rows = [i for i in range(table_size)]
        cols = ['DepDates', 'tof', 'c3d', 'c3a', 'dvd', 'dva', 'dvt', 'theta']
        data = np.zeros((table_size, len(cols)), dtype=np.double)

        # Do the conversion.
        get_value = SonetPCPManagerQt._fill_the_table_data
        row = 0
        for i in range(0, table_rows):  # For each departure date.
            # print(i)
            for j in range(0, table_rows):  # For each tof.
                # First, check max dvt, if greater than the cut-off value, discard this table row.
                dvt = get_value(a_my_mat_file, 'dvt', i, j)
                if dvt > a_dvt_limit:
                    continue

                # Independent vars are (1,table_rows) ndarrays.
                data[row, 0] = get_value(a_my_mat_file, 'departure_dates', 0, i)
                data[row, 1] = get_value(a_my_mat_file, 'tofs', 0, j)

                # Dependent vars are (table_rows,table_rows) ndarrays.
                data[row, 2] = get_value(a_my_mat_file, 'c3d', i, j)
                data[row, 3] = get_value(a_my_mat_file, 'c3a', i, j)
                data[row, 4] = get_value(a_my_mat_file, 'dvd', i, j)
                data[row, 5] = get_value(a_my_mat_file, 'dva', i, j)
                data[row, 6] = dvt
                data[row, 7] = get_value(a_my_mat_file, 'theta', i, j)

                row = row + 1

        # If the user has set a dvt limit, the returned dataframe my have less rows than the original expected.
        if a_dvt_limit:
            unfilled_rows = len(rows) - row
            df = pd.DataFrame(data[:-unfilled_rows,:], columns=cols, index=[i for i in range(row)])
        else:
            df = pd.DataFrame(data, columns=cols, index=rows)

        # Add 'ArrivDates' column and perform some conversions and columns reordering.
        df = SonetPCPManagerQt.post_process(df)

        # Add attributes to the dataframe.
        df.attrs['file_name'] = str(a_my_mat_file['fname'][0]) + '.pkl'
        df.attrs['memory_usage'] = int(df.memory_usage().sum() / 1e6)
        return df

    @staticmethod
    def _fill_the_table_data(a_my_mat_file, var='', row=0, col=0):
        return a_my_mat_file[var][row, col]

    def fill_matrix_QTreeWidget(self, a_file_type='', a_file_name='',
                                a_total_trajectories='0',
                                a_total_dep_dates='0',
                                a_total_tofs='0',
                                p_clean_qtw_before_cleaning=False):
        if p_clean_qtw_before_cleaning:
            self.sonet_read_pcp_qtw.clear()

        # root_node = self.sonet_read_pcp_qtw.invisibleRootItem()

        if a_file_type == 'Outgoing':
            self.matrix_tw_outgoing_root_item.takeChildren()
            the_new_item = QTreeWidgetItem(self.matrix_tw_outgoing_root_item, [a_file_name,
                                                                               a_total_trajectories,
                                                                               a_total_dep_dates,
                                                                               a_total_tofs])
        else:
            self.matrix_tw_incoming_root_item.takeChildren()
            the_new_item = QTreeWidgetItem(self.matrix_tw_incoming_root_item, [a_file_name,
                                                                               a_total_trajectories,
                                                                               a_total_dep_dates,
                                                                               a_total_tofs])
        self.matrix_tw_outgoing_root_item.setExpanded(True)
        self.matrix_tw_incoming_root_item.setExpanded(True)
        self.resize_matrix_tw_columns()

    def fill_table_QTreeWidget(self, a_file_type='', a_file_name='',
                               a_total_rows='0',
                               a_total_cols='0',
                               p_clean_qtw_before_cleaning=False):
        if p_clean_qtw_before_cleaning:
            self.sonet_working_pcp_qtw.clear()

        if a_file_type == 'Outgoing':
            self.table_tw_outgoing_root_item.takeChildren()
            the_new_item = QTreeWidgetItem(self.table_tw_outgoing_root_item, [a_file_name,
                                                                              a_total_rows,
                                                                              a_total_cols])
        else:
            self.table_tw_incoming_root_item.takeChildren()
            the_new_item = QTreeWidgetItem(self.table_tw_incoming_root_item, [a_file_name,
                                                                              a_total_rows,
                                                                              a_total_cols])
        self.table_tw_outgoing_root_item.setExpanded(True)
        self.table_tw_incoming_root_item.setExpanded(True)
        self.resize_table_tw_columns()

    def resize_matrix_tw_columns(self):
        self.sonet_read_pcp_qtw.resizeColumnToContents(0)
        self.sonet_read_pcp_qtw.resizeColumnToContents(1)
        self.sonet_read_pcp_qtw.resizeColumnToContents(2)
        self.sonet_read_pcp_qtw.resizeColumnToContents(3)

    def resize_table_tw_columns(self):
        self.sonet_working_pcp_qtw.resizeColumnToContents(0)
        self.sonet_working_pcp_qtw.resizeColumnToContents(1)
        self.sonet_working_pcp_qtw.resizeColumnToContents(2)

    @staticmethod
    def post_process(a_df: pd.DataFrame):
        """
        Given a input dataframe:
            - Creates a new column called 'ArrivDates', which is a lineal combination of 'DepDates' and 'tof'.
            - Converts 'DepDates' and 'ArrivDates' from JD2000 to JD, as QDate objects work with absolute dates.
            - Converts 'theta' from radians to sexagesimal degrees.
            - Reorder columns in a more convenient way.
        :param df: a Pandas DataFrame.
        """

        # Create 'ArrivDates' column.
        a_df['ArrivDates'] = a_df.DepDates + a_df.tof

        # Convert dates JD2000 to JD.
        JD2000 = 2451545.0  # Julian Day 2000, extracted from AstroLib matlab code.
        a_df['DepDates'] = (a_df.DepDates + JD2000)
        a_df['ArrivDates'] = (a_df.ArrivDates + JD2000)

        # Convert theta rad to º.
        a_df.theta = a_df.theta * 180 / np.pi

        # Reorder columns.
        reordered_cols = ['DepDates', 'ArrivDates', 'tof', 'theta', 'dvt', 'dvd', 'dva', 'c3d', 'c3a']
        return a_df.reindex(columns=reordered_cols)