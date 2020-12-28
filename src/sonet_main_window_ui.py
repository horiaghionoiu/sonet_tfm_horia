# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sonet_main_window.ui',
# licensing of 'sonet_main_window.ui' applies.
#
# Created: Sat Dec 26 11:17:51 2020
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(1350, 650)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(sizePolicy)
        main_window.setMinimumSize(QtCore.QSize(1024, 600))
        main_window.setBaseSize(QtCore.QSize(1024, 960))
        main_window.setTabShape(QtWidgets.QTabWidget.Rounded)
        main_window.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.sonet_mission_tree_qgb = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sonet_mission_tree_qgb.sizePolicy().hasHeightForWidth())
        self.sonet_mission_tree_qgb.setSizePolicy(sizePolicy)
        self.sonet_mission_tree_qgb.setObjectName("sonet_mission_tree_qgb")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.sonet_mission_tree_qgb)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.sonet_mission_tree_qlv = QtWidgets.QListView(self.sonet_mission_tree_qgb)
        self.sonet_mission_tree_qlv.setObjectName("sonet_mission_tree_qlv")
        self.verticalLayout_2.addWidget(self.sonet_mission_tree_qlv)
        self.sonet_add_mission_qpb = QtWidgets.QPushButton(self.sonet_mission_tree_qgb)
        self.sonet_add_mission_qpb.setObjectName("sonet_add_mission_qpb")
        self.verticalLayout_2.addWidget(self.sonet_add_mission_qpb)
        self.sonet_add_spacecraft_qpb = QtWidgets.QPushButton(self.sonet_mission_tree_qgb)
        self.sonet_add_spacecraft_qpb.setObjectName("sonet_add_spacecraft_qpb")
        self.verticalLayout_2.addWidget(self.sonet_add_spacecraft_qpb)
        self.sonet_spacecraft_type_qcmb = QtWidgets.QComboBox(self.sonet_mission_tree_qgb)
        self.sonet_spacecraft_type_qcmb.setObjectName("sonet_spacecraft_type_qcmb")
        self.sonet_spacecraft_type_qcmb.addItem("")
        self.sonet_spacecraft_type_qcmb.addItem("")
        self.verticalLayout_2.addWidget(self.sonet_spacecraft_type_qcmb)
        self.sonet_spacecraft_type_has_return_trajectory_qcmb = QtWidgets.QComboBox(self.sonet_mission_tree_qgb)
        self.sonet_spacecraft_type_has_return_trajectory_qcmb.setObjectName("sonet_spacecraft_type_has_return_trajectory_qcmb")
        self.sonet_spacecraft_type_has_return_trajectory_qcmb.addItem("")
        self.sonet_spacecraft_type_has_return_trajectory_qcmb.addItem("")
        self.verticalLayout_2.addWidget(self.sonet_spacecraft_type_has_return_trajectory_qcmb)
        self.line = QtWidgets.QFrame(self.sonet_mission_tree_qgb)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.sonet_remove_mission_qpb = QtWidgets.QPushButton(self.sonet_mission_tree_qgb)
        self.sonet_remove_mission_qpb.setObjectName("sonet_remove_mission_qpb")
        self.verticalLayout_2.addWidget(self.sonet_remove_mission_qpb)
        self.sonet_remove_spacecraft_qpb = QtWidgets.QPushButton(self.sonet_mission_tree_qgb)
        self.sonet_remove_spacecraft_qpb.setObjectName("sonet_remove_spacecraft_qpb")
        self.verticalLayout_2.addWidget(self.sonet_remove_spacecraft_qpb)
        self.line_3 = QtWidgets.QFrame(self.sonet_mission_tree_qgb)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_2.addWidget(self.line_3)
        self.sonet_pcp_filter_qpb = QtWidgets.QPushButton(self.sonet_mission_tree_qgb)
        self.sonet_pcp_filter_qpb.setObjectName("sonet_pcp_filter_qpb")
        self.verticalLayout_2.addWidget(self.sonet_pcp_filter_qpb)
        self.sonet_select_trajectory_qpb = QtWidgets.QPushButton(self.sonet_mission_tree_qgb)
        self.sonet_select_trajectory_qpb.setObjectName("sonet_select_trajectory_qpb")
        self.verticalLayout_2.addWidget(self.sonet_select_trajectory_qpb)
        self.gridLayout.addWidget(self.sonet_mission_tree_qgb, 0, 1, 1, 1)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.gridLayout.addLayout(self.verticalLayout_7, 0, 2, 1, 1)
        self.sonet_pcp_table_qgb = QtWidgets.QGroupBox(self.centralwidget)
        self.sonet_pcp_table_qgb.setObjectName("sonet_pcp_table_qgb")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.sonet_pcp_table_qgb)
        self.verticalLayout.setObjectName("verticalLayout")
        self.sonet_pcp_tabs_qtw = QtWidgets.QTabWidget(self.sonet_pcp_table_qgb)
        self.sonet_pcp_tabs_qtw.setObjectName("sonet_pcp_tabs_qtw")
        self.sonet_pcp_table_transit_1 = QtWidgets.QWidget()
        self.sonet_pcp_table_transit_1.setObjectName("sonet_pcp_table_transit_1")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.sonet_pcp_table_transit_1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.sonet_pcp_table_qtv_outgoing = QtWidgets.QTableView(self.sonet_pcp_table_transit_1)
        self.sonet_pcp_table_qtv_outgoing.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.sonet_pcp_table_qtv_outgoing.setLineWidth(1)
        self.sonet_pcp_table_qtv_outgoing.setMidLineWidth(1)
        self.sonet_pcp_table_qtv_outgoing.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.sonet_pcp_table_qtv_outgoing.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.sonet_pcp_table_qtv_outgoing.setObjectName("sonet_pcp_table_qtv_outgoing")
        self.verticalLayout_4.addWidget(self.sonet_pcp_table_qtv_outgoing)
        self.sonet_pcp_tabs_qtw.addTab(self.sonet_pcp_table_transit_1, "")
        self.sonet_pcp_table_transit_2 = QtWidgets.QWidget()
        self.sonet_pcp_table_transit_2.setObjectName("sonet_pcp_table_transit_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.sonet_pcp_table_transit_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.sonet_pcp_table_qtv_incoming = QtWidgets.QTableView(self.sonet_pcp_table_transit_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sonet_pcp_table_qtv_incoming.sizePolicy().hasHeightForWidth())
        self.sonet_pcp_table_qtv_incoming.setSizePolicy(sizePolicy)
        self.sonet_pcp_table_qtv_incoming.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.sonet_pcp_table_qtv_incoming.setLineWidth(1)
        self.sonet_pcp_table_qtv_incoming.setMidLineWidth(1)
        self.sonet_pcp_table_qtv_incoming.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.sonet_pcp_table_qtv_incoming.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.sonet_pcp_table_qtv_incoming.setObjectName("sonet_pcp_table_qtv_incoming")
        self.verticalLayout_3.addWidget(self.sonet_pcp_table_qtv_incoming)
        self.sonet_pcp_tabs_qtw.addTab(self.sonet_pcp_table_transit_2, "")
        self.verticalLayout.addWidget(self.sonet_pcp_tabs_qtw)
        self.sonet_label_rows_filtered_visible = QtWidgets.QLabel(self.sonet_pcp_table_qgb)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sonet_label_rows_filtered_visible.sizePolicy().hasHeightForWidth())
        self.sonet_label_rows_filtered_visible.setSizePolicy(sizePolicy)
        self.sonet_label_rows_filtered_visible.setText("")
        self.sonet_label_rows_filtered_visible.setObjectName("sonet_label_rows_filtered_visible")
        self.verticalLayout.addWidget(self.sonet_label_rows_filtered_visible)
        self.sonet_label_selected_trajectory = QtWidgets.QLabel(self.sonet_pcp_table_qgb)
        self.sonet_label_selected_trajectory.setText("")
        self.sonet_label_selected_trajectory.setObjectName("sonet_label_selected_trajectory")
        self.verticalLayout.addWidget(self.sonet_label_selected_trajectory)
        self.sonet_trajectory_selection_qprogrbar = QtWidgets.QProgressBar(self.sonet_pcp_table_qgb)
        self.sonet_trajectory_selection_qprogrbar.setProperty("value", 0)
        self.sonet_trajectory_selection_qprogrbar.setTextVisible(False)
        self.sonet_trajectory_selection_qprogrbar.setObjectName("sonet_trajectory_selection_qprogrbar")
        self.verticalLayout.addWidget(self.sonet_trajectory_selection_qprogrbar)
        self.gridLayout.addWidget(self.sonet_pcp_table_qgb, 0, 0, 1, 1)
        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1350, 21))
        self.menubar.setObjectName("menubar")
        self.file = QtWidgets.QMenu(self.menubar)
        self.file.setObjectName("file")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        main_window.setMenuBar(self.menubar)
        self.exit = QtWidgets.QAction(main_window)
        self.exit.setObjectName("exit")
        self.open_pcp_filter = QtWidgets.QAction(main_window)
        self.open_pcp_filter.setObjectName("open_pcp_filter")
        self.actionHelp = QtWidgets.QAction(main_window)
        self.actionHelp.setObjectName("actionHelp")
        self.file.addAction(self.exit)
        self.file.addSeparator()
        self.menubar.addAction(self.file.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(main_window)
        self.sonet_pcp_tabs_qtw.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QtWidgets.QApplication.translate("main_window", "SONET Mars Mission Timeline", None, -1))
        self.sonet_mission_tree_qgb.setTitle(QtWidgets.QApplication.translate("main_window", "Mission tree", None, -1))
        self.sonet_add_mission_qpb.setText(QtWidgets.QApplication.translate("main_window", "Add mission (pending implementation)", None, -1))
        self.sonet_add_spacecraft_qpb.setText(QtWidgets.QApplication.translate("main_window", "Add spacecraft", None, -1))
        self.sonet_spacecraft_type_qcmb.setItemText(0, QtWidgets.QApplication.translate("main_window", "Crewed", None, -1))
        self.sonet_spacecraft_type_qcmb.setItemText(1, QtWidgets.QApplication.translate("main_window", "Cargo", None, -1))
        self.sonet_spacecraft_type_has_return_trajectory_qcmb.setItemText(0, QtWidgets.QApplication.translate("main_window", "One way", None, -1))
        self.sonet_spacecraft_type_has_return_trajectory_qcmb.setItemText(1, QtWidgets.QApplication.translate("main_window", "Two way", None, -1))
        self.sonet_remove_mission_qpb.setText(QtWidgets.QApplication.translate("main_window", "Remove mission (pending implementation)", None, -1))
        self.sonet_remove_spacecraft_qpb.setText(QtWidgets.QApplication.translate("main_window", "Remove spacecraft", None, -1))
        self.sonet_pcp_filter_qpb.setText(QtWidgets.QApplication.translate("main_window", "Apply filter", None, -1))
        self.sonet_select_trajectory_qpb.setText(QtWidgets.QApplication.translate("main_window", "Select trajectory (pending implementation)", None, -1))
        self.sonet_pcp_table_qgb.setTitle(QtWidgets.QApplication.translate("main_window", "PCP table", None, -1))
        self.sonet_pcp_tabs_qtw.setTabText(self.sonet_pcp_tabs_qtw.indexOf(self.sonet_pcp_table_transit_1), QtWidgets.QApplication.translate("main_window", "Earth - Mars", None, -1))
        self.sonet_pcp_tabs_qtw.setTabText(self.sonet_pcp_tabs_qtw.indexOf(self.sonet_pcp_table_transit_2), QtWidgets.QApplication.translate("main_window", "Mars - Earth ", None, -1))
        self.file.setTitle(QtWidgets.QApplication.translate("main_window", "&File", None, -1))
        self.menuEdit.setTitle(QtWidgets.QApplication.translate("main_window", "Edit", None, -1))
        self.menuHelp.setTitle(QtWidgets.QApplication.translate("main_window", "Help", None, -1))
        self.exit.setText(QtWidgets.QApplication.translate("main_window", "&Exit", None, -1))
        self.open_pcp_filter.setText(QtWidgets.QApplication.translate("main_window", "Apply filter to PCP table", None, -1))
        self.actionHelp.setText(QtWidgets.QApplication.translate("main_window", "Help", None, -1))

