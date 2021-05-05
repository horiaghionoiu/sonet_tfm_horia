"""
SonetMainWindow class.

Author: Horia Ghionoiu Martínez.
Project: Sonet Mars Mission Architecture Planner
Started:    22th June 2020
Code submitted: 22th June 2021
Project defense: 22th July 2021
"""

import datetime
import sys

# Matlab environment
import matlab.engine
# Some Python modules.
import pandas as pd
from PySide2.QtCore import QAbstractListModel, QAbstractTableModel, QModelIndex, Qt, QDate
# SONet imports.
# From module X import class Y.
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QMainWindow, QApplication, QMessageBox
from scipy.io import savemat

from src import database
from src import sonet_main_window_ui
from src.SonetPCPFilterQt import SonetPCPFilterQt
from src.SonetPCPManagerQt import SonetPCPManagerQt
from src.SonetSpacecraft import SonetSpacecraft
from src.SonetTrajectoryFilter import SonetTrajectoryFilter
from src.SonetUtils import TripType, SonetLogType, sonet_log, popup_msg, SONET_MSG_TIMEOUT, SONET_DIR, SONET_DATA_DIR

matlab_engine = matlab.engine.start_matlab()
s = matlab_engine.genpath(SONET_DIR)
matlab_engine.addpath(s, nargout=0)
# QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)  # To avoid AA_ShareOpenGLContexts warning in QtCreator.

# ==============================================================================================
# ==============================================================================================
#
#                                    CLASS SonetMainWindowQt
#                            (also classes ListModel & TableModel)
#
# ==============================================================================================
# ==============================================================================================


def force_table_view_update():
    """
    Force update of the selected table view. Merder method to be reviewed.
    It simlates the user clicking over the current selected tab (Earth-Mars or Mars-Earth).
    """
    index = get_main_window().sonet_pcp_tabs_qtw.currentIndex()
    get_main_window().sonet_pcp_tabs_qtw.currentChanged.emit(index)

def get_current_sc() -> SonetSpacecraft:
    """
    Get the current selected s/c in the main window's list. Returns None object if no selection
    is made or if the list is empty.

    @return:
    """
    # Get some stuff.
    qlv_row = main_window.sonet_mission_tree_qlv.currentIndex().row()
    the_sc_list = database.get_spacecrafts_list()

    # If there is at least a s/c.
    if the_sc_list:
        # If a s/c is selected.
        if qlv_row != -1:
            the_sc = the_sc_list[qlv_row]
            return database.get_spacecraft(the_sc)
        else:
            return None
    else:
        return None

def get_main_window():
    """
    Getter method.
    """
    return main_window

def get_pcp_filter_window():
    return get_main_window()._p_pcp_filter_window

class SonetMainWindow(QMainWindow, sonet_main_window_ui.Ui_main_window):
    """
    The main application window (QMainWindow).
    """

    def __init__(self, *args, **kwargs):
        super(SonetMainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Access to SonetPCPFilterQt window.
        self._p_pcp_filter_window = None

        # Widgets settings.
        self.menubar.setNativeMenuBar(False)  # I'd problems with MacOSX native menubar, the menus didn't appear
        self.sonet_pcp_tabs_qtw.setCurrentIndex(0)
        self.sonet_spacecraft_type_qcmb.setCurrentIndex(1)  # Select cargo payload, by default.

        # Table models, it should be declared prior to list model
        self._table_model_outgoing = TableModel(TripType.OUTGOING)
        self._table_model_incoming = TableModel(TripType.INCOMING)
        self.sonet_pcp_table_qtv_outgoing.setModel(self._table_model_outgoing)
        self.sonet_pcp_table_qtv_incoming.setModel(self._table_model_incoming)

        # Stackoverflow - QSortProxyModel for sorting the columns, TOO SLOW! :(
        # tableModel = Model()
        # tableView = QtGui.QTableView()
        # proxyModel = QtGui.QSortFilterProxyModel()
        # proxyModel.setSourceModel(tableModel)
        # tableView.setModel(proxyModel)
        # tableView.setSortingEnabled(True)
        # tableView.show()
        # app.exec_()

        # List model, it should be declared after table model
        self._list_model = ListModel()
        self.sonet_mission_tree_qlv.setModel(self._list_model)
        # TODO: Explain why this ordering when declaring table + list model

        # Connect signals and slots
        self.sonet_add_spacecraft_qpb.clicked.connect(self.clicked_new_spacecraft)
        self.sonet_remove_spacecraft_qpb.clicked.connect(self.clicked_remove_spacecraft)
        self.sonet_pcp_filter_qpb.clicked.connect(self.clicked_apply_filter)
        self.sonet_select_trajectory_qpb.clicked.connect(self.clicked_select_trajectory)
        self.sonet_draw_qpb.clicked.connect(self.clicked_draw)
        self.sonet_open_matlab_pcp_viewer.clicked.connect(self.clicked_pcp_viewer)
        self.sonet_pcp_generator_qpb.clicked.connect(self.clicked_pcp_manager)
        self.sonet_mission_tree_qlv.clicked.connect(self._list_model.list_clicked)
        self.sonet_pcp_tabs_qtw.currentChanged.connect(self.clicked_tab)
        # self.sonet_pcp_table_qtv_outgoing.horizontalHeader().sortIndicatorChanged.connect(self.clicked_table_view_column)
        self.sonet_pcp_table_qtv_outgoing.horizontalHeader().sectionClicked.connect(self.clicked_table_view_column)
        self.sonet_pcp_table_qtv_incoming.horizontalHeader().sectionClicked.connect(self.clicked_table_view_column)


    # Signals should be defined only within classes inheriting from QObject!
    # +info:https://wiki.qt.io/Qt_for_Python_Signals_and_Slots

    def clicked_apply_filter(self):
        """
        Slot executed when clicked over 'Apply filter' button. It executes the modal window
        for applying filters to the currently available spacecrafts.

        When clicked accept button, it travers all the spacecrafts, and store the modified
        filters from the window. The filters are applied on demand when clicked over a specified
        spacecraft in the main window list view.
        """
        sonet_log(SonetLogType.INFO, 'SonetMainWindow.clicked_apply_filter')

        # Get the spacecrafts list and the current selected spacecraft.
        arg1 = database.get_spacecrafts_list()
        arg2 = self.sonet_mission_tree_qlv.currentIndex().row()

        # SonetPCPFilterQt.
        filter_dialog_qt = SonetPCPFilterQt(self, ar_list_spacecrafts=arg1, ar_current_index=arg2)

        # Update pointer to the dialog, e.g. for accessing to its status bar.
        self._p_pcp_filter_window = filter_dialog_qt

        filter_dialog_qt.setModal(True)
        filter_dialog_qt.setSizeGripEnabled(True)
        filter_dialog_qt.exec_()

        # Force Qt repaint to update the table views.
        index = get_main_window().sonet_mission_tree_qlv.currentIndex()
        self.sonet_mission_tree_qlv.clicked.emit(index)  # The filters are applied here inside.
        # TODO Awkward update, to improve.

    def clicked_draw(self):
        sonet_log(SonetLogType.INFO, 'SonetMainWindow.clicked_draw')
        self.statusbar.showMessage('Not yet implemented :).', SONET_MSG_TIMEOUT)

        # self.statusbar.showMessage('Drawing the mission...', 1000)
        # self.canvas_window = SonetCanvasQt()

    def clicked_new_spacecraft(self):
        """
        This method is called when clicking over 'Add SonetSpacecraft' QPushButton, it creates a new SonetSpacecraft.
        :rtype: bool
        """
        sonet_log(SonetLogType.INFO, 'SonetMainWindow.clicked_new_spacecraft')

        db = database.db

        # Create new SonetSpacecraft.

        # Get the widgets values.
        spacecraft_type_crew = self.sonet_spacecraft_type_qcmb.currentText()
        spacecraft_type_return = self.sonet_spacecraft_type_has_return_trajectory_qcmb.currentText()
        spacecraft_name = self.sonet_sc_name_le.text()

        # If the input s/c name is empty, popup a msg and exit.
        if spacecraft_name == '':
            popup_msg(window_title='Empty s/c name',
                      icon=QMessageBox.Information,
                      text='Please, select a different s/c name.',
                      info_text='')
            return False

        # If the input s/c name is already in the db, popup a msg and exit.
        if spacecraft_name in db:
            popup_msg(window_title='Duplicated s/c name',
                      icon=QMessageBox.Information,
                      text='Please, select a different s/c name.',
                      info_text='')
            return False

        # Create the s/c. The ap_main_window parameter is to pass a pointer to the main window to the s/c, so she can access
        # to main window's methods and properties.
        db[spacecraft_name] = SonetSpacecraft(spacecraft_name, spacecraft_type_crew, spacecraft_type_return, ap_main_window=main_window)

        # Update list model
        lm = self.get_list_model()
        lm.update()

        msg = ('Created Spacecraft ' + spacecraft_name
                  + ' (' + spacecraft_type_crew + ', ' + spacecraft_type_return + ')')
        sonet_log(SonetLogType.INFO, 'SonetMainWindow.clicked_new_spacecraft."' + msg + '"')

        return True

    def clicked_pcp_manager(self):
        sonet_log(SonetLogType.INFO, 'SonetMainWindow.clicked_pcp_manager')

        pcp_manager_window = SonetPCPManagerQt(self, p_main_window=self, p_mat_eng=matlab_engine)

    def clicked_pcp_viewer(self):
        """
        When user clicks over 'PCP Viewer' btn, the current pcp being displayed should be sent to matlab and a contour
        plot generated.
        The user selects the desired trajectory, and when closing the window, the selected trajectory appears selected
        back in the python app.
        """
        sonet_log(SonetLogType.INFO, 'SonetMainWindow.clicked_pcp_viewer')
        # self.statusbar.showMessage('Not yet implemented :).', SONET_MSG_TIMEOUT)

        # Get the current displayed pcp, as dataframe.
        df = self.sonet_pcp_tabs_qtw.currentWidget().children()[1].model()._data

        # Check.
        if df is None:
            self.statusbar.showMessage('No PCP selected.', SONET_MSG_TIMEOUT)
            return
        elif df.empty:
            self.statusbar.showMessage('No PCP selected.', SONET_MSG_TIMEOUT)
            return

        # Save it to a temporary mat file, which is read by matlab.
        if self.sonet_pcp_tabs_qtw.currentWidget().objectName() == 'sonet_pcp_table_transit_1':
            departure_planet = 'Earth'
            arrival_planet = 'Mars'
        else:
            departure_planet = 'Mars'
            arrival_planet = 'Earth'

        mat_file = SONET_DATA_DIR + 'pcp_viewer_tmp.mat'
        savemat(mat_file, {'departure_planet': departure_planet,
                           'arrival_planet': arrival_planet,
                           'jd0': QDate.toJulianDay(df.iloc[0].DepDates),
                           'cal0': [df.iloc[0].DepDates.year(), df.iloc[0].DepDates.month(), df.iloc[0].DepDates.day()],
                           'departure_dates': df.DepDates.apply(QDate.toJulianDay).tolist(),
                           'arrival_dates': df.ArrivDates.apply(QDate.toJulianDay).tolist(),
                           'm_departure_dates': df.attrs['m_departure_dates'], # This are the original dep dates in the mat file, before filtering trajectories by max dvt.
                           'tofs': df.tof.tolist(),
                           'm_tofs': df.attrs['m_tofs'], # This are the original dep dates in the mat file, before filtering trajectories by max dvt.
                           'dvd': df.dvd.tolist(),
                           'dva': df.dva.tolist(),
                           'dvt': df.dvt.tolist(),
                           'theta': df.theta.tolist()})  # In degrees!

        # Read mat file with matlab, display pcp plot, and return last selected trajectory when closed the app.
        selected_trajectory = matlab_engine.PCP_Viewer(mat_file, nargout=1)
        self.clicked_select_trajectory(p_called_from_pcp_viewer=True, p_pcp_viewer_selected_trajectory=int(selected_trajectory))

        print(df.iloc[int(selected_trajectory)])

    def clicked_remove_spacecraft(self):
        # Get the current list view selection.
        selection = self.sonet_mission_tree_qlv.currentIndex().row()

        # If there's no SonetSpacecraft, then return.
        db = database.db
        if len(list(db.keys())) is 0:
            sonet_log(SonetLogType.INFO, 'SonetMainWindow.clicked_remove_spacecraft."No s/c to remove"')
            self.statusbar.showMessage('No s/c to remove.', SONET_MSG_TIMEOUT)
            return True

        # If there is no selection, remove last SonetSpacecraft.
        if (selection is -1):
            selection = len(list(db.keys())) - 1

        # Remove it from the database.
        key = list(db.keys())[selection] # The selected object (e.g. SonetSpacecraft).
        del db[key]

        # Update table models.
        self.get_table_model(TripType.OUTGOING).reset_model()
        self.get_table_model(TripType.INCOMING).reset_model()

        # Update list model.
        lm = self.get_list_model()
        lm.update()

        # Update main window widgets/labels/progress bars.
        force_table_view_update()
        self.update_trajectory_label_and_progress_bar(a_reset_widgets=True)

        msg = key + ' removed'
        sonet_log(SonetLogType.INFO, 'SonetMainWindow.clicked_remove_spacecraft."' + msg + '"')

        return True

    def clicked_select_trajectory(self, p_called_from_pcp_viewer=False, p_pcp_viewer_selected_trajectory=None):
        """
        Gets the current selection for the current selected s/c and stores it inside the s/c.
        If no selection, displays a msg in the main window status bar.
        It also informs to the user, by updating the relevant widgets.
        Update: Refactored to include also the possibility to be called from clicked_pcp_viewer.
        """
        sonet_log(SonetLogType.INFO, 'SonetMainWindow.clicked_select_trajectory')

        # Get the current selected s/c.
        index = self.sonet_mission_tree_qlv.currentIndex().row()
        the_spacecraft = self._list_model.get_spacecraft(a_row=index)

        # Check
        if the_spacecraft is None:
            sonet_log(SonetLogType.INFO, 'SonetMainWindow.clicked_select_trajectory."No s/c selected"')
            self.statusbar.showMessage('No s/c selected.', SONET_MSG_TIMEOUT)
            return False

        # Set the selected trajectory within the s/c.
        the_selected_trajectory: pd.Series
        the_selected_trajectory, index, is_incoming_trajectory = self.get_selected_trajectory(p_called_from_pcp_viewer, p_pcp_viewer_selected_trajectory)
        the_spacecraft.set_trajectory(the_selected_trajectory, index, a_is_incoming_trajectory=is_incoming_trajectory)

        # Update the trajectory label & progress bar.
        status = the_spacecraft.get_trajectory_selection_status()
        self.update_trajectory_label_and_progress_bar(status)
        force_table_view_update()
        # Force focus on main window.
        self.raise_()

    def clicked_tab(self, index):
        """
        Slot executed whenever the Earth-Mars/Mars-Earth tab is changed. Sometimes, the signal is emitted to force
        an update.
        It controls the state of the main window labels and progress bar, which communicate to the usr the current
        trajectory selection state for a given s/c.
        """
        sonet_log(SonetLogType.INFO, 'SonetMainWindow.clicked_tab')

        if self.sonet_mission_tree_qlv.currentIndex().row() is not -1:
            if index is 0:
                # Outgoing trip selected.

                # Update the # rows filtered label.
                n_filtered = main_window._table_model_outgoing._data.shape[0]
                n = database.get_pcp_table(TripType.OUTGOING).shape[0]
                self.sonet_label_rows_filtered_visible.setText(str(n_filtered) + ' rows filtered out of ' + str(n))

            elif index is 1:
                # Incoming trip selected.

                # If the selected s/c has no return trajectory, inform to the user.
                row = self.sonet_mission_tree_qlv.currentIndex().row()
                the_spacecraft = self._list_model.get_spacecraft(a_row=row)
                if the_spacecraft.get_has_return_trajectory() is False:
                    self.sonet_label_rows_filtered_visible.setText('This s/c has no return trip.')
                    return

                # Update the # rows filtered label.
                n_filtered = main_window._table_model_incoming._data.shape[0]
                n = database.get_pcp_table(TripType.OUTGOING).shape[0]
                self.sonet_label_rows_filtered_visible.setText(str(n_filtered) + ' rows filtered out of ' + str(n))
        else:
            self.sonet_label_rows_filtered_visible.setText('')

        # Update the trajectory selection, in case there is a trajectory selected for the current s/c.
        the_sc = get_current_sc()
        main_window.update_trajectory_selection_in_table_view(the_sc)

    def clicked_table_view_column(self, logicalIndex):
        force_table_view_update()

    def exit_app(self):
        sys.exit()

    def get_list_model(self):
        return self._list_model

    def get_selected_trajectory(self, p_called_from_pcp_viewer=False, p_pcp_viewer_selected_trajectory=None):
        """
        Getter method.
        You get:
            - The selected trajectory in the current tab pcp table, as a pandas Series.
            - Its position in the pcp table (index).
            - A flag indicating if it's a outgoing/incoming trajectory
        Update: Refactored to include also the possibility to be called from clicked_pcp_viewer.
        @return: (Series, QModelIndex, bool)
        """
        sonet_log(SonetLogType.INFO, 'SonetMainWindow.get_selected_trajectory')

        # We are setting Earth-Mars or Mars-Earth trajectory?
        tab_index = main_window.sonet_pcp_tabs_qtw.currentIndex()

        # If trajectory was selected from the pcp_viewer pcp plot, or directly through the table.
        if p_called_from_pcp_viewer and p_pcp_viewer_selected_trajectory:
            if tab_index is 0:
                the_row = p_pcp_viewer_selected_trajectory
                the_real_dataframe_index = p_pcp_viewer_selected_trajectory
                the_df = self._table_model_outgoing._data
                is_incoming_trajectory = False
            elif tab_index is 1:
                the_row = p_pcp_viewer_selected_trajectory
                the_real_dataframe_index = p_pcp_viewer_selected_trajectory
                the_df = self._table_model_incoming._data
                is_incoming_trajectory = True
            else:
                sonet_log(SonetLogType.WARNING, 'SonetMainWindow.get_selected_trajectory."Unexpected behaviour')
                return None, None, None
        else:
            if tab_index is 0:
                the_index = self.sonet_pcp_table_qtv_outgoing.selectionModel().currentIndex()
                the_row = the_index.row()
                the_df = self._table_model_outgoing._data
                the_real_dataframe_index = the_df.index[the_row]
                is_incoming_trajectory = False
            elif tab_index is 1:
                the_index = self.sonet_pcp_table_qtv_incoming.selectionModel().currentIndex()
                the_row = the_index.row()
                the_df = self._table_model_incoming._data
                the_real_dataframe_index = the_df.index[the_row]
                is_incoming_trajectory = True
            else:
                sonet_log(SonetLogType.WARNING, 'SonetMainWindow.get_selected_trajectory."Unexpected behaviour')
                return None, None, None

        if the_row < 0:
            sonet_log(SonetLogType.INFO, 'SonetMainWindow.get_selected_trajectory."No row selected"')
            return None, None, None

        # The try-catch is because if the returned dataframe the_df is empty, and you try to access a
        # position in it, you get an IndexError exception.
        try:
            result: pd.Series
            result = the_df.iloc[the_row]
            return result, the_real_dataframe_index, is_incoming_trajectory
        except IndexError:
            sonet_log(SonetLogType.WARNING,
                      'SonetMainWindow.get_selected_trajectory."Empty/Out-of-bonds dataframe accessed"')
            return None, None, None

    def get_table_model(self, pcp_table_model=None):
        switcher = {
            TripType.OUTGOING: self._table_model_outgoing,
            TripType.INCOMING: self._table_model_incoming
        }
        return switcher.get(pcp_table_model, 'Error in SonetMainWindow.get_table_model: '
                                             'No model found with the requested argument')

    def update_trajectory_label_and_progress_bar(self, a_status=0, a_reset_widgets=False):
        """
        Updates both label & progbar widgets.
        :param a_status: 0, 0.5, 1
        :return:
        """
        sonet_log(SonetLogType.INFO,
                  'SonetMainWindow.update_trajectory_label_and_progress_bar')
        if a_reset_widgets:
            self.sonet_label_selected_trajectory.setText('')
            self.sonet_trajectory_selection_qprogrbar.setValue(0)
        else:
            if a_status == 0:
                self.sonet_label_selected_trajectory.setText('Pending to select trajectories.')
                self.sonet_trajectory_selection_qprogrbar.setValue(0)
            elif a_status == 0.5:
                self.sonet_label_selected_trajectory.setText('Pending to select trajectories.')
                self.sonet_trajectory_selection_qprogrbar.setValue(50)
            elif a_status == 1:
                self.sonet_label_selected_trajectory.setText('Trajectories selected.')
                self.sonet_trajectory_selection_qprogrbar.setValue(100)
            else:
                sonet_log(SonetLogType.ERROR,
                          'SonetMainWindow.update_trajectory_label_and_progress_bar."Wrong argument value"')

    def update_trajectory_selection_in_table_view(self, a_the_sc: SonetSpacecraft):
        """
        Selects the current selected trajectory for the passed s/c, in the relevant table view.

        @param a_the_sc: the s/c
        """
        sonet_log(SonetLogType.INFO, 'SonetMainWindow.update_trajectory_selection_in_table_view')

        # Check.
        if a_the_sc is None:
            return

        # Get widgets current selection.
        qlv_index = main_window.sonet_mission_tree_qlv.currentIndex().row()
        qtw_index = main_window.sonet_pcp_tabs_qtw.currentIndex()
        # & other stuff.
        sc_has_return_trajectory = a_the_sc.get_has_return_trajectory()

        # Continue only if valid selection.
        if -1 not in [qlv_index, qtw_index]:

            if sc_has_return_trajectory:
                # There are both out/inc trips, update both out/inc table views.
                if qtw_index == 0:
                    the_model = self._table_model_outgoing
                    the_df = the_model._data

                    the_current_dataframe_index = a_the_sc._trajectory1_index
                    try:
                        the_current_position_in_table_view = the_df.index.to_list().index(the_current_dataframe_index)
                        the_index = the_model.createIndex(the_current_position_in_table_view, 0)
                    except ValueError:
                        the_index = the_model.createIndex(-1, -1)

                    self.sonet_pcp_table_qtv_outgoing.setCurrentIndex(the_index)
                elif qtw_index == 1:
                    the_model = self._table_model_incoming
                    the_df = the_model._data

                    the_current_dataframe_index = a_the_sc._trajectory2_index
                    try:
                        the_current_position_in_table_view = the_df.index.to_list().index(the_current_dataframe_index)
                        the_index = the_model.createIndex(the_current_position_in_table_view, 0)
                    except ValueError:
                        the_index = the_model.createIndex(-1, -1)

                    self.sonet_pcp_table_qtv_incoming.setCurrentIndex(the_index)
                else:
                    sonet_log(SonetLogType.WARNING,
                              'SonetMainWindow.update_trajectory_selection_in_table_view."Not supposed to arrive here"')
                    return
            else:
                # There is only out trip, so update only out table view.
                if qtw_index == 0:
                    # First, get the real stored dataframe index for the s/c. Then, find where is this current row in
                    # the current table view, as the user may filter the columns, dataframe index 10 (for example) may
                    # be located in row 1100 of the current displayed table view.

                    the_model = self._table_model_outgoing
                    the_df = the_model._data

                    the_current_dataframe_index = a_the_sc._trajectory_index
                    try:
                        the_current_position_in_table_view = the_df.index.to_list().index(the_current_dataframe_index)
                        the_index = the_model.createIndex(the_current_position_in_table_view, 0)
                    except ValueError:
                        the_index = the_model.createIndex(-1, -1)

                    self.sonet_pcp_table_qtv_outgoing.setCurrentIndex(the_index)
                elif qtw_index == 1:
                    pass
                else:
                    sonet_log(SonetLogType.WARNING,
                              'SonetMainWindow.update_trajectory_selection_in_table_view."Not supposed to arrive here"')
                    return



# TODO: Move TableModel and ListModel classes outside main_window.py file.
class ListModel(QAbstractListModel):
    """
    TODO docstring ListModel()
    """

    def __init__(self, data=None, parent=None):
        super(ListModel, self).__init__(parent)
        self._data = {}.keys()  # It's a dictionary keys

    def get_data(self):
        return list(self._data)

    def get_spacecraft(self, a_index=None, a_row=None):
        """
        Getter method.
        It returns the SonetSpacecraft object from the database, based on the current
        selected item. You can query by QModelIndex or by row.
        Returns None object if no s/c selected or if encountered any problem.
        :rtype: SonetSpacecraft
        """
        # Checks.
        if (a_index is None and a_row is None):
            return None
        if (not isinstance(a_index, QModelIndex)) and (not isinstance(a_row, int)):
            return None

        # Get the clicked s/c position in the list.
        if a_index:
            row = a_index.row()
        elif isinstance(a_row, int):
            row = a_row
        else:
            row = None

        # Check.
        if row is -1:
            # No s/c selected, return None object.
            sonet_log(SonetLogType.INFO, 'ListModel.get_spacecraft."Selected row is -1"')
            return None

        key = None
        try:
            # Get the clicked s/c name.
            key = list(self._data)[row]
            sonet_log(SonetLogType.INFO, 'ListModel.get_spacecraft."Spacecraft ' + key + '"')
        except:
            sonet_log(SonetLogType.WARNING, 'SonetMainWindow.get_spacecraft."Exception raised"')
            return None

        return database.db[key]

    def list_clicked(self, a_index):
        """
        Slot executed whenever an item from the ListModel is clicked. It sets both
        the outgoing and incoming table models, and updates both associated table views.

        There are two possible situations. The clicked spacecraft has only
        TripType.OUTGOING trip type, or both TripType.OUTGOING and TripType.INCOMING.
        If it is the first case, then for the return trip, an empty dataframe
        is displayed.

        The process is the following:
            - You get the s/c.
            - You get its filter.
            - You apply this filter to the pcp table (possible performance issue if pcp has millions
            of rows?)
            - The resultant pcp dataframe is set as the QTableView table model, to be displayed to the user.
        """

        sonet_log(SonetLogType.INFO, 'SonetMainWindow.list_clicked')

        # In case no s/c is selected.
        if a_index.row() is -1:
            sonet_log(SonetLogType.INFO, 'list_clicked."No s/c selected"')
            return

        # Otherwise, get the s/c, and its filter.
        the_sc = self.get_spacecraft(a_index=a_index)
        if not isinstance(the_sc, SonetSpacecraft):
            sonet_log(SonetLogType.ERROR, 'list_clicked."Wrong s/c type"')
            return False

        SonetTrajectoryFilter.update_filters_dependencies(the_sc.get_filter())
        the_filter = the_sc.get_filter()

        if not the_sc.get_has_return_trajectory():
            # The sc has got only outgoing trajectory.

            # Get the filtered pcp dataframe.
            the_filtered_dataframe = the_filter.get_filtered_pcp()
            # Update the table model.
            main_window._table_model_outgoing.set_model_data(the_sc, the_filtered_dataframe)

            # Again for the 2nd table view.
            the_filtered_dataframe = pd.DataFrame()
            main_window._table_model_incoming.set_model_data(the_sc, the_filtered_dataframe)
        else:
            # The sc has got both outgoing and incoming trajectories.
            sonet_log(SonetLogType.INFO, 'list_clicked."This spacecraft is of two-way type"')

            # Get the filtered pcp dataframe.
            the_filtered_dataframe = the_filter[0].get_filtered_pcp()
            # Update the table model.
            main_window._table_model_outgoing.set_model_data(the_sc, the_filtered_dataframe)

            # Again for the 2nd table view.
            the_filtered_dataframe = the_filter[1].get_filtered_pcp()
            main_window._table_model_incoming.set_model_data(the_sc, the_filtered_dataframe)

        # Update the trajectory label & progress bar.
        status = the_sc.get_trajectory_selection_status()
        main_window.update_trajectory_label_and_progress_bar(status)
        # & select current trajectory in the table view.
        main_window.update_trajectory_selection_in_table_view(the_sc)
        force_table_view_update()

    def update(self):
        self.beginResetModel()
        self._data = list(database.db.keys())
        self.endResetModel()

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self._data)

    def data(self, QModelIndex, int_role=None):
        row = QModelIndex.row()
        if int_role == Qt.DisplayRole:
            return str(list(self._data)[row])

    def flags(self, QModelIndex):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


class TableModel(QAbstractTableModel):
    """
    The Earth-Mars and Mars-Earth table views displayed in the main window are QAbstractTableModels.
    """

    def __init__(self, a_spacecraft=None, a_trip_type=None, parent=None):
        super(TableModel, self).__init__(parent)
        self._data = pd.DataFrame()
        self._trip_type = a_trip_type
        self._spacecraft = a_spacecraft

    def get_spacecraft(self):
        """
        Getter method.
        Returns the spacecraft owner of the table model's current data.
        """
        return self._spacecraft

    def set_model_data(self, a_the_spacecraft=None, a_the_filtered_dataframe=None):
        """
        Set the table model's internal _data, stored as dataframe.
        """
        sonet_log(SonetLogType.INFO, 'TableModel.set_model_data."' + str(self._trip_type) + '"')

        # The spacecraft which owns the data.
        self._spacecraft = a_the_spacecraft

        # The data.
        self.beginResetModel()
        self._data = a_the_filtered_dataframe.reset_index(drop=True)
        self.endResetModel()

    def reset_model(self):
        """
        Reset the table model.
        """
        sonet_log(SonetLogType.INFO, 'TableModel.reset_model')

        self.beginResetModel()
        self._data = None
        self.endResetModel()
        return True

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        # try:
        #     self.dict_key
        # except AttributeError:
        #     return 0
        # else:
        #     return self._data[self.dict_key].get_pcp_table(self._trip_type).shape[0]
        if self._data is None:
            return 0
        return self._data.shape[0]  # Number of rows of the dataframe

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        # try:
        #     self.dict_key
        # except AttributeError:
        #     return 0
        # else:
        #     return self._data[self.dict_key].get_pcp_table(self._trip_type).shape[1]
        if self._data is None:
            return 0
        return self._data.shape[1]  # Number of columns of the dataframe

    def data(self, index=QModelIndex, role=None):
        if not index.isValid():
            return None

        row = index.row()
        column = index.column()

        if role == Qt.DisplayRole:

            value = self._data.iloc[row, column]

            # Perform per-type checks and render accordingly.
            if isinstance(value, datetime.datetime):
                # Render time to YYY-MM-DD.
                return value.strftime("%Y-%m-%d")

            if isinstance(value, float):
                # Render float to 2 dp
                return "%.2f" % value

            if isinstance(value, str):
                # Render strings with quotes
                return '"%s"' % value

            # Default (anything not captured above: e.g. int)
            return value

        if role == Qt.BackgroundRole:
            # Pair rows will have different color, to visually distinguish them from the even ones.
            if row % 2 is not 0:
                return QColor(255, 230, 255)
            # Very light blue 230, 242, 255
            # Very light purple 240, 240, 245
            # Very light pink 255, 230, 255
        return None

    def headerData(self, section, orientation, role):

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])
        return None

    def sort(self, Ncol, order):
        """
        Sort table by given column number.
        https://stackoverflow.com/questions/28660287/sort-qtableview-in-pyqt5
        """
        try:
            self.layoutAboutToBeChanged.emit()
            self._data = self._data.sort_values(self._data.columns[Ncol], ascending=not order)
            self.layoutChanged.emit()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    # Using no fbs module
    # Add as parameter to the script to set an app style: -style Fusion|Windows|windowsvista
    app = QApplication(sys.argv)

    # App style cyberpunk|darkblue|oceanic|lightorange|darkorange|qdarkstyle|qdarkstyle3.
    # stylesheet = qrainbowstyle.load_stylesheet_pyside2(style='qdarkstyle')
    # app.setStyleSheet(stylesheet)

    main_window = SonetMainWindow()
    main_window.show()

    sys.exit(app.exec_())

    # Using fbs module
    # appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    # main_window = SonetMainWindow()
    # main_window.show()
    # exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    # sys.exit(exit_code)

    # Example app.
    # appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    # window = QMainWindow()
    # window.resize(250, 150)
    # window.show()
    # exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    # sys.exit(exit_code)