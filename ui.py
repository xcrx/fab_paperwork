__author__ = 'ryan'

from PyQt4 import QtCore, QtGui
from code128 import Code128
from PIL import ImageQt

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setObjectName("MainWindow")
        self.setWindowTitle("Fabrication Paperwork")
        self.resize(1024, 768)

        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")

        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName("gridLayout")

        self.joblabel = QtGui.QLabel(self.widget)
        self.joblabel.setObjectName("joblabel")
        self.joblabel.setText("Job #:")
        self.gridLayout.addWidget(self.joblabel, 0, 0, 1, 1)

        self.jobnum = QtGui.QLineEdit(self.widget)
        self.jobnum.setObjectName("jobnum")
        self.gridLayout.addWidget(self.jobnum, 1, 0, 1, 1)

        self.machinelabel = QtGui.QLabel(self.widget)
        self.machinelabel.setObjectName("machinelabel")
        self.machinelabel.setText("Machine:")
        self.gridLayout.addWidget(self.machinelabel, 0, 1, 1, 1)

        self.machine = QtGui.QLineEdit(self.widget)
        self.machine.setObjectName("machine")
        self.gridLayout.addWidget(self.machine, 1, 1, 1, 1)

        self.createdlabel = QtGui.QLabel(self.widget)
        self.createdlabel.setObjectName("createdlabel")
        self.createdlabel.setText("Created By:")
        self.gridLayout.addWidget(self.createdlabel, 0, 2, 1, 1)

        self.created = QtGui.QLineEdit(self.widget)
        self.created.setObjectName("created")
        self.gridLayout.addWidget(self.created, 1, 2, 1, 1)

        self.datelabel = QtGui.QLabel(self.widget)
        self.datelabel.setObjectName("datelabel")
        self.datelabel.setText("Date:")
        self.gridLayout.addWidget(self.datelabel, 0, 3, 1, 1)

        self.dateline = QtGui.QLineEdit(self.widget)
        self.dateline.setObjectName("dateline")
        self.gridLayout.addWidget(self.dateline, 1, 3, 1, 1)

        self.loadcnc = QtGui.QPushButton(self.widget)
        self.loadcnc.setObjectName("loadcnc")
        self.loadcnc.setText("Load CNC")
        self.gridLayout.addWidget(self.loadcnc, 0, 4, 1, 1)

        self.searchline = QtGui.QLineEdit(self.widget)
        self.searchline.setObjectName("searchline")
        self.searchline.setPlaceholderText("Seach By Job #...")
        self.gridLayout.addWidget(self.searchline, 0, 5, 1, 1)

        self.printbutton = QtGui.QPushButton(self.widget)
        self.printbutton.setObjectName("printbutton")
        self.printbutton.setText("Print")
        self.gridLayout.addWidget(self.printbutton, 1, 4, 1, 1)

        self.savebutton = QtGui.QPushButton(self.widget)
        self.savebutton.setObjectName("savebutton")
        self.savebutton.setText("Save")
        self.gridLayout.addWidget(self.savebutton, 1, 5, 1, 1)

        self.line = QtGui.QFrame(self.widget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 6)

        self.workparts = QtGui.QTableWidget(self)
        self.workparts.setObjectName("workparts")
        self.workparts.setColumnCount(7)

        cols = ["Part #", "Qty", "Dest", "Order", "Status", "Routing", "Material"]
        for i, col in enumerate(cols):
            self.workparts.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(col))

        self.gridLayout.addWidget(self.workparts, 3, 0, 2, 4)

        self.badpartlabel = QtGui.QLabel(self.widget)
        self.badpartlabel.setObjectName("badpartlabel")
        self.badpartlabel.setText("Bad Part Numbers:")
        self.gridLayout.addWidget(self.badpartlabel, 3, 4, 1, 1)

        self.badparts = QtGui.QTableWidget(self.widget)
        self.badparts.setObjectName("badparts")
        self.badparts.setColumnCount(2)
        bad_cols = ["Part #", "Qty"]
        for i, col in enumerate(bad_cols):
            self.badparts.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(col))
        self.gridLayout.addWidget(self.badparts, 4, 4, 1, 2)

        self.centralwidget.setLayout(self.gridLayout)
        self.setCentralWidget(self.centralwidget)


class PrintsWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setObjectName("PrintsWidget")
        self.setWindowTitle("Fabrication Paperwork")
        self.resize(1024, 768)

        self.widget = QtGui.QWidget(self)
        self.widget.setGeometry(QtCore.QRect(10, 0, 1008, 761))
        self.widget.setObjectName("widget")
        self.maingrid = QtGui.QGridLayout(self.widget)
        self.maingrid.setMargin(0)
        self.maingrid.setObjectName("maingrid")

        self.barcodeboxtop = QtGui.QGroupBox(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.barcodeboxtop.sizePolicy().hasHeightForWidth())
        self.barcodeboxtop.setSizePolicy(sizePolicy)
        self.barcodeboxtop.setMinimumSize(QtCore.QSize(200, 100))
        self.barcodeboxtop.setMaximumSize(QtCore.QSize(200, 100))
        self.barcodeboxtop.setObjectName("barcodeboxtop")

        self.verticalLayout = QtGui.QVBoxLayout(self.barcodeboxtop)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setMargin(3)
        self.verticalLayout.setObjectName("verticalLayout")

        self.barcodetop = QtGui.QLabel(self.barcodeboxtop)
        self.barcodetop.setObjectName("barcodetop")
        self.verticalLayout.addWidget(self.barcodetop)

        # self.barcodelabeltop = QtGui.QLabel(self.barcodeboxtop)
        # self.barcodelabeltop.setAlignment(QtCore.Qt.AlignCenter)
        # self.barcodelabeltop.setObjectName("barcodelabeltop")
        # self.verticalLayout.addWidget(self.barcodelabeltop)

        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 1)
        self.maingrid.addWidget(self.barcodeboxtop, 0, 3, 1, 1)

        self.printlabel = QtGui.QLabel(self.widget)
        sizePolicymm = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicymm.setHorizontalStretch(0)
        sizePolicymm.setVerticalStretch(0)
        sizePolicymm.setHeightForWidth(self.printlabel.sizePolicy().hasHeightForWidth())
        self.printlabel.setSizePolicy(sizePolicymm)
        self.printlabel.setMaximumSize(QtCore.QSize(100, 16777215))
        self.printlabel.setObjectName("printlabel")
        self.printlabel.setText("Print:")
        self.maingrid.addWidget(self.printlabel, 1, 1, 1, 1)

        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.maingrid.addItem(spacerItem, 3, 0, 1, 1)

        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.maingrid.addItem(spacerItem1, 1, 3, 1, 1)

        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.maingrid.addItem(spacerItem2, 1, 0, 1, 1)

        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.dateline = QtGui.QLineEdit(self.widget)
        sizePolicymf = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicymf.setHorizontalStretch(0)
        sizePolicymf.setVerticalStretch(0)
        sizePolicymf.setHeightForWidth(self.dateline.sizePolicy().hasHeightForWidth())
        self.dateline.setSizePolicy(sizePolicymf)
        self.dateline.setObjectName("dateline")
        self.gridLayout_2.addWidget(self.dateline, 1, 1, 1, 1)

        self.machine = QtGui.QLineEdit(self.widget)
        self.machine.setSizePolicy(sizePolicymf)
        self.machine.setObjectName("machine")
        self.gridLayout_2.addWidget(self.machine, 0, 3, 1, 1)
        
        self.orderlabel = QtGui.QLabel(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.orderlabel.sizePolicy().hasHeightForWidth())
        self.orderlabel.setSizePolicy(sizePolicy)
        self.orderlabel.setText("Order #:")
        self.orderlabel.setObjectName("orderlabel")

        self.gridLayout_2.addWidget(self.orderlabel, 1, 2, 1, 1)
        self.jobnum = QtGui.QLineEdit(self.widget)
        self.jobnum.setSizePolicy(sizePolicymf)
        self.jobnum.setObjectName("jobnum")
        self.gridLayout_2.addWidget(self.jobnum, 0, 1, 1, 1)
        
        self.order = QtGui.QLineEdit(self.widget)
        self.order.setSizePolicy(sizePolicymf)
        self.order.setObjectName("order")
        self.gridLayout_2.addWidget(self.order, 1, 3, 1, 1)
        
        self.datelabel = QtGui.QLabel(self.widget)
        self.datelabel.setSizePolicy(sizePolicymf)
        self.datelabel.setObjectName("datelabel")
        self.datelabel.setText("Date:")
        self.gridLayout_2.addWidget(self.datelabel, 1, 0, 1, 1)
        
        self.machinelabel = QtGui.QLabel(self.widget)
        self.machinelabel.setSizePolicy(sizePolicymf)
        self.machinelabel.setObjectName("machinelabel")
        self.machinelabel.setText("Machine:")
        self.gridLayout_2.addWidget(self.machinelabel, 0, 2, 1, 1)

        self.joblabel = QtGui.QLabel(self.widget)
        self.joblabel.setSizePolicy(sizePolicymf)
        self.joblabel.setObjectName("joblabel")
        self.joblabel.setText("Job #:")
        self.gridLayout_2.addWidget(self.joblabel, 0, 0, 1, 1)

        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 0, 4, 2, 1)
        
        self.maingrid.addLayout(self.gridLayout_2, 0, 0, 1, 3)

        self.printbox = QtGui.QLabel(self.widget)
        sizePolicyMM = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.barcodeboxtop.sizePolicy().hasHeightForWidth())
        self.printbox.setSizePolicy(sizePolicyMM)
        self.printbox.setMinimumSize(QtCore.QSize(900, 700))
        self.printbox.setMaximumSize(QtCore.QSize(900, 700))
        self.printbox.setObjectName("printbox")
        self.maingrid.addWidget(self.printbox, 2, 1, 3, 3)
        
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        
        self.partlabel = QtGui.QLabel(self.widget)
        self.partlabel.setSizePolicy(sizePolicymf)
        self.partlabel.setMaximumWidth(100)
        self.partlabel.setObjectName("partlabel")
        self.partlabel.setText("Part #:")
        self.gridLayout.addWidget(self.partlabel, 0, 0, 1, 1)

        self.partnum = QtGui.QLineEdit(self.widget)
        self.partnum.setSizePolicy(sizePolicymf)
        self.partnum.setMaximumWidth(200)
        self.partnum.setObjectName("partnum")
        self.gridLayout.addWidget(self.partnum, 0, 1, 1, 1)
        
        self.qtylabel = QtGui.QLabel(self.widget)
        self.qtylabel.setSizePolicy(sizePolicymf)
        self.qtylabel.setObjectName("qtylabel")
        self.qtylabel.setText("Qty:")
        self.gridLayout.addWidget(self.qtylabel, 1, 0, 1, 1)
        
        self.qty = QtGui.QLineEdit(self.widget)
        self.qty.setSizePolicy(sizePolicymf)
        self.qty.setMaximumWidth(200)
        self.qty.setObjectName("qty")
        self.gridLayout.addWidget(self.qty, 1, 1, 1, 1)
        
        self.desclabel = QtGui.QLabel(self.widget)
        self.desclabel.setSizePolicy(sizePolicymf)
        self.desclabel.setObjectName("desclabel")
        self.desclabel.setText("Description:")
        self.gridLayout.addWidget(self.desclabel, 2, 0, 1, 1)
        
        self.description = QtGui.QLineEdit(self.widget)
        self.description.setSizePolicy(sizePolicymf)
        self.description.setMaximumWidth(200)
        self.description.setObjectName("description")
        self.gridLayout.addWidget(self.description, 2, 1, 1, 1)
        
        self.matlabel = QtGui.QLabel(self.widget)
        self.matlabel.setSizePolicy(sizePolicymf)
        self.matlabel.setObjectName("matlabel")
        self.matlabel.setText("Material:")
        self.gridLayout.addWidget(self.matlabel, 3, 0, 1, 1)
        
        self.material = QtGui.QLineEdit(self.widget)
        self.material.setSizePolicy(sizePolicymf)
        self.material.setMaximumWidth(200)
        self.material.setObjectName("material")
        self.gridLayout.addWidget(self.material, 3, 1, 1, 1)
        
        self.routlabel = QtGui.QLabel(self.widget)
        self.routlabel.setSizePolicy(sizePolicymf)
        self.routlabel.setObjectName("routlabel")
        self.routlabel.setText("Routing:")
        self.gridLayout.addWidget(self.routlabel, 4, 0, 1, 1)
        
        self.routing = QtGui.QLineEdit(self.widget)
        self.routing.setSizePolicy(sizePolicymf)
        self.routing.setMaximumWidth(200)
        self.routing.setObjectName("routing")
        self.gridLayout.addWidget(self.routing, 4, 1, 1, 1)
        
        self.desclabel = QtGui.QLabel(self.widget)
        self.desclabel.setSizePolicy(sizePolicymf)
        self.desclabel.setObjectName("desclabel")
        self.desclabel.setText("Destination:")
        self.gridLayout.addWidget(self.desclabel, 5, 0, 1, 1)
        
        self.destination = QtGui.QLineEdit(self.widget)
        self.destination.setSizePolicy(sizePolicymf)
        self.destination.setMaximumWidth(200)
        self.destination.setObjectName("destination")
        self.gridLayout.addWidget(self.destination, 5, 1, 1, 1)
        
        self.noteslabel = QtGui.QLabel(self.widget)
        self.noteslabel.setSizePolicy(sizePolicymf)
        self.noteslabel.setObjectName("noteslabel")
        self.noteslabel.setText("Notes:")
        self.gridLayout.addWidget(self.noteslabel, 6, 0, 1, 1)
        
        self.notes = QtGui.QTextEdit(self.widget)
        sizePolicyme = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicyme.setHorizontalStretch(0)
        sizePolicyme.setVerticalStretch(0)
        sizePolicyme.setHeightForWidth(self.notes.sizePolicy().hasHeightForWidth())
        self.notes.setSizePolicy(sizePolicyme)
        self.notes.setMaximumWidth(200)
        self.notes.setObjectName("notes")
        self.gridLayout.addWidget(self.notes, 6, 1, 1, 1)

        self.maingrid.addLayout(self.gridLayout, 2, 0, 1, 1)

        self.barcodeboxbtm = QtGui.QGroupBox(self.widget)
        self.barcodeboxbtm.setSizePolicy(sizePolicy)
        self.barcodeboxbtm.setMinimumSize(QtCore.QSize(200, 100))
        self.barcodeboxbtm.setMaximumSize(QtCore.QSize(200, 100))
        self.barcodeboxbtm.setObjectName("barcodeboxbtm")

        self.verticalLayout_2 = QtGui.QVBoxLayout(self.barcodeboxbtm)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setMargin(3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.barcodebtm = QtGui.QLabel(self.barcodeboxbtm)
        self.barcodebtm.setObjectName("barcodebtm")
        self.verticalLayout_2.addWidget(self.barcodebtm)

        # self.barcodebtmlabel = QtGui.QLabel(self.barcodeboxbtm)
        # self.barcodebtmlabel.setAlignment(QtCore.Qt.AlignCenter)
        # self.barcodebtmlabel.setObjectName("barcodebtmlabel")
        # self.verticalLayout_2.addWidget(self.barcodebtmlabel)

        self.verticalLayout_2.setStretch(0, 2)
        self.verticalLayout_2.setStretch(1, 1)
        self.maingrid.addWidget(self.barcodeboxbtm, 4, 0, 1, 1)

        self.printline = QtGui.QLineEdit(self.widget)
        self.printline.setSizePolicy(sizePolicymf)
        self.printline.setObjectName("printline")
        self.maingrid.addWidget(self.printline, 1, 2, 1, 1)

    def fill_data(self, jobdata, partdata):
        self.jobnum.setText(jobdata['jobnum'])
        self.dateline.setText(jobdata['date'])
        self.machine.setText(jobdata['machine'])

        self.partnum.setText(partdata['partnum'])
        self.qty.setText(partdata['qty'])
        self.description.setText(partdata['desc'])
        self.material.setText(partdata['mat'])
        self.routing.setText(partdata['rout'])
        self.destination.setText(partdata['dest'])
        self.printline.setText(partdata['print'])
        self.order.setText(partdata['order'])
        notes = partdata['notes']
        if "Null" in notes:
            notes = ""
        self.notes.setText(notes)

        tracking = partdata['tracking']

        barcode = self.getBarcodes(tracking)

        # self.barcodelabeltop.setText(tracking)
        # self.barcodebtmlabel.setText(tracking)
        self.barcodebtm.setPixmap(barcode)
        self.barcodetop.setPixmap(barcode)

        print_pix = QtGui.QPixmap()
        print_pix.load("P:\\{0}.jpg".format(self.printline.text()))
        print_pix = print_pix.scaledToWidth(700, mode=QtCore.Qt.SmoothTransformation)
        self.printbox.setPixmap(print_pix)

    def getBarcodes(self, code):
        img = Code128().getImage(code)
        barcodeImage = ImageQt.ImageQt(img.convert('RGBA'))
        barcodePix = QtGui.QPixmap.fromImage(barcodeImage).scaled(250, 75, 1, 1)
        return barcodePix