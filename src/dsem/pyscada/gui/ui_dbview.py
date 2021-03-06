# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui_files/dbview.ui'
#
# Created: Wed Jan 28 04:47:37 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_QDBView(object):
    def setupUi(self, QDBView):
        QDBView.setObjectName("QDBView")
        QDBView.resize(423, 279)
        self.verticalLayout = QtGui.QVBoxLayout(QDBView)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.panelFilterRefreshPrint = QtGui.QWidget(QDBView)
        self.panelFilterRefreshPrint.setObjectName("panelFilterRefreshPrint")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.panelFilterRefreshPrint)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setMargin(1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.panelNavigation = QtGui.QWidget(self.panelFilterRefreshPrint)
        self.panelNavigation.setObjectName("panelNavigation")
        self.horizontalLayout = QtGui.QHBoxLayout(self.panelNavigation)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setMargin(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.comboCant = QtGui.QComboBox(self.panelNavigation)
        self.comboCant.setObjectName("comboCant")
        self.horizontalLayout.addWidget(self.comboCant)
        self.pushFirst = QtGui.QPushButton(self.panelNavigation)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/res/go-first.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushFirst.setIcon(icon)
        self.pushFirst.setIconSize(QtCore.QSize(16, 16))
        self.pushFirst.setObjectName("pushFirst")
        self.horizontalLayout.addWidget(self.pushFirst)
        self.pushBack = QtGui.QPushButton(self.panelNavigation)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/res/go-previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushBack.setIcon(icon1)
        self.pushBack.setIconSize(QtCore.QSize(16, 16))
        self.pushBack.setObjectName("pushBack")
        self.horizontalLayout.addWidget(self.pushBack)
        self.pushNext = QtGui.QPushButton(self.panelNavigation)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/res/go-next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushNext.setIcon(icon2)
        self.pushNext.setIconSize(QtCore.QSize(16, 16))
        self.pushNext.setObjectName("pushNext")
        self.horizontalLayout.addWidget(self.pushNext)
        self.pushLast = QtGui.QPushButton(self.panelNavigation)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/res/go-last.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushLast.setIcon(icon3)
        self.pushLast.setIconSize(QtCore.QSize(16, 16))
        self.pushLast.setObjectName("pushLast")
        self.horizontalLayout.addWidget(self.pushLast)
        self.horizontalLayout_2.addWidget(self.panelNavigation)
        self.pushRefresh = QtGui.QPushButton(self.panelFilterRefreshPrint)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/res/view-refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushRefresh.setIcon(icon4)
        self.pushRefresh.setIconSize(QtCore.QSize(16, 16))
        self.pushRefresh.setObjectName("pushRefresh")
        self.horizontalLayout_2.addWidget(self.pushRefresh)
        self.pushFilter = QtGui.QPushButton(self.panelFilterRefreshPrint)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/res/edit-find.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushFilter.setIcon(icon5)
        self.pushFilter.setIconSize(QtCore.QSize(16, 16))
        self.pushFilter.setObjectName("pushFilter")
        self.horizontalLayout_2.addWidget(self.pushFilter)
        self.pushPrint = QtGui.QPushButton(self.panelFilterRefreshPrint)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/res/document-print.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushPrint.setIcon(icon6)
        self.pushPrint.setIconSize(QtCore.QSize(16, 16))
        self.pushPrint.setObjectName("pushPrint")
        self.horizontalLayout_2.addWidget(self.pushPrint)
        self.verticalLayout.addWidget(self.panelFilterRefreshPrint)
        self.tableView = ModelChangedTableView(QDBView)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.label = QtGui.QLabel(QDBView)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.retranslateUi(QDBView)
        QtCore.QMetaObject.connectSlotsByName(QDBView)

    def retranslateUi(self, QDBView):
        QDBView.setWindowTitle(QtGui.QApplication.translate("QDBView", "DB VIew", None, QtGui.QApplication.UnicodeUTF8))
        self.pushFirst.setToolTip(QtGui.QApplication.translate("QDBView", "Primera Página", None, QtGui.QApplication.UnicodeUTF8))
        self.pushBack.setToolTip(QtGui.QApplication.translate("QDBView", "Página anterior", None, QtGui.QApplication.UnicodeUTF8))
        self.pushNext.setToolTip(QtGui.QApplication.translate("QDBView", "Página siguiente", None, QtGui.QApplication.UnicodeUTF8))
        self.pushLast.setToolTip(QtGui.QApplication.translate("QDBView", "Última Página", None, QtGui.QApplication.UnicodeUTF8))
        self.pushRefresh.setToolTip(QtGui.QApplication.translate("QDBView", "Refrescar", None, QtGui.QApplication.UnicodeUTF8))
        self.pushFilter.setToolTip(QtGui.QApplication.translate("QDBView", "Filtrar", None, QtGui.QApplication.UnicodeUTF8))
        self.pushPrint.setToolTip(QtGui.QApplication.translate("QDBView", "Imprimir listado", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("QDBView", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

from dbview import ModelChangedTableView
import data_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    QDBView = QtGui.QWidget()
    ui = Ui_QDBView()
    ui.setupUi(QDBView)
    QDBView.show()
    sys.exit(app.exec_())

