import sys

from PySide2.QtCore import QCoreApplication, Qt, QAbstractTableModel, QModelIndex
from PySide2.QtWidgets import QDialog, QApplication, QDialogButtonBox

from src import database
from src import sonet_pcp_filter_qt_ui
from src.sonet_utils import SpacecraftType, SONET_DEBUG


class sonet_pcp_filter_qt(QDialog, sonet_pcp_filter_qt_ui.Ui_sonet_pcp_filter):
    def __init__(self, *args, ar_list_spacecrafts=[], ar_current_index=-1):
        super(sonet_pcp_filter_qt, self).__init__(*args)  # , **kwargs)
        self.setupUi(self)
        self.init(ar_list_spacecrafts, ar_current_index)

        # Draft
        self._applied_filters_table_model = sonet_applied_filters_TableModel()
        self.applied_filters_table_view.setModel(self._applied_filters_table_model)

    def init(self, ar_list_spacecrafts=[], ar_current_index=-1):
        """
        Initializes the this QDialog window. It does the signal/slot connections.
        :param ar_list_spacecrafts:
        :param ar_current_index:
        :return:
        """
        # Connect signals and slots.
        self.btn_accept = self.dialog_button_box.button(QDialogButtonBox.Ok)
        self.btn_accept.clicked.connect(self.accept)

        self.btn_cancel = self.dialog_button_box.button(QDialogButtonBox.Cancel)
        self.btn_cancel.clicked.connect(self.reject)

        self.pb_add.clicked.connect(self.clicked_pb_add)
        self.pb_reset.clicked.connect(self.clicked_pb_reset)

        self.select_spacecraft.currentIndexChanged.connect(self.changed_cmb_select_spacecraft)
        self.select_trip.currentIndexChanged.connect(self.changed_cmb_select_trip)
        self.combo_energy_parameter.currentIndexChanged.connect(self.changed_cmb_energy_parameter)

        self.cb_energy.stateChanged.connect(self.enable_pb_add)
        self.cb_energy.stateChanged.connect(self.changed_cb_energy)

        # Fill select_spacecraft combo with the available spacecrafts and select the current one.
        self.init_combo_select_spacecraft(ar_list_spacecrafts, ar_current_index)

    def init_combo_select_spacecraft(self, ar_list_spacecrafts=[], ar_current_index=-1):
        """
        Fill select_spacecraft combo box with the available spacecrafts.
        And select the one selected by the user.
        If no selection (ar_current_index = -1, then 0 should be selected, which tells
        the user that it has to do a selection.
        :param ar_list_spacecrafts:
        :param ar_current_index:
        :return:
        """
        self.select_spacecraft.addItems(ar_list_spacecrafts)
        if ar_current_index is not -1:
            self.select_spacecraft.setCurrentIndex(ar_current_index + 1)  # The '+1' is because the combo box is already
            # populated with 'Select spacecraft...' item when the above addItems() is executed.
        else:
            self.select_spacecraft.setCurrentIndex(0)

    def enable_pb_add(self):
        """
        If no checkbox is checked, then disable the 'Add' push button, otherwise it should remain enabled.
        """
        any_checked = self.is_any_cb_checked()

        if SONET_DEBUG:
            if any_checked:
                print('At least one checkbox is checked, "Add" button is enabled.')
            else:
                print('No checkbox is checked, "Add" button is disabled.')

        if any_checked:
            self.pb_add.setEnabled(True)
        else:
            self.pb_add.setEnabled(False)

        return True

    def enable_combos(self, ar_activate):
        """
        Activates the group box combos if a valid spacecraft and trip are selected.
        :param ar_activate: bool flag.
        :return: bool 0 if no errors, 1 otherwise.
        """
        self.enable_groupbox_energy(ar_activate)
        return 0

    def enable_energy_combos(self, ar_enable):
        self.combo_energy_parameter.setEnabled(ar_enable)
        self.combo_energy_operator.setEnabled(ar_enable)
        self.spin_energy_number.setEnabled(ar_enable)

    def enable_groupbox_energy(self, ar_activate):
        self.energy_group_box.setEnabled(ar_activate)
        if ar_activate is False:
            self.cb_energy.setChecked(False)
        self.cb_energy.setEnabled(ar_activate)

    def get_filter_data_energy(self):
        """
        Retrieves the energy combo boxes data, to apply filters.
        :return:
        """
        if SONET_DEBUG:
            print('get_filter_data_energy() called.')

        the_selection = [self.combo_energy_parameter.currentText(),
                         self.combo_energy_operator.currentText(),
                         self.spin_energy_number.text(),
                         self.combo_energy_units.currentText()]
        print(the_selection)

    def reset_filter_energy(self):
        """
        Disables the energy filter checkbox and resets all the fields to their default value.
        :return:
        """
        if SONET_DEBUG:
            print('reset_filter_energy()')

        self.cb_energy.setChecked(False)
        self.combo_energy_parameter.setCurrentIndex(0)
        self.combo_energy_operator.setCurrentIndex(0)
        # self.spin_energy_number.clear()
        self.spin_energy_number.setValue(0)

    def is_any_cb_checked(self):
        """
        Checks if any of the filter checkboxes is checked.
        If at least one is checked, then returns true, otherwise false.
        :return: bool
        """
        any_checked = any([self.cb_time_of_flight.isChecked(),
                           self.cb_time_of_flight_2.isChecked(),
                           self.cb_dates_1.isChecked(),
                           self.cb_dates_2.isChecked(),
                           self.cb_energy.isChecked()])
        if any_checked:
            return True
        else:
            return False

    def is_selection_valid(self):
        c1 = self.select_spacecraft.currentText() == 'Select spacecraft'
        c2 = self.select_trip.currentText() == 'Select trip'
        if not c1 and not c2:
            print('Selection is valid.')
            return True
        else:
            print("Selection isn't valid.")
            # print(self.select_trip.currentText())
            return False

    def which_cb_checked(self):
        """
        Traverses the QDialog window to check which checkboxes are checked. It returns a list with the checked
        checkboxes. If no checkbox is checked, it returns and empty list.
        :return: list
        """
        if SONET_DEBUG:
            print('which_cb_checked() called.')

        any_checked = self.is_any_cb_checked()
        the_list = []

        if any_checked:
            if self.cb_energy.isChecked():
                the_list.append('cb_energy')
            if self.cb_time_of_flight.isChecked():
                the_list.append('cb_time_of_flight')
            if self.cb_time_of_flight_2.isChecked():
                the_list.append('cb_time_of_flight_2')
            if self.cb_dates_1.isChecked():
                the_list.append('cb_dates_1')
            if self.cb_dates_2.isChecked():
                the_list.append('cb_dates_2')

        if SONET_DEBUG:
            print(the_list)

        return the_list

    def changed_cmb_select_spacecraft(self, index):
        """
        Triggered when the select_spacecraft combo box index changes.

        Updates the 'Select trip' combo box every time the 'Select spacecraft' changes.
        If the spacecraft is crewed, then it will have both outgoing and incoming trips.
        If the spacecraft is cargo, then it will have only outgoing trip.
        Each trip is represented by a Pandas dataframe.
        :param index:
        :return:
        """
        # print('Slot cmb_select_spacecraft_changed() called.')

        # Retrieve the selected spacecraft.
        selected_spacecraft = self.select_spacecraft.itemText(index)

        # Get the spacecraft type.
        if selected_spacecraft == 'Select spacecraft':
            self.select_trip.clear()
            self.select_trip.addItems(['Select trip'])
            return True
        else:
            spacecraft_type = database.db[selected_spacecraft].getSpacecraftType()

            if spacecraft_type == SpacecraftType.CREWED:
                items = ['Select trip', 'Earth - Mars', 'Mars - Earth']
            elif spacecraft_type == SpacecraftType.CARGO:
                items = ['Select trip', 'Earth - Mars']
            else:
                return False

            self.select_trip.clear()
            self.select_trip.addItems(items)
            return True

    def changed_cmb_select_trip(self, index):
        """
        Triggered when the select_trip combo box index changes.

        Only once both combo boxes (select_spacecraft, and select_trip) are valid, then we will be able
        to work with a specific table (outgoing or incoming). Once the selection is valid, we'll enable the
        different filtering options combo boxes (i.e. by trajectory energy, by time of flight, etc.).
        """
        selection_is_valid = self.is_selection_valid()

        if selection_is_valid:
            self.enable_combos(True)
        elif not selection_is_valid:
            self.enable_combos(False)

    def changed_cmb_energy_parameter(self, index):
        cmb_units = self.combo_energy_units

        if index in [0, 1, 2]:
            # km/s
            cmb_units.setCurrentIndex(0)
            return 0
        elif index in [3, 4]:
            # km2/s2
            cmb_units.setCurrentIndex(1)
            return 0
        elif index in [5]:
            # º
            cmb_units.setCurrentIndex(2)
            return 0
        else:
            print('Warning: cmb_energy_parameter_changed()')

    def changed_cb_energy(self):
        cb = self.cb_energy
        if cb.isChecked():
            self.enable_energy_combos(True)
        else:
            self.enable_energy_combos(False)

    def clicked_pb_reset(self):
        self.reset_filter_energy()

        # Pending implementation
        # self.reset_filter_time_of_flight()
        # self.reset_filter_time_of_flight_2()
        # self.reset.filter_dates()

    def clicked_pb_add(self):
        """
        Traverses all the checked filters and adds them to the filters table.
        """
        if SONET_DEBUG:
            print('pb_add_clicked()')

        list_checked_cb = self.which_cb_checked()

        if len(list_checked_cb) == 0:
            if SONET_DEBUG:
                print('Empty list: list_checked_cb.')
            return True
        else:
            # The switcher implementation is an efficient alternative to multiple if statements, as it
            # only checks one time each variable. E.g. it can be seen as a sort of switch-case clause, from c++.

            switcher = {
                'cb_energy': self.get_filter_data_energy(),
                'cb_time_of_flight': 'Pending implementation',
                'cb_time_of_flight_2': 'Pending implementation',
                'cb_dates_1': 'Pending implementation',
                'cb_dates_2': 'Pending implementation',
            }

            for cb in list_checked_cb:
                switcher.get(cb, 'Error in clicked_pb_add()')

    def clicked_pb_delete(self):
        pass

    def clicked_pb_delete_all(self):
        pass


class sonet_applied_filters_TableModel(QAbstractTableModel):
    """
    Table model for the applied filters QTableView. Only two columns:
    Column 1: Checkbox to enable/disable the filter.
    Column 2: String describing the filter, if several filters were applied it displays them with the format [filter1]
    AND [filter2] AND [filterN].
    """

    def __init__(self, pcp_table='', parent=None):
        pass

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        pass

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        pass

    def data(self, index=QModelIndex, role=None):
        pass

    def headerData(self, section, orientation, role):
        pass

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)  # To avoid AA_ShareOpenGLContexts Qt warning.
    app = QApplication([])
    dialog = sonet_pcp_filter_qt()
    dialog.show()
    sys.exit(app.exec_())
