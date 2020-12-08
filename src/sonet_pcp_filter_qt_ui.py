# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sonet_pcp_filter_qt.ui',
# licensing of 'sonet_pcp_filter_qt.ui' applies.
#
# Created: Tue Dec  8 10:52:22 2020
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_sonet_pcp_filter(object):
    def setupUi(self, sonet_pcp_filter):
        sonet_pcp_filter.setObjectName("sonet_pcp_filter")
        sonet_pcp_filter.setEnabled(True)
        sonet_pcp_filter.resize(770, 707)
        self.gridLayout = QtWidgets.QGridLayout(sonet_pcp_filter)
        self.gridLayout.setObjectName("gridLayout")
        self.bottom_group_box = QtWidgets.QGroupBox(sonet_pcp_filter)
        self.bottom_group_box.setEnabled(False)
        self.bottom_group_box.setObjectName("bottom_group_box")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.bottom_group_box)
        self.verticalLayout.setObjectName("verticalLayout")
        self.bottom_grid_layout = QtWidgets.QGridLayout()
        self.bottom_grid_layout.setObjectName("bottom_grid_layout")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.pb_delete = QtWidgets.QPushButton(self.bottom_group_box)
        self.pb_delete.setEnabled(False)
        self.pb_delete.setObjectName("pb_delete")
        self.horizontalLayout_14.addWidget(self.pb_delete)
        self.pb_delete_all = QtWidgets.QPushButton(self.bottom_group_box)
        self.pb_delete_all.setEnabled(False)
        self.pb_delete_all.setObjectName("pb_delete_all")
        self.horizontalLayout_14.addWidget(self.pb_delete_all)
        self.bottom_grid_layout.addLayout(self.horizontalLayout_14, 1, 0, 1, 1)
        self.applied_filters_table_view = QtWidgets.QTableView(self.bottom_group_box)
        self.applied_filters_table_view.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.applied_filters_table_view.sizePolicy().hasHeightForWidth())
        self.applied_filters_table_view.setSizePolicy(sizePolicy)
        self.applied_filters_table_view.setMinimumSize(QtCore.QSize(100, 0))
        self.applied_filters_table_view.setAlternatingRowColors(True)
        self.applied_filters_table_view.setObjectName("applied_filters_table_view")
        self.bottom_grid_layout.addWidget(self.applied_filters_table_view, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.bottom_grid_layout)
        self.gridLayout.addWidget(self.bottom_group_box, 17, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 10, 0, 1, 1)
        self.dialog_button_box = QtWidgets.QDialogButtonBox(sonet_pcp_filter)
        self.dialog_button_box.setEnabled(True)
        self.dialog_button_box.setCursor(QtCore.Qt.PointingHandCursor)
        self.dialog_button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.dialog_button_box.setObjectName("dialog_button_box")
        self.gridLayout.addWidget(self.dialog_button_box, 18, 1, 1, 1)
        self.select_spacecraft = QtWidgets.QComboBox(sonet_pcp_filter)
        self.select_spacecraft.setEnabled(True)
        self.select_spacecraft.setObjectName("select_spacecraft")
        self.select_spacecraft.addItem("")
        self.gridLayout.addWidget(self.select_spacecraft, 0, 0, 1, 2)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.pb_reset = QtWidgets.QPushButton(sonet_pcp_filter)
        self.pb_reset.setEnabled(True)
        self.pb_reset.setObjectName("pb_reset")
        self.horizontalLayout_9.addWidget(self.pb_reset)
        self.pb_add = QtWidgets.QPushButton(sonet_pcp_filter)
        self.pb_add.setEnabled(False)
        self.pb_add.setObjectName("pb_add")
        self.horizontalLayout_9.addWidget(self.pb_add)
        self.gridLayout.addLayout(self.horizontalLayout_9, 8, 0, 2, 2)
        self.top_grid_layout = QtWidgets.QGridLayout()
        self.top_grid_layout.setObjectName("top_grid_layout")
        self.time_of_flight_group_box = QtWidgets.QGroupBox(sonet_pcp_filter)
        self.time_of_flight_group_box.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time_of_flight_group_box.sizePolicy().hasHeightForWidth())
        self.time_of_flight_group_box.setSizePolicy(sizePolicy)
        self.time_of_flight_group_box.setObjectName("time_of_flight_group_box")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.time_of_flight_group_box)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.time_of_flight_grid_layout = QtWidgets.QGridLayout()
        self.time_of_flight_grid_layout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.time_of_flight_grid_layout.setObjectName("time_of_flight_grid_layout")
        self.combo_time_of_flight = QtWidgets.QComboBox(self.time_of_flight_group_box)
        self.combo_time_of_flight.setEnabled(False)
        self.combo_time_of_flight.setObjectName("combo_time_of_flight")
        self.combo_time_of_flight.addItem("")
        self.time_of_flight_grid_layout.addWidget(self.combo_time_of_flight, 0, 0, 1, 2)
        self.combo_time_of_flight_operator = QtWidgets.QComboBox(self.time_of_flight_group_box)
        self.combo_time_of_flight_operator.setEnabled(False)
        self.combo_time_of_flight_operator.setObjectName("combo_time_of_flight_operator")
        self.combo_time_of_flight_operator.addItem("")
        self.combo_time_of_flight_operator.addItem("")
        self.time_of_flight_grid_layout.addWidget(self.combo_time_of_flight_operator, 1, 0, 1, 2)
        self.spin_number_2 = QtWidgets.QSpinBox(self.time_of_flight_group_box)
        self.spin_number_2.setEnabled(False)
        self.spin_number_2.setMaximum(10000)
        self.spin_number_2.setObjectName("spin_number_2")
        self.time_of_flight_grid_layout.addWidget(self.spin_number_2, 3, 0, 1, 1)
        self.combo_time_scale_2 = QtWidgets.QComboBox(self.time_of_flight_group_box)
        self.combo_time_scale_2.setEnabled(False)
        self.combo_time_scale_2.setObjectName("combo_time_scale_2")
        self.combo_time_scale_2.addItem("")
        self.combo_time_scale_2.addItem("")
        self.combo_time_scale_2.addItem("")
        self.combo_time_scale_2.addItem("")
        self.time_of_flight_grid_layout.addWidget(self.combo_time_scale_2, 3, 1, 1, 1)
        self.time_of_flight_grid_layout.setRowStretch(0, 10)
        self.gridLayout_5.addLayout(self.time_of_flight_grid_layout, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem2, 2, 0, 1, 1)
        self.cb_time_of_flight = QtWidgets.QCheckBox(self.time_of_flight_group_box)
        self.cb_time_of_flight.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_time_of_flight.sizePolicy().hasHeightForWidth())
        self.cb_time_of_flight.setSizePolicy(sizePolicy)
        self.cb_time_of_flight.setText("")
        self.cb_time_of_flight.setObjectName("cb_time_of_flight")
        self.gridLayout_5.addWidget(self.cb_time_of_flight, 0, 0, 1, 1)
        self.top_grid_layout.addWidget(self.time_of_flight_group_box, 1, 2, 1, 1)
        self.energy_group_box = QtWidgets.QGroupBox(sonet_pcp_filter)
        self.energy_group_box.setEnabled(False)
        self.energy_group_box.setObjectName("energy_group_box")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.energy_group_box)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cb_energy = QtWidgets.QCheckBox(self.energy_group_box)
        self.cb_energy.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_energy.sizePolicy().hasHeightForWidth())
        self.cb_energy.setSizePolicy(sizePolicy)
        self.cb_energy.setText("")
        self.cb_energy.setObjectName("cb_energy")
        self.horizontalLayout_2.addWidget(self.cb_energy)
        self.energy_grid_layout = QtWidgets.QGridLayout()
        self.energy_grid_layout.setObjectName("energy_grid_layout")
        self.spin_energy_number = QtWidgets.QSpinBox(self.energy_group_box)
        self.spin_energy_number.setEnabled(False)
        self.spin_energy_number.setMaximum(10000)
        self.spin_energy_number.setObjectName("spin_energy_number")
        self.energy_grid_layout.addWidget(self.spin_energy_number, 1, 2, 1, 1)
        self.combo_energy_parameter = QtWidgets.QComboBox(self.energy_group_box)
        self.combo_energy_parameter.setEnabled(False)
        self.combo_energy_parameter.setObjectName("combo_energy_parameter")
        self.combo_energy_parameter.addItem("")
        self.combo_energy_parameter.addItem("")
        self.combo_energy_parameter.addItem("")
        self.combo_energy_parameter.addItem("")
        self.combo_energy_parameter.addItem("")
        self.combo_energy_parameter.addItem("")
        self.energy_grid_layout.addWidget(self.combo_energy_parameter, 1, 0, 1, 1)
        self.combo_energy_operator = QtWidgets.QComboBox(self.energy_group_box)
        self.combo_energy_operator.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_energy_operator.sizePolicy().hasHeightForWidth())
        self.combo_energy_operator.setSizePolicy(sizePolicy)
        self.combo_energy_operator.setMinimumSize(QtCore.QSize(0, 0))
        self.combo_energy_operator.setObjectName("combo_energy_operator")
        self.combo_energy_operator.addItem("")
        self.combo_energy_operator.addItem("")
        self.energy_grid_layout.addWidget(self.combo_energy_operator, 1, 1, 1, 1)
        self.combo_energy_units = QtWidgets.QComboBox(self.energy_group_box)
        self.combo_energy_units.setEnabled(False)
        self.combo_energy_units.setObjectName("combo_energy_units")
        self.combo_energy_units.addItem("")
        self.combo_energy_units.addItem("")
        self.combo_energy_units.addItem("")
        self.energy_grid_layout.addWidget(self.combo_energy_units, 1, 3, 1, 1)
        self.horizontalLayout_2.addLayout(self.energy_grid_layout)
        self.top_grid_layout.addWidget(self.energy_group_box, 2, 2, 1, 1)
        self.top_left_group_box = QtWidgets.QGroupBox(sonet_pcp_filter)
        self.top_left_group_box.setEnabled(False)
        self.top_left_group_box.setObjectName("top_left_group_box")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.top_left_group_box)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.cb_dep_arriv_dates = QtWidgets.QCheckBox(self.top_left_group_box)
        self.cb_dep_arriv_dates.setEnabled(False)
        self.cb_dep_arriv_dates.setText("")
        self.cb_dep_arriv_dates.setObjectName("cb_dep_arriv_dates")
        self.verticalLayout_11.addWidget(self.cb_dep_arriv_dates)
        self.combo_dept_arriv = QtWidgets.QComboBox(self.top_left_group_box)
        self.combo_dept_arriv.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_dept_arriv.sizePolicy().hasHeightForWidth())
        self.combo_dept_arriv.setSizePolicy(sizePolicy)
        self.combo_dept_arriv.setObjectName("combo_dept_arriv")
        self.combo_dept_arriv.addItem("")
        self.combo_dept_arriv.addItem("")
        self.verticalLayout_11.addWidget(self.combo_dept_arriv)
        self.combo_planet = QtWidgets.QComboBox(self.top_left_group_box)
        self.combo_planet.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_planet.sizePolicy().hasHeightForWidth())
        self.combo_planet.setSizePolicy(sizePolicy)
        self.combo_planet.setObjectName("combo_planet")
        self.combo_planet.addItem("")
        self.combo_planet.addItem("")
        self.verticalLayout_11.addWidget(self.combo_planet)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(spacerItem3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.cb_dates_1 = QtWidgets.QCheckBox(self.top_left_group_box)
        self.cb_dates_1.setEnabled(False)
        self.cb_dates_1.setText("")
        self.cb_dates_1.setObjectName("cb_dates_1")
        self.verticalLayout_3.addWidget(self.cb_dates_1)
        self.spin_number = QtWidgets.QSpinBox(self.top_left_group_box)
        self.spin_number.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spin_number.sizePolicy().hasHeightForWidth())
        self.spin_number.setSizePolicy(sizePolicy)
        self.spin_number.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.spin_number.setMaximum(999999)
        self.spin_number.setObjectName("spin_number")
        self.verticalLayout_3.addWidget(self.spin_number)
        self.combo_time_scale = QtWidgets.QComboBox(self.top_left_group_box)
        self.combo_time_scale.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_time_scale.sizePolicy().hasHeightForWidth())
        self.combo_time_scale.setSizePolicy(sizePolicy)
        self.combo_time_scale.setObjectName("combo_time_scale")
        self.combo_time_scale.addItem("")
        self.combo_time_scale.addItem("")
        self.combo_time_scale.addItem("")
        self.combo_time_scale.addItem("")
        self.combo_time_scale.addItem("")
        self.verticalLayout_3.addWidget(self.combo_time_scale)
        self.combo_when = QtWidgets.QComboBox(self.top_left_group_box)
        self.combo_when.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_when.sizePolicy().hasHeightForWidth())
        self.combo_when.setSizePolicy(sizePolicy)
        self.combo_when.setObjectName("combo_when")
        self.combo_when.addItem("")
        self.combo_when.addItem("")
        self.verticalLayout_3.addWidget(self.combo_when)
        self.combo_select_spacecraft = QtWidgets.QComboBox(self.top_left_group_box)
        self.combo_select_spacecraft.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_select_spacecraft.sizePolicy().hasHeightForWidth())
        self.combo_select_spacecraft.setSizePolicy(sizePolicy)
        self.combo_select_spacecraft.setObjectName("combo_select_spacecraft")
        self.combo_select_spacecraft.addItem("")
        self.verticalLayout_3.addWidget(self.combo_select_spacecraft)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem4)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.cb_dates_2 = QtWidgets.QCheckBox(self.top_left_group_box)
        self.cb_dates_2.setEnabled(False)
        self.cb_dates_2.setText("")
        self.cb_dates_2.setObjectName("cb_dates_2")
        self.verticalLayout_7.addWidget(self.cb_dates_2)
        self.combo_when_2 = QtWidgets.QComboBox(self.top_left_group_box)
        self.combo_when_2.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_when_2.sizePolicy().hasHeightForWidth())
        self.combo_when_2.setSizePolicy(sizePolicy)
        self.combo_when_2.setObjectName("combo_when_2")
        self.combo_when_2.addItem("")
        self.combo_when_2.addItem("")
        self.combo_when_2.addItem("")
        self.verticalLayout_7.addWidget(self.combo_when_2)
        self.dateEdit = QtWidgets.QDateEdit(self.top_left_group_box)
        self.dateEdit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEdit.sizePolicy().hasHeightForWidth())
        self.dateEdit.setSizePolicy(sizePolicy)
        self.dateEdit.setObjectName("dateEdit")
        self.verticalLayout_7.addWidget(self.dateEdit)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem5)
        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        self.verticalLayout_11.addLayout(self.horizontalLayout_3)
        self.gridLayout_2.addLayout(self.verticalLayout_11, 0, 0, 1, 1)
        self.top_grid_layout.addWidget(self.top_left_group_box, 1, 1, 2, 1)
        self.gridLayout.addLayout(self.top_grid_layout, 3, 0, 1, 2)
        self.select_trip = QtWidgets.QComboBox(sonet_pcp_filter)
        self.select_trip.setObjectName("select_trip")
        self.gridLayout.addWidget(self.select_trip, 1, 0, 1, 2)

        self.retranslateUi(sonet_pcp_filter)
        QtCore.QObject.connect(self.select_spacecraft, QtCore.SIGNAL("activated(QString)"), self.cb_dep_arriv_dates.show)
        QtCore.QMetaObject.connectSlotsByName(sonet_pcp_filter)

    def retranslateUi(self, sonet_pcp_filter):
        sonet_pcp_filter.setWindowTitle(QtWidgets.QApplication.translate("sonet_pcp_filter", "Apply filter to PCP table", None, -1))
        self.bottom_group_box.setTitle(QtWidgets.QApplication.translate("sonet_pcp_filter", "Applied filters", None, -1))
        self.pb_delete.setText(QtWidgets.QApplication.translate("sonet_pcp_filter", "Delete", None, -1))
        self.pb_delete_all.setText(QtWidgets.QApplication.translate("sonet_pcp_filter", "Delete all", None, -1))
        self.select_spacecraft.setItemText(0, QtWidgets.QApplication.translate("sonet_pcp_filter", "Select spacecraft", None, -1))
        self.pb_reset.setText(QtWidgets.QApplication.translate("sonet_pcp_filter", "Reset", None, -1))
        self.pb_add.setText(QtWidgets.QApplication.translate("sonet_pcp_filter", "Add", None, -1))
        self.time_of_flight_group_box.setTitle(QtWidgets.QApplication.translate("sonet_pcp_filter", "Time of flight", None, -1))
        self.combo_time_of_flight.setItemText(0, QtWidgets.QApplication.translate("sonet_pcp_filter", "Time of flight", None, -1))
        self.combo_time_of_flight_operator.setItemText(0, QtWidgets.QApplication.translate("sonet_pcp_filter", "<=", None, -1))
        self.combo_time_of_flight_operator.setItemText(1, QtWidgets.QApplication.translate("sonet_pcp_filter", ">=", None, -1))
        self.combo_time_scale_2.setItemText(0, QtWidgets.QApplication.translate("sonet_pcp_filter", "Days", None, -1))
        self.combo_time_scale_2.setItemText(1, QtWidgets.QApplication.translate("sonet_pcp_filter", "Weeks", None, -1))
        self.combo_time_scale_2.setItemText(2, QtWidgets.QApplication.translate("sonet_pcp_filter", "Months", None, -1))
        self.combo_time_scale_2.setItemText(3, QtWidgets.QApplication.translate("sonet_pcp_filter", "Years", None, -1))
        self.energy_group_box.setTitle(QtWidgets.QApplication.translate("sonet_pcp_filter", "Energy", None, -1))
        self.combo_energy_parameter.setItemText(0, QtWidgets.QApplication.translate("sonet_pcp_filter", "dvt", None, -1))
        self.combo_energy_parameter.setItemText(1, QtWidgets.QApplication.translate("sonet_pcp_filter", "dvd", None, -1))
        self.combo_energy_parameter.setItemText(2, QtWidgets.QApplication.translate("sonet_pcp_filter", "dva", None, -1))
        self.combo_energy_parameter.setItemText(3, QtWidgets.QApplication.translate("sonet_pcp_filter", "c3d", None, -1))
        self.combo_energy_parameter.setItemText(4, QtWidgets.QApplication.translate("sonet_pcp_filter", "c3a", None, -1))
        self.combo_energy_parameter.setItemText(5, QtWidgets.QApplication.translate("sonet_pcp_filter", "theta", None, -1))
        self.combo_energy_operator.setItemText(0, QtWidgets.QApplication.translate("sonet_pcp_filter", "<=", None, -1))
        self.combo_energy_operator.setItemText(1, QtWidgets.QApplication.translate("sonet_pcp_filter", ">=", None, -1))
        self.combo_energy_units.setItemText(0, QtWidgets.QApplication.translate("sonet_pcp_filter", "km/s", None, -1))
        self.combo_energy_units.setItemText(1, QtWidgets.QApplication.translate("sonet_pcp_filter", "km2/s2", None, -1))
        self.combo_energy_units.setItemText(2, QtWidgets.QApplication.translate("sonet_pcp_filter", "deg", None, -1))
        self.top_left_group_box.setTitle(QtWidgets.QApplication.translate("sonet_pcp_filter", "Departure and arrival dates", None, -1))
        self.combo_dept_arriv.setItemText(0, QtWidgets.QApplication.translate("sonet_pcp_filter", "Departs", None, -1))
        self.combo_dept_arriv.setItemText(1, QtWidgets.QApplication.translate("sonet_pcp_filter", "Arrives", None, -1))
        self.combo_planet.setItemText(0, QtWidgets.QApplication.translate("sonet_pcp_filter", "Earth", None, -1))
        self.combo_planet.setItemText(1, QtWidgets.QApplication.translate("sonet_pcp_filter", "Mars", None, -1))
        self.combo_time_scale.setAccessibleName(QtWidgets.QApplication.translate("sonet_pcp_filter", "accesible", None, -1))
        self.combo_time_scale.setItemText(0, QtWidgets.QApplication.translate("sonet_pcp_filter", "Days", None, -1))
        self.combo_time_scale.setItemText(1, QtWidgets.QApplication.translate("sonet_pcp_filter", "Weeks", None, -1))
        self.combo_time_scale.setItemText(2, QtWidgets.QApplication.translate("sonet_pcp_filter", "Months", None, -1))
        self.combo_time_scale.setItemText(3, QtWidgets.QApplication.translate("sonet_pcp_filter", "Years", None, -1))
        self.combo_time_scale.setItemText(4, QtWidgets.QApplication.translate("sonet_pcp_filter", "Launch opportunities", None, -1))
        self.combo_when.setItemText(0, QtWidgets.QApplication.translate("sonet_pcp_filter", "Before", None, -1))
        self.combo_when.setItemText(1, QtWidgets.QApplication.translate("sonet_pcp_filter", "After", None, -1))
        self.combo_select_spacecraft.setItemText(0, QtWidgets.QApplication.translate("sonet_pcp_filter", "Select spacecraft", None, -1))
        self.combo_when_2.setItemText(0, QtWidgets.QApplication.translate("sonet_pcp_filter", "On", None, -1))
        self.combo_when_2.setItemText(1, QtWidgets.QApplication.translate("sonet_pcp_filter", "Before", None, -1))
        self.combo_when_2.setItemText(2, QtWidgets.QApplication.translate("sonet_pcp_filter", "After", None, -1))

