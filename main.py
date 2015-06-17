__author__ = 'ryan'

from PyQt4 import QtCore, QtGui, QtSql
import re

import ui
from query import query


def get_data_list(query_name):
    qry = query(query_name)
    q_list = []
    while qry.next():
        q_list.append(str(qry.value(1)))
    return q_list


def phrase_cnc(text):
    content = text.readlines()
    trim = []
    parts = []
    write = False
    for line in content:
        if "(endPartsList)" in line:
            write = False
        if write:
            trim.append(line)
        if "(startPartsList)" in line:
            write = True
    for line in trim:
        part = re.search('(?<=PART - )(.*?)(?=\.prt)', line)
        qty = re.search('(?<=prt = )(.*?)\d+', line)
        parts.append([part.group(0), qty.group(0)])
    return parts


class Main(ui.MainWindow):

    def __init__(self):
        ui.MainWindow.__init__(self)
        self.jobid = None
        self.job = {}
        self.parts = []

        def connections():
            self.searchline.returnPressed.connect(self.search)
            self.printbutton.clicked.connect(self.print_paperwork)
            self.savebutton.clicked.connect(self.save)
            self.loadcnc.clicked.connect(self.load_cnc)

        parts_qry = query("parts")
        self.parts_d = {}
        while parts_qry.next():
            self.parts_d[str(parts_qry.value(1))] = str(parts_qry.value(0))

        self.machine_l = get_data_list("machine")
        self.user_l = get_data_list("user")

        self.machine.setCompleter(QtGui.QCompleter(self.machine_l))
        self.created.setCompleter(QtGui.QCompleter(self.user_l))

        connections()

    def search(self):
        jobnum = self.searchline.text()
        self.parts = []
        self.job.clear()
        self.jobnum.setText("")
        self.dateline.setText("")
        self.machine.setText("")
        self.created.setText("")
        #self.workparts.clearContents()
        for i in range(self.workparts.rowCount()):
            self.workparts.removeRow(0)
        for i in range(self.badparts.rowCount()):
            self.badparts.removeRow(0)
        qry = query("load_work_order", {jobnum})
        if qry:
            self.searchline.setText("")
            if qry.first():
                self.jobid = qry.value(0)
                self.job['jobnum'] = qry.value(1)
                self.job['date'] = qry.value(2)
                self.job['machine'] = qry.value(3)
                self.jobnum.setText(str(qry.value(1)))
                self.dateline.setText(str(qry.value(2)))
                self.machine.setText(str(qry.value(3)))
                self.created.setText(str(qry.value(4)))

                subqry = query("load_wo_parts", {self.jobid})
                while subqry.next():
                    self.parts.append({'tracking': str(subqry.value(9)),
                                       'partnum': str(subqry.value(0)),
                                       'qty': str(subqry.value(1)),
                                       'desc': str(subqry.value(5)),
                                       'mat': str(subqry.value(6)),
                                       'rout': str(subqry.value(7)),
                                       'dest': str(subqry.value(2)),
                                       'notes': str(subqry.value(10)),
                                       'print': str(subqry.value(8)),
                                       'order': str(subqry.value(4)),
                                       'status': str(subqry.value(3)),
                                       })

                for i, part in enumerate(self.parts):
                    self.workparts.insertRow(i)
                    keys = ["partnum", "qty", "dest", "order", "status", "rout", "mat"]
                    for e, key in enumerate(keys):
                        text = QtGui.QTableWidgetItem(part[key])
                        if "QPyNullVariant" in text.text():
                            text.setText("")
                            part.update({key: ""})
                        self.workparts.setItem(i, e, text)

                self.workparts.resizeColumnsToContents()

    def print_paperwork(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        print_ = QtGui.QPrintPreviewDialog()
        print_.paintRequested.connect(self.print_preview)
        print_.exec_()
        QtGui.QApplication.restoreOverrideCursor()

    def print_preview(self, printer):
        printer.setOrientation(1)
        printer.setPaperSize(printer.PageSize(2))
        printer.setPageSize(printer.PageSize(2))
        printer.setPageMargins(.25, .25, .25, .25, 2)
        painter = QtGui.QPainter()
        painter.begin(printer)
        for i, part in enumerate(self.parts):
            self.printWork = ui.PrintsWidget()
            self.printWork.fill_data(self.job, part)
            self.printWork.setGeometry(printer.pageRect())
            self.printWork.render(painter)
            if i < self.parts.__len__()-1:
                printer.newPage()
        painter.end()

    def save(self):
        if self.jobid is None:
            job = []
            job.append(self.jobnum.text())
            machine_qry = query("machine_id")
            if machine_qry.first():
                machine_id = str(machine_qry.value(0))
            else:
                machine_id = "8"
            job.append(machine_id)
            user_qry = query("user_id")
            if user_qry.first():
                user_id = str(user_qry.value(0))
            else:
                user_id = "42"
            job.append(user_id)
            jobqry = query("save_job", job)
            jobid = jobqry.lastInsertId()
            print(jobid)
        else:
            jobid = self.jobid
        parts = []
        for i in range(self.workparts.rowCount()):
            dest = self.workparts.item(i, 2).text()
            dest_qry = query("dest_id", [dest])
            if dest_qry.first():
                dest_id = str(dest_qry.value(0))
            else:
                dest_id = "7"
            part = self.workparts.item(i, 0).text()
            # part_qry = query("part_id", [part])
            # if part_qry.first():
            #     part_id = str(part_qry.value(0))
            part_id = self.parts_d[part]
            if self.parts.__len__() > 0:
                row = [jobid,
                       part_id,
                       self.workparts.item(i, 1).text(),
                       dest_id,
                       self.workparts.item(i, 3).text(),
                       self.parts[i]['tracking']]
                parts.append(row)
            else:
                row = [jobid,
                       part_id,
                       self.workparts.item(i, 1).text(),
                       dest_id,
                       self.workparts.item(i, 3).text()]
                parts.append(row)

        for part in parts:
            if self.parts.__len__() > 0:
                query("save_part", part)
            else:
                qry = query("save_new_part", part)
                tid = qry.lastInsertId()
                query("create_status", [tid])

        self.searchline.setText(self.jobnum.text())
        self.search()

    def load_cnc(self):
        self.jobid = None
        self.parts = []
        self.job.clear()
        self.jobnum.setText("")
        self.dateline.setText("")
        self.machine.setText("")
        self.created.setText("")
        for i in range(self.workparts.rowCount()):
            self.workparts.removeRow(0)
        open_files = QtGui.QFileDialog.getOpenFileNames(self, "Phrase CNC Files", "N:\\", "*.cnc")
        cnc = []
        parts = {}
        for file in open_files:
            with open(file, 'r') as f:
                cnc.append(phrase_cnc(f))
        for c in cnc:
            for p in c:
                if p[0] in parts.keys():
                    parts[p[0]] = str(int(p[1]) + int(parts[p[0]]))
                else:
                    parts[p[0]] = p[1]
        good_parts = []
        bad_parts = []
        for part in parts.keys():
            qry = query("check_part", [part])
            if qry.size() > 0:
                qry.first()
                good_parts.append([part, parts[part], str(qry.value(1)), ''])
            else:
                bad_parts.append([part, parts[part]])

        for i, part in enumerate(good_parts):
            self.workparts.insertRow(i)
            for e, cell in enumerate(part):
                text = QtGui.QTableWidgetItem(cell)
                self.workparts.setItem(i, e, text)
        for i, part in enumerate(bad_parts):
            self.badparts.insertRow(i)
            for e, cell in enumerate(part):
                text = QtGui.QTableWidgetItem(cell)
                self.badparts.setItem(i, e, text)
        print(good_parts)
        print(bad_parts)