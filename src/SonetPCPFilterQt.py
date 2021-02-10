# General imports
import sys
import pandas as pd

# Qt imports
from PySide2.QtCore import QCoreApplication, Qt, QAbstractTableModel, QModelIndex, QDate
from PySide2.QtWidgets import QDialog, QApplication, QDialogButtonBox, QMessageBox, QStatusBar

# Sonet imports
from src import database
from src import sonet_pcp_filter_qt_ui
from src.SonetSpacecraft import SonetSpacecraft
from src.SonetUtils import FilterType, TripType, SonetLogType, sonet_log, popup_msg, SONET_MSG_TIMEOUT


# ==============================================================================================
# ==============================================================================================
#
#
#                                    CLASS SonetPCPFilterQt
#                            (also class SonetAppliedFiltersTableModel)
#
# ==============================================================================================
# ==============================================================================================

class SonetPCPFilterQt(QDialog, sonet_pcp_filter_qt_ui.Ui_sonet_pcp_filter):
    """
    The filter window (QDialog).
    """
    def __init__(self, *args, ar_list_spacecrafts=None, ar_current_index=-1):
        super(SonetPCPFilterQt, self).__init__(*args)  # , **kwargs)
        self.setupUi(self)
        self.init(ar_list_spacecrafts, ar_current_index)

        # Draft
        # self._applied_filters_table_model = SonetAppliedFiltersTableModel()
        # self.applied_filters_table_view.setModel(self._applied_filters_table_model)
        self.applied_filters_table_view.resizeColumnsToContents()

        # Status bar,for messages to the user.
        self.status_bar = QStatusBar()
        self.status_bar.setSizeGripEnabled(False)
        self.status_bar_HLayout.addWidget(self.status_bar)

    def init(self, ar_list_spacecrafts=None, ar_current_index=-1):
        """
        Initializes the SonetPCPFilterQt window. It also sets the signal/slot connections.
        :param ar_list_spacecrafts: The list of available s/c's.
        :param ar_current_index: The current selected s/c.

        - LESSON LEARNED [#35] The init_combo_select_spacecraft method triggers table model and filters updates, so
        depends on them, i.e. at the time we call this method, those dependencies should have been constructed.
        The proper way to init this window is calling
        1) init_table_model,
        2) init_filters,
        3) init_combo_select_spacecraft.
        """
        # Connect signals and slots.
        self.btn_accept = self.dialog_button_box.button(QDialogButtonBox.Ok)
        self.btn_accept.clicked.connect(self.clicked_pb_accept)
        self.btn_accept.clicked.connect(self.accept)

        self.btn_cancel = self.dialog_button_box.button(QDialogButtonBox.Cancel)
        self.btn_cancel.clicked.connect(self.clicked_pb_cancel)
        self.btn_cancel.clicked.connect(self.reject)

        self.pb_add.clicked.connect(self.clicked_pb_add)
        self.pb_reset.clicked.connect(self.clicked_pb_reset)
        self.pb_delete.clicked.connect(self.clicked_pb_delete)
        self.pb_delete_all.clicked.connect(self.clicked_pb_delete_all)
        self.select_spacecraft.currentIndexChanged.connect(self.changed_cmb_select_spacecraft)
        self.select_trip.currentIndexChanged.connect(self.changed_cmb_select_trip)
        self.combo_energy_parameter.currentIndexChanged.connect(self.changed_cmb_energy_parameter)
        self.combo_dept_arriv.currentIndexChanged.connect(self.changed_cmb_dept_arriv)
        self.combo_select_spacecraft.currentIndexChanged.connect(self.changed_combo_select_spacecraft)
        self.combo_at_least.currentIndexChanged.connect(self.changed_combo_at_least)

        self.cb_dep_arriv_dates.stateChanged.connect(self.enable_pb_add)
        self.cb_dep_arriv_dates.stateChanged.connect(self.changed_cb_departure_dates_step1)
        self.cb_dates_1.stateChanged.connect(self.changed_cb_departure_dates_step2)
        self.cb_dates_2.stateChanged.connect(self.changed_cb_departure_dates_step3)

        self.cb_energy.stateChanged.connect(self.enable_pb_add)
        self.cb_energy.stateChanged.connect(self.changed_cb_energy)

        self.cb_time_of_flight.stateChanged.connect(self.enable_pb_add)
        self.cb_time_of_flight.stateChanged.connect(self.changed_cb_time_of_flight)

        self.radio_mission.toggled.connect(self.clicked_radio_mission)
        self.radio_spacecraft.toggled.connect(self.clicked_radio_spacecraft)

        # Next 3 statements should be called sequentially, see method's docstring.
        # Init table model and table view
        self.init_table_model()
        # Retrieve the current filters.
        self.init_filters(ar_list_spacecrafts)
        # Fill select_spacecraft combo with the available spacecrafts and select the current one.
        self.init_combo_select_spacecraft(ar_list_spacecrafts, ar_current_index)

        self.dateEdit.setDisplayFormat('dd-MM-yyyy')
        self.dateEdit.setCalendarPopup(True)

        # Computations
        self.compute_spacecrafts_with_selected_trajectories(p_return_type='String')

    def init_combo_select_spacecraft(self, ar_list_spacecrafts=None, ar_current_index=-1):
        """
        Fill select_spacecraft combo box with the available spacecrafts.
        And select the one selected by the user.
        If no selection (ar_current_index = -1, then 0 should be selected, which tells
        the user that it has to do a selection.
        :param ar_list_spacecrafts: The list of available s/c's.
        :param ar_current_index: The current selected s/c.
        """
        self.select_spacecraft.addItems(ar_list_spacecrafts)
        if ar_current_index is not -1:
            self.select_spacecraft.setCurrentIndex(ar_current_index + 1)  # The '+1' is because the combo box is already
            # populated with 'Select SonetSpacecraft...' item when the above addItems() is executed.
        else:
            self.select_spacecraft.setCurrentIndex(0)

    def init_filters(self, ar_list_spacecrafts=None):
        """
        Retrieves the filters for the spacecrafts in ar_list_spacecrafts, and stores them in a dict.
        Copies that dict to restore it in case the user cancels the window.
        :param ar_list_spacecrafts:
        """
        # Retrieve the filters dataframes into a dict.
        self._dict_filters_current = {}
        for sc_name in ar_list_spacecrafts:
            sc: SonetSpacecraft = database.db[sc_name]
            self._dict_filters_current[sc_name] = sc.get_filter_data(p_get_dataframe_copy=True)

    def init_table_model(self):
        """
        Initialize the table model and connect the table view to it.
        :return:
        """
        self._applied_filters_table_model = SonetAppliedFiltersTableModel()
        self.applied_filters_table_view.setModel(self._applied_filters_table_model)

    def compute_spacecrafts_with_selected_trajectories(self, p_return_type='String'):
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.get_spacecrafts_with_selected_trajectories')

        # List with available s/c for which the user has selected at least a trajectory.
        self._spacecrafts_with_selected_trajectories = []

        # Traverse all the spacecrafts and update their filters.
        for sc_name in database.get_spacecrafts_list():
            sc = database.get_spacecraft(sc_name)

            # If the sc has at least one trajectory selected, then should be included in the list.
            if sc.get_trajectory_selection_status() in [0.5, 1]:
                if p_return_type == 'String':
                    self._spacecrafts_with_selected_trajectories.append(sc.get_spacecraft_name())
                elif p_return_type == 'Object':
                    self._spacecrafts_with_selected_trajectories.append(sc)

        # The current selected element (in select_spacecraft combo) shouldn't be included in the list.
        current_selected_sc = self.select_spacecraft.currentText()
        if p_return_type == 'Object':
            current_selected_sc = database.get_spacecraft(current_selected_sc)

        try:
            index = self._spacecrafts_with_selected_trajectories.index(current_selected_sc)
            self._spacecrafts_with_selected_trajectories.pop(index)
        except ValueError:
            # The current selected s/c isn't in the list, so nothing to do.
            pass

        sonet_log(SonetLogType.INFO,
                  'SonetPCPFilterQt.get_spacecrafts_with_selected_trajectories.'
                  '"Number of s/c with at least a trajectory selected: ' +
                  str(len(self._spacecrafts_with_selected_trajectories)) + '"')

    def dates_combos_check1(self):
        """
        docstring
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.dates_combos_check1')

        list_checked_cb = self.which_cb_checked()

        c1 = 'cb_dep_arriv_dates+0' in list_checked_cb
        c2 = 'cb_dep_arriv_dates+1' in list_checked_cb
        c3 = 'cb_dep_arriv_dates+2' in list_checked_cb
        if c1 and not (c2 or c3):
            popup_msg(window_title='Incomplete filters selection',
                      icon=QMessageBox.Information,
                      text='If the departure/arrival dates filter is checked, then one of the two below'
                           ' options should be also selected.',
                      info_text='Please, do a valid selection.')
            return False
        return True

    def dates_combos_check2(self):
        """
        When the complex dates filter is activated, check that all the relevant widgets have a valid selection.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.dates_combos_check2')

        if self.radio_mission.isChecked():
            self.status_bar.showMessage('Pending to implement mission radio button.',
                                        SONET_MSG_TIMEOUT)
            return False
        elif self.radio_spacecraft.isChecked():
            c1 = self.combo_select_spacecraft.currentText() != 'Selected s/c'
            c2 = self.combo_select_trip.currentText() in ['Earth - Mars', 'Mars - Earth']
            if c1 and c2:
                return True
            else:
                self.status_bar.showMessage('Pending to select combos, please do a valid selection.',
                                            SONET_MSG_TIMEOUT)
                return False
        else:
            # No radio btn is toggled, return.
            self.status_bar.showMessage('No radio button toggled, please select either Mission or S/C.', SONET_MSG_TIMEOUT)
            return False

    def enable_pb_add(self):
        """
        If no checkbox is checked, then disable the 'Add' push button, otherwise it should remain enabled.
        """
        is_any_cb_checked = self.is_any_cb_checked()

        if is_any_cb_checked:
            msg = 'At least one checkbox is checked, "Add" button is enabled'
            self.pb_add.setEnabled(is_any_cb_checked)
        else:
            msg = 'No checkbox is checked, "Add" button is disabled'
            self.pb_add.setEnabled(is_any_cb_checked)

        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.enable_pb_add."' + msg + '"')

    def enable_pb_delete(self, ar_enable):
        """
        Activates, or not the 'Delete' QPushButton.
        :param ar_enable: bool
        """
        self.pb_delete.setEnabled(ar_enable)

    def enable_pb_delete_all(self, ar_enable):
        """
        Activates, or not the 'Delete all' QPushButton.
        :param ar_enable: bool
        """
        self.pb_delete_all.setEnabled(ar_enable)

    def enable_combos(self, ar_enable):
        """
        Activates the group box combos if a valid SonetSpacecraft and trip are selected.
        :param ar_enable: bool flag.
        :return: bool.
        """
        self.enable_groupbox_energy(ar_enable)
        self.enable_groupbox_time_of_flight(ar_enable)
        self.enable_groupbox_departure_dates_step1(ar_enable)
        self.enable_groupbox_applied_filters(ar_enable)

    def enable_departure_dates_step1_combos(self, ar_enable):
        self.combo_dept_arriv.setEnabled(ar_enable)

    def enable_energy_combos(self, ar_enable):
        self.combo_energy_parameter.setEnabled(ar_enable)
        self.combo_energy_operator.setEnabled(ar_enable)
        self.spin_energy_number.setEnabled(ar_enable)

    def enable_time_of_flight_combos(self, ar_enable):
        self.combo_time_of_flight.setEnabled(ar_enable)
        self.combo_time_of_flight_operator.setEnabled(ar_enable)
        self.spin_number_2.setEnabled(ar_enable)
        self.combo_time_scale_2.setEnabled(ar_enable)

    def enable_groupbox_applied_filters(self, ar_enable):
        self.bottom_group_box.setEnabled(ar_enable)
        self.applied_filters_table_view.setEnabled(ar_enable)

    def enable_groupbox_departure_dates_step1(self, ar_enable):
        self.top_left_group_box.setEnabled(ar_enable)
        # If we are disabling the group box, then associated combo boxes should also be disabled.
        if ar_enable is False:
            self.cb_dep_arriv_dates.setChecked(False)
        self.cb_dep_arriv_dates.setEnabled(ar_enable)

    def enable_groupbox_energy(self, ar_enable):
        self.energy_group_box.setEnabled(ar_enable)
        # If we are disabling the group box, then associated combo boxes should also be disabled.
        if ar_enable is False:
            self.cb_energy.setChecked(False)
        self.cb_energy.setEnabled(ar_enable)

    def enable_groupbox_time_of_flight(self, ar_enable):
        self.time_of_flight_group_box.setEnabled(ar_enable)
        # If we are disabling the group box, then associated combo boxes should also be disabled.
        if ar_enable is False:
            self.cb_time_of_flight.setChecked(False)
        self.cb_time_of_flight.setEnabled(ar_enable)

    def get_current_selection(self):
        """
        Getter function.
        :return: The current spacecraft and trip combo selection.
        """
        return self.select_spacecraft.currentText(), self.select_trip.currentText()

    def get_dep_arriv_dates_combos_selection(self):
        """
        Retrieves the SimpleDate & CompexDate widgets data, to apply filters.
        @rtype: dict
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.get_dep_arriv_dates_combos_selection')

        # cb_dates_1 is the more complex dates filter.
        if self.cb_dates_1.isChecked():

            # Step 1. Depending on the 'combo_at_least' selection, the initial list is filled differently.
            current_selection = self.combo_at_least.currentText()

            if current_selection in ['At least', 'At maximum']:
                the_selection = [self.combo_dept_arriv.currentText(),
                                 self.combo_planet.currentText(),
                                 self.combo_at_least.currentText(),
                                 self.spin_number.text(),
                                 self.combo_time_scale.currentText(),
                                 self.combo_when.currentText()]
            # In other cases, disable irrelevant combos.
            elif current_selection in ['At the same time']:
                the_selection = [self.combo_dept_arriv.currentText(),
                                 self.combo_planet.currentText(),
                                 self.combo_at_least.currentText()]
            # Uups.
            else:
                sonet_log(SonetLogType.WARNING, 'SonetPCPFilterQt.get_dep_arriv_dates_combos_selection."Not supposed to arrive here"')

            # Step 2. Depending on which radio btn is checked, behave differently.
            if self.radio_mission.isChecked():
                # Widgets only relevant for the mission radio button.
                self.status_bar.showMessage('Mission radio btn not implemented', SONET_MSG_TIMEOUT)
                pass
            elif self.radio_spacecraft.isChecked():
                # Widgets only relevant for the spacecraft radio button.
                the_selection.append(self.combo_select_spacecraft.currentText())
                the_selection.append(self.combo_select_trip.currentText())
                the_selection.append(self.combo_event.currentText())
            else:
                # No radio btn is toggled, return.
                self.status_bar.showMessage('No radio button toggled, please select either Mission or S/C.',
                                            SONET_MSG_TIMEOUT)
            return {'Status': 1, 'Type': 'ComplexDate', 'Filter': the_selection}

        # cb_dates_2 is the simpler dates filter.
        elif self.cb_dates_2.isChecked():
            the_selection = [self.combo_dept_arriv.currentText(),
                             self.combo_planet.currentText(),
                             self.combo_when_2.currentText(),
                             self.dateEdit.text()]
            return {'Status': 1, 'Type': 'SimpleDate', 'Filter': the_selection}

        else:
            sonet_log(SonetLogType.ERROR, 'SonetPCPFilterQt.get_dep_arriv_dates_combos_selection')
            return {'Status': 1, 'Type': 'SimpleDate', 'Filter': pd.Series()}

    def get_energy_combos_selection(self):
        """
        Retrieves the energy combo boxes data, to apply filters.
        :return: a dict, representing a pandas dataframe row.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.get_energy_combos_selection')

        the_selection = [self.combo_energy_parameter.currentText(),
                         self.combo_energy_operator.currentText(),
                         self.spin_energy_number.text(),
                         self.combo_energy_units.currentText()]
        # return the_selection
        return {'Status': 1, 'Type': 'Energy', 'Filter': the_selection}

    def get_spacecrafts_with_selected_trajectories(self, return_type='String'):
        """
        Getter method.

        Returns the list of sc with at least one selected trajectory, in string or object format.
        If the list isn't calculated, it computes it.
        :rtype: list
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.get_spacecrafts_with_selected_trajectories')

        # Return the list, or compute it if it wasn't defined.
        if return_type == 'String':
            try:
                return self._spacecrafts_with_selected_trajectories
            except NameError:
                return self.compute_spacecrafts_with_selected_trajectories(p_return_type='String')
        elif return_type == 'Object':
            return self.compute_spacecrafts_with_selected_trajectories(p_return_type='Object')

    def get_time_of_flight_combos_selection(self):
        """
        Retrieves the time of flight combo boxes data, to apply filters.
        :return: a dict, representing a pandas dataframe row.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.get_time_of_flight_combos_selection')

        the_selection = ['tof',
                         self.combo_time_of_flight_operator.currentText(),
                         self.spin_number_2.text(),
                         self.combo_time_scale_2.currentText()]
        # return the_selection
        return {'Status': 1, 'Type': 'Time of flight', 'Filter': the_selection}

    def get_table_model(self):
        """
        Getter method.
        :return:
        """
        return self._applied_filters_table_model

    def reset_filter_departure_dates_step1(self):
        """
        Disables the departure/arrival dates filter checkbox and resets all the fields to their default value.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.reset_filter_departure_dates_step1 (dep/arriv dates)')

        self.cb_dep_arriv_dates.setChecked(False)
        self.combo_dept_arriv.setCurrentIndex(0)
        # self.combo_planet.setCurrentIndex(0)

    def reset_filter_departure_dates_left(self):
        """
        Disables the departure/arrival dates filter checkbox and resets all the fields to their default value.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.reset_filter_departure_dates_step2 (left dep/arriv dates)')

        self.cb_dates_1.setChecked(False)
        self.spin_number.setValue(0)
        self.combo_time_scale.setCurrentIndex(0)
        self.combo_when.setCurrentIndex(0)
        self.combo_select_spacecraft.clear()

        # Weird way to uncheck all radio buttons.
        self.radio_mission.setAutoExclusive(False)
        self.radio_spacecraft.setAutoExclusive(False)

        self.radio_mission.setChecked(False)
        self.radio_spacecraft.setChecked(False)

        self.radio_mission.setAutoExclusive(True)
        self.radio_spacecraft.setAutoExclusive(True)

    def reset_filter_departure_dates_right(self):
        """
        Disables the departure/arrival dates filter checkbox and resets all the fields to their default value.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.reset_filter_departure_dates_step3 (right dep/arriv dates)')

        self.cb_dates_2.setChecked(False)
        self.combo_when_2.setCurrentIndex(0)
        self.dateEdit.setDate(QDate(2020, 5, 1))

    def reset_filter_energy(self):
        """
        Disables the energy filter checkbox and resets all the fields to their default value.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.reset_filter_energy')

        self.cb_energy.setChecked(False)
        self.combo_energy_parameter.setCurrentIndex(0)
        self.combo_energy_operator.setCurrentIndex(0)
        # self.spin_energy_number.clear()
        self.spin_energy_number.setValue(0)

    def reset_filter_time_of_flight(self):
        """
        Disables the time of flight filter checkbox and resets all the fields to their default value.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.reset_filter_time_of_flight')

        self.cb_time_of_flight.setChecked(False)
        self.combo_time_of_flight.setCurrentIndex(0)
        self.combo_time_of_flight_operator.setCurrentIndex(0)
        self.combo_time_scale_2.setCurrentIndex(0)
        self.spin_number_2.setValue(0)

    def update_table_model(self):
        """
        Reset the table model.
        """
        spc_selection, trip_selection = self.get_current_selection()
        self.get_table_model().update_model(self._dict_filters_current, spc_selection, trip_selection)
        self.applied_filters_table_view.resizeColumnsToContents()

    def is_any_cb_checked(self):
        """
        Checks if any of the filter checkboxes is checked.
        If at least one is checked, then returns true, otherwise false.
        :return: bool
        """
        any_checked = any([self.cb_time_of_flight.isChecked(),
                           self.cb_dep_arriv_dates.isChecked(),
                           self.cb_energy.isChecked()])
        if any_checked:
            return True
        else:
            return False

    def is_selection_complete(self):
        c1 = self.select_spacecraft.currentText() == 'Select SonetSpacecraft'
        c2 = self.select_trip.currentText() == 'Select trip'
        if not c1 and not c2:
            sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.is_selection_valid."Selection is complete"')
            return True
        else:
            sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.is_selection_valid."Selection is not complete"')
            return False

    def which_cb_checked(self):
        """
        Traverses the SonetPCPFilterQt window to check which checkboxes are checked. It returns a list with the checked
        checkboxes. If no checkbox is checked, it returns and empty list.
        :return: list
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.which_cb_checked')

        any_checked = self.is_any_cb_checked()
        the_list = []

        if any_checked:
            if self.cb_energy.isChecked():
                the_list.append('cb_energy')
            if self.cb_time_of_flight.isChecked():
                the_list.append('cb_time_of_flight')
            if self.cb_dep_arriv_dates.isChecked():
                if self.cb_dates_1.isChecked():
                    the_list.append('cb_dep_arriv_dates+1')
                elif self.cb_dates_2.isChecked():
                    the_list.append('cb_dep_arriv_dates+2')
                else:
                    the_list.append('cb_dep_arriv_dates+0')


        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.which_cb_checked."Checked checkboxes: "' + str(the_list) + '"')

        return the_list

    def changed_cmb_dept_arriv(self):
        """
        Slot executed when the combo_dept_arriv changes its state. Example, if the 'Departure' option is activated,
        then depending on the select_trip combo, the combo_planet will be setted to 'Earth' or 'Mars'.
        """
        trip = self.select_trip.currentText()
        combo = self.combo_dept_arriv.currentText()

        if (trip == 'Earth - Mars' and combo == 'Departs') or (trip == 'Mars - Earth' and combo == 'Arrives'):
            res = 'Earth'
        else:
            res = 'Mars'

        if res == 'Earth':
            self.combo_planet.setCurrentIndex(0)
        else:
            self.combo_planet.setCurrentIndex(1)

    def changed_cmb_energy_parameter(self, ar_index):
        cmb_units = self.combo_energy_units

        if ar_index in [0, 1, 2]:
            # km/s
            cmb_units.setCurrentIndex(0)
            return 0
        elif ar_index in [3, 4]:
            # km2/s2
            cmb_units.setCurrentIndex(1)
            return 0
        elif ar_index in [5]:
            # º
            cmb_units.setCurrentIndex(2)
            return 0
        else:
            sonet_log(SonetLogType.WARNING, 'SonetPCPFilterQt.changed_cmb_energy_parameter')

    def changed_cmb_select_spacecraft(self, ar_index):
        """
        Triggered when the select_spacecraft combo box index changes.

        Updates the 'Select trip' combo box every time the 'Select s/c' changes.
        Checks whether the SonetSpacecraft has only outgoing trip or both outgoing and incoming.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.changed_cmb_select_spacecraft')

        # Retrieve the selected SonetSpacecraft.
        selected_spacecraft = self.select_spacecraft.itemText(ar_index)

        # Get the SonetSpacecraft type.
        if selected_spacecraft == 'Select s/c':
            self.select_trip.clear()
            self.select_trip.addItems(['Select trip'])
            return True
        else:
            has_return_trajectory = database.db[selected_spacecraft].get_has_return_trajectory()

            if not isinstance(has_return_trajectory, bool):
                sonet_log(SonetLogType.ERROR,
                          'SonetPCPFilterQt.changed_cmb_select_spacecraft.'
                          '"S/C with a non bool member has_return_trajectory"')
                return False

            self.select_trip.blockSignals(True)

            if has_return_trajectory is True:
                items = ['Select trip', 'Earth - Mars', 'Mars - Earth']
                self.select_trip.clear()
                self.select_trip.addItems(items)

                self.select_trip.blockSignals(False)

                current_tab = self.parent().sonet_pcp_tabs_qtw.currentIndex()
                self.select_trip.setCurrentIndex(current_tab + 1)

            else:
                items = ['Select trip', 'Earth - Mars']
                self.select_trip.clear()
                self.select_trip.addItems(items)

                self.select_trip.blockSignals(False)

                self.select_trip.setCurrentIndex(1)

            # Every time the selected s/c is changed, the  self._spacecrafts_with_selected_trajectories list should
            # be updated, extracting the current selected s/c in case it is present in the list, as it makes no sense.
            self.compute_spacecrafts_with_selected_trajectories(p_return_type='String')

            return True

    def changed_combo_select_spacecraft(self):
        """
        Mehtod executed whenever the combo_select_spacecraft's index is changed.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.changed_combo_select_spacecraft')

        # Check which radio button is toggled (mission/spacecraft).
        radio_btn_sel = self.which_radio_toggled()

        if radio_btn_sel == 'Spacecraft':
            selected_sc = self.combo_select_spacecraft.currentText()
            self.fill_dates_combo_select_trip(selected_sc)
        elif radio_btn_sel == 'Mission':
            pass
        else:
            sonet_log(SonetLogType.INFO,
                      'SonetPCPFilterQt.changed_combo_select_spacecraft."No s/c nor mission selected"')

    def changed_cmb_select_trip(self):
        """
        Triggered when the select_trip combo box index changes.

        Only once both combo boxes (select_spacecraft, and select_trip) are valid, then we will be able
        to work with a specific porkchop plot table (outgoing or incoming). Once the selection is valid,
        we'll enable the different filtering options combo boxes (i.e. by trajectory energy, by time of flight, etc.).
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.changed_cmb_select_trip')

        selection_is_valid = self.is_selection_complete()

        self.enable_combos(selection_is_valid)
        self.enable_pb_delete(selection_is_valid)
        self.enable_pb_delete_all(selection_is_valid)

        if selection_is_valid:
            self.update_table_model()

        # In any case, reset the filters checkboxes, in case any was checked.
        self.clicked_pb_reset()

    def changed_combo_at_least(self, ar_index):
        """
        When the 'combo_at_least' changes, some widgets should be locked (or not) depending on the combo selection.
        @return:
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.changed_combo_at_least')

        current_selection = self.combo_at_least.currentText()

        # In some cases, enable associated combos.
        if current_selection in ['At least', 'At maximum']:
            self.spin_number.setEnabled(True)
            # self.combo_time_scale.setEnabled(True)
            self.combo_when.setEnabled(True)
        # In other cases, disable irrelevant combos.
        elif current_selection in ['At the same time']:
            self.spin_number.setEnabled(False)
            # self.combo_time_scale.setEnabled(False)
            self.combo_when.setEnabled(False)
        # Uups.
        else:
            sonet_log(SonetLogType.WARNING, 'SonetPCPFilterQt.changed_combo_at_least."Not supposed to arrive here"')

    def changed_cb_departure_dates_step1(self):
        """
        Slot which enables or disables the departure/arrival dates group box top combos,
        depending on the checkbox state.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.changed_cb_departure_dates_step1')

        # The three combos share the same state.
        enable = self.cb_dep_arriv_dates.isChecked()
        self.enable_departure_dates_step1_combos(enable)
        self.cb_dates_1.setEnabled(enable)
        self.cb_dates_2.setEnabled(enable)

        # In case the checkboxes were checked, if we are disabling them, we should also uncheck them.
        if not enable:
            self.cb_dates_1.setChecked(False)
            self.cb_dates_2.setChecked(False)

        # Force combo_planet to be updated based on the combo_dept_arriv and combo select_trip values.
        # self.combo_dept_arriv.currentIndexChanged.emit
        # A la desesperada.
        self.combo_dept_arriv.setCurrentIndex(0)
        self.combo_dept_arriv.setCurrentIndex(1)
        self.combo_dept_arriv.setCurrentIndex(0)

    def changed_cb_departure_dates_step2(self):
        """
        Method executed whenever the check box cb_dates_1 is toggled.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.changed_cb_departure_dates_step2 (left dep/arriv dates)')

        enable = self.cb_dates_1.isChecked()

        self.combo_at_least.setEnabled(enable)
        self.spin_number.setEnabled(enable)
        self.combo_when.setEnabled(enable)
        self.radio_mission.setEnabled(enable)
        self.radio_spacecraft.setEnabled(enable)
        self.combo_select_spacecraft.setEnabled(enable)
        self.combo_select_trip.setEnabled(enable)
        self.combo_event.setEnabled(enable)

        # Only allow one checkbox checked at a time (cb_dates1 and cb_dates2)
        if self.cb_dep_arriv_dates.isChecked():
            self.cb_dates_2.setEnabled(not enable)

    def changed_cb_departure_dates_step3(self):
        """
        Method executed whenever the check box cb_dates_2 is toggled.
        """

        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.changed_cb_departure_dates_step3 (right dep/arriv dates)')

        enable = self.cb_dates_2.isChecked()

        self.combo_when_2.setEnabled(enable)
        self.dateEdit.setEnabled(enable)

        # Only allow one checkbox checked at a time (cb_dates1 and cb_dates2)
        if self.cb_dep_arriv_dates.isChecked():
            self.cb_dates_1.setEnabled(not enable)

    def changed_cb_energy(self):
        """
        Slot which enables or disables the energy group box combos, depending on the energy group box checkbox state.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.changed_cb_energy')

        cb = self.cb_energy
        if cb.isChecked():
            self.enable_energy_combos(True)
        else:
            self.enable_energy_combos(False)

    def changed_cb_time_of_flight(self):
        """
        Slot which enables or disables the time of flight group box combos, depending on the time of flight group box
        checkbox state.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.changed_cb_time_of_flight')

        self.enable_time_of_flight_combos(self.cb_time_of_flight.isChecked())

    def clicked_pb_accept(self):
        """
        When clicked the 'Accept' btn, we retrieve and store the filters for each s/c. Only the ones modified are
        stored, so the s/c's with unmodified filters won't suffer any change.
        Each time a filter is modified, the affected s/c resets its selected trajectory/ies.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.clicked_pb_accept')

        # Traverse all the s/c and update their filters.
        sc: SonetSpacecraft
        for sc in database.get_spacecrafts_list(p_return_objects=True):
            # Set the current filter.
            the_dataframe = self._dict_filters_current.get(sc.get_spacecraft_name())
            sc.set_filter(the_dataframe, p_dataframe=True)

            # Add dependencies, if the current filter generates them.
            dependencies_list = sc.get_filter_dependencies(the_dataframe)
            for sc_name in dependencies_list:
                sc.add_dependency(sc_name)

    def clicked_pb_cancel(self):
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.clicked_pb_cancel')
        pass

    def clicked_pb_add(self):
        """
        Travers the applied filters, gets their data, and add it to the spacecraft private members.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.clicked_pb_add')

        # Get the checked filters.
        list_checked_cb = self.which_cb_checked()

        # If no filter checked, return.
        if not list_checked_cb:
            self.status_bar.showMessage('No check box enabled')
            return False
        else:
            # Python's switch-case.
            switcher = \
                {
                    'cb_energy': self.get_energy_combos_selection,
                    'cb_time_of_flight': self.get_time_of_flight_combos_selection,
                    'cb_dep_arriv_dates+0': 'Invalid selection',
                    'cb_dep_arriv_dates+1': self.get_dep_arriv_dates_combos_selection,
                    'cb_dep_arriv_dates+2': self.get_dep_arriv_dates_combos_selection
                }

            # Check 1 - If the checkbox 'cb_dep_arriv_dates' is checked,
            # then also 'cb_dates_1' or 'cb_dates_2' should be also checked.
            if not self.dates_combos_check1():
                return False

            # Check 2 - If complex dates filter activated, depending on the radio btn selected,
            # all relevant combos should have valid selection.
            if 'cb_dep_arriv_dates+1' in list_checked_cb:
                if not self.dates_combos_check2():
                    return False

            # Get the spacecraft's filter.
            spc, trip = self.get_current_selection()
            the_sc = database.get_spacecraft(spc)
            has_return_trajectory = the_sc.get_has_return_trajectory()

            # the_filter_data can be a dataframe or a list of them.
            # If has_return_trajectory is true, then I should get the dataframe from a list (because a spacecraft with
            # both out and inc trip, has one dataframe for each trip), otherwise the_filter_data
            # is a dataframe.
            for cb in list_checked_cb:
                # Get the combos selection, to be added to the spacecraft's filter.
                the_new_row = \
                    switcher.get(cb, 'Not found')()

                if the_new_row == 'Not found':
                    sonet_log(SonetLogType.ERROR, 'SonetPCPFilterQt.clicked_pb_add."Argument not present in switcher"')
                    return False

                # Add it as a new row into the selected spacecraft and trip dataframe.
                # Note: it's not efficient to use append every time you add a row to a dataframe, but it's not a problem
                # for our particular case.
                if has_return_trajectory:
                    self._dict_filters_current[spc][TripType.get_index(trip)] = \
                        self._dict_filters_current[spc][TripType.get_index(trip)].append(
                            the_new_row, ignore_index=True)
                else:
                    self._dict_filters_current[spc] = \
                        self._dict_filters_current[spc].append(the_new_row, ignore_index=True)

            # After modifying the filter data of the selected spacecraft and trip, we update the
            # table model to let the user inspect the currently applied filters.
            self.update_table_model()

            # Reset the filters. Once you apply a filter, you probably won't apply the same filter again, so reset them.
            self.clicked_pb_reset()
            return True

    def clicked_pb_delete(self):
        """
        Github issue [#].
        Slot executed whenclicking over 'Delete' QPushButton. It's main function is to delete the current selected
        filter of a given spacecraft and trip.

        :return: bool
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.clicked_pb_delete')

        # Get the current selected spacecraft and trip.
        spc, trip = self.get_current_selection()
        the_spacecraft = database.get_spacecraft(spc)
        has_return_trajectory = the_spacecraft.get_has_return_trajectory()
        current_row = self.applied_filters_table_view.currentIndex().row()

        # Remove the current row from the filter data (which can be a dataframe, or a list of them, if the spc has two
        # trips).
        try:
            if has_return_trajectory:
                self._dict_filters_current[spc][TripType.get_index(trip)] = \
                    self._dict_filters_current[spc][TripType.get_index(trip)].drop(current_row).reset_index(drop=True)
            else:
                self._dict_filters_current[spc] = self._dict_filters_current[spc] \
                    .drop(current_row).reset_index(drop=True)
            #     The reset_index method is used to reset the resulting dataframe index, to avoid weird index numbers
            # after deleting a row in the middle (e.g. 0,2,3...)

            # After modifying the filter data of the selected spacecraft and trip, we update the
            # table model to let the user inspect the currently applied filters.
            self.update_table_model()
            return True

        except KeyError:
            # Sometimes (not deterministically), when the user does a weird selection, KeyError is raised.
            # In those cases, then just do nothing and return False, to show that sth went wrong.
            sonet_log(SonetLogType.WARNING, 'SonetPCPFilterQt.clicked_pb_delete."KeyError exception raised"')
            return False

    def clicked_pb_delete_all(self):
        """
        Github issue [#18].
        Slot executed when clicking over 'Delete all' QPushButton. It's main function is to delete all the filters
        (e.g. reset the filter) of a given spacecraft and trip.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.clicked_pb_delete_all')

        # Get the current selected spacecraft and trip.
        spc, trip = self.get_current_selection()
        the_spacecraft = database.get_spacecraft(spc)
        has_return_trajectory = the_spacecraft.get_has_return_trajectory()

        # Get the dataframe columns, to reset the dataframe. Forma un poco guarra de sacar las columnas.
        try:
            cols = self._dict_filters_current.get(spc).columns
        except AttributeError:
            cols = self._dict_filters_current.get(spc)[0].columns

        # Reset the filter data (which can be a dataframe, or a list of them, if the spc has two trips).
        if has_return_trajectory:
            self._dict_filters_current[spc][TripType.get_index(trip)] = pd.DataFrame(columns=cols)
        else:
            self._dict_filters_current[spc] = pd.DataFrame(columns=cols)

        # After modifying the filter data of the selected spacecraft and trip, we update the
        # table model to let the user inspect the currently applied filters.
        self.update_table_model()

    def clicked_pb_reset(self):
        """
        Restores the widgets to their original values.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.clicked_pb_reset')

        self.reset_filter_energy()
        self.reset_filter_time_of_flight()
        self.reset_filter_departure_dates_step1()
        self.reset_filter_departure_dates_left()
        self.reset_filter_departure_dates_right()

    def clicked_radio_mission(self):
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.clicked_radio_mission')

        # Fill combo_select_spacecraft.
        self.fill_dates_combo_select_spacecraft(p_config_for='Missions')

        # Fill combo_event.
        self.fill_dates_combo_event(p_config_for='Missions')

    def clicked_radio_spacecraft(self):
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.clicked_radio_spacecraft')

        # Fill combo_select_spacecraft.
        self.fill_dates_combo_select_spacecraft(p_config_for='Spacecrafts')

        # Fill combo_event.
        self.fill_dates_combo_event(p_config_for='Spacecrafts')

    def fill_dates_combo_event(self, p_config_for='Spacecrafts'):
        """
        Fills the combo_event with the relevant items, depending on the passed p_config_for parameter.
            p_config_for='[Spacecrafts'|'Missions'].
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.fill_dates_combo_event."(' + p_config_for + ')"')

        self.combo_event.clear()

        items = []
        if p_config_for == 'Spacecrafts':
            items = ['Launching', 'Landing']
        if p_config_for == 'Missions':
            pass

        self.combo_event.addItems(items)

    def fill_dates_combo_select_spacecraft(self, p_config_for='Spacecrafts'):
        """
        Fills the combo_select_spacecraft with the available missions or s/c's,
        depending on the passed p_config_for parameter.
            p_config_for='Spacecrafts' for filling the combo with s/c's.
            p_config_for='Missions' for filling the combo with missions.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.fill_dates_combo_select_spacecraft."(' + p_config_for + ')"')

        self.combo_select_spacecraft.clear()
        self.combo_select_trip.clear()

        if p_config_for == 'Spacecrafts':
            # Fill the combo with the available s/c with at least one trajectory selected in the main window.
            items = ['Select s/c']
            items.extend(self.get_spacecrafts_with_selected_trajectories(return_type='String'))
            self.combo_select_spacecraft.addItems(items)

        if p_config_for == 'Missions':
            pass

    def fill_dates_combo_select_trip(self, ar_the_sc: str):
        """
        Fills the combo_select_trip with the available trips (the ones with a trajectory selected)
        for a given ar_the_sc spacecraft.
        """
        sonet_log(SonetLogType.INFO, 'SonetPCPFilterQt.fill_dates_combo_select_trip')

        if ar_the_sc in ['Select s/c', '']:
            self.combo_select_trip.clear()
            return

        # Get the s/c.
        sc = database.get_spacecraft(ar_the_sc)

        # Get their available trips (the ones with a trajectory selected).
        items = sc.get_trajectory_selected()

        # Fill the combo.
        self.combo_select_trip.clear()
        self.combo_select_trip.addItems(items)

    def which_radio_toggled(self):
        """
        Returns:
            'Mission' if radio_mission is toggled.
            'Spacecraft' if radio_spacecraft is toggled.
            None object if none of them is toggled.
        """
        if self.radio_mission.isChecked():
            return 'Mission'
        elif self.radio_spacecraft.isChecked():
            return 'Spacecraft'
        else:
            return None


class SonetAppliedFiltersTableModel(QAbstractTableModel):
    """
    Table model for the applied filters QTableView. Only two columns:
    Col 1: Status - Checkbox to enable/disable the filter.
    Col 2: Filter type - Energy, Time of flight, Dates.
    Col 3: Filter - String describing the filter, if several filters were applied, each one will be splitted in a row.
    """

    def __init__(self, parent=None):
        super(SonetAppliedFiltersTableModel, self).__init__(parent)
        self._data = pd.DataFrame(columns=['Status', 'Type', 'Filter'])  # pd.DataFrame()  # A Pandas dataframe

        # Draft
        # new_row = {'Status': 1, 'Type': FilterType.ENERGY, 'Filter': 'filter1'}
        # self._data = self._data.append(new_row, ignore_index=True)
        # self._data = self._data.append(new_row, ignore_index=True)

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        if self._data is None:
            return 0
        return self._data.shape[0]  # Number of rows of the dataframe

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        if self._data is None:
            return 0
        return self._data.shape[1]  # Number of columns of the dataframe

    def data(self, index=QModelIndex, role=None):
        if not index.isValid():
            return None

        row = index.row()
        column = index.column()

        if role == Qt.DisplayRole:
            # Get the raw value
            value = self._data.iloc[row, column]

            # Perform per-type checks and render accordingly.
            if isinstance(value, float):
                # Render float to 2 dp
                return "%.2f" % value
            if isinstance(value, str):
                # Render strings with quotes
                return '%s' % value
            if isinstance(FilterType.ENERGY, FilterType):
                # Render own enums as strings
                return '%s' % value
            # Default (anything not captured above: e.g. int)
            return value

        if role == Qt.BackgroundRole:
            pass
            # Pair rows will have different color, to visually distinguish them from the even ones.
            # if row % 2 is not 0:
            # return QColor(255, 230, 255)
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

    def update_model(self, ar_dict_filters_current, ar_spc_selection, ar_trip_selection):
        """
        Reset the table model.
        index == 1 -> Earth - Mars trip
        index == 2 -> Mars - Earth trip
        """
        sonet_log(SonetLogType.INFO, 'SonetAppliedFiltersTableModel.update_model')

        # If no valid selection, then we just reset the table model.
        if ar_spc_selection not in list(ar_dict_filters_current.keys()) or not TripType.is_valid(
                TripType.convert_to_enum(ar_trip_selection)):
            self.beginResetModel()
            self._data = pd.DataFrame(columns=['Status', 'Type', 'Filter'])
            self.endResetModel()
            return False

        # Get the filter
        the_filter_data = ar_dict_filters_current[ar_spc_selection]  # a dataframe or list of them.
        has_return_trajectory = database.get_spacecraft(ar_spc_selection).get_has_return_trajectory()
        if has_return_trajectory:
            # the_filter_data is not a dataframe, but a list of them, with both the outgoing and incoming
            # trip filter dataframe.
            if ar_trip_selection == 'Earth - Mars':
                the_filter_data = the_filter_data[0]
            elif ar_trip_selection == 'Mars - Earth':
                the_filter_data = the_filter_data[1]
            else:
                sonet_log(SonetLogType.ERROR, 'SonetAppliedFiltersTableModel.update_model')
                return False
        else:
            # the_filter_data is a dataframe, representing the outgoing trip filter.
            pass

        self.beginResetModel()
        self._data = the_filter_data
        self.endResetModel()
        return True


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)  # To avoid AA_ShareOpenGLContexts Qt warning.
    app = QApplication([])
    dialog = SonetPCPFilterQt()
    dialog.show()
    sys.exit(app.exec_())
