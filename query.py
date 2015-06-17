__author__ = 'rhanson'

from PyQt4 import QtSql, QtGui
import sys
from database_connection import db_err, default_connection

load_work_order = ("SELECT `Job_ID`, `Job_num`, `Date`, `Machine_Desc`, `Name` FROM workOrder_qry "
                   "WHERE `Job_num` like '{0}'")
load_wo_parts = ("SELECT `Part Num`, `Qty`, `Dest`, `Status`, `Order`, `Desc`, `Mat`, `Process`, `Print`, `Tracking`, "
                 "`Notes` FROM workOrderData_qry WHERE `Job_ID`={0} ORDER BY `Part Num` ASC")
check_part = ("SELECT `Part_ID`, `Dest_Desc` FROM `Parts_tbl` JOIN `Destination_tbl` ON `Parts_tbl`.`destination` = "
              "`Destination_tbl`.`Dest_id` WHERE `Part_num` LIKE '{0}'")
save_job = "INSERT INTO `Work_Orders_tbl` (`Job_num`, `Machine_ID`, `User_ID`) VALUES('{0}', {1}, {2})"
save_part = ("INSERT INTO `Work_Details_tbl` (`Job_ID`, `Part_ID`, `Qty`, `Dest_ID`, `orderNum`, `Tracking_num`) "
             "VALUES({0}, {1}, {2}, {3}, '{4}', {5}) ON DUPLICATE KEY UPDATE `Qty`={2}, `Dest_ID`={3}, `orderNum`='{4}'")
save_new_part = ("INSERT INTO `Work_Details_tbl` (`Job_ID`, `Part_ID`, `Qty`, `Dest_ID`, `orderNum`) "
                 "VALUES({0}, {1}, {2}, {3}, '{4}')")
create_status = ("INSERT INTO `Status_tbl` (`Status_Description`, `User_ID`, `Tracking_num`) "
                 "VALUES('Programmed', 42, {0})")
parts = "SELECT `Part_ID`, `Part_num` FROM `Parts_tbl` ORDER BY `Part_num` ASC"
dest = "SELECT `Dest_ID`, `Dest_Desc` FROM `Destination_tbl` ORDER BY `Dest_Desc` ASC"
machine = "SELECT `Machine_ID`, `Machine_Desc` FROM `Machine_tbl` ORDER BY `Machine_Desc` ASC"
user = "SELECT `User_ID`, `Name` FROM `Users_tbl` WHERE `active` ORDER BY `Name` ASC"

part_id = "SELECT `Part_ID` FROM `Parts_tbl` WHERE `Part_num` LIKE '{0}'"
dest_id = "SELECT `Dest_ID` FROM `Destination_tbl` WHERE `Dest_Desc` LIKE '{0}'"
machine_id = "SELECT `Machine_ID` FROM `Machine_tbl` WHERE `Machine_Desc` LIKE '{0}'"
user_id = "SELECT `User_ID` FROM `Users_tbl` WHERE Name LIKE '{0}'"


def query(data, args=None, db='qt_sql_default_connection', rerun=False):
    qry = QtSql.QSqlQuery(db)
    try:
        dataf = getattr(sys.modules[__name__], data)
    except AttributeError:
        QtGui.QMessageBox.critical(None, "Query Not Found", "A query matching %s was not found. Typo?" % data)
        return False
    if args:
        dataf = dataf.format(*args)
    if qry.exec_(dataf):
        return qry
    else:
        if not rerun:
            print(dataf)
            default_connection()
            s = query(data, args, rerun=True)
            return s
        else:
            db_err(qry)
            return False