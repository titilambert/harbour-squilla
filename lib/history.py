#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtSql
import datetime

db = QtSql.QSqlDatabase("QSQLITE")
db.setDatabaseName("/home/user/.rtcom-eventlogger/el-v1.db");

def insert_sms_in_history(sms):
    global db

    # Pre
    num = sms['num']
    msg = sms['message'].encode('utf-8').decode('utf-8')
    group_uid = str(num[-7:])
    now = int(datetime.datetime.now().strftime("%s"))

    db.open()
    query = QtSql.QSqlQuery(db)
    query.prepare("""INSERT INTO Events (service_id, event_type_id,
                     storage_time, start_time, end_time, is_read,
                     outgoing, flags, bytes_sent, bytes_received,
                     local_uid, local_name, remote_uid, channel,
                     free_text, group_uid)
                     VALUES (:service_id, :event_type_id,
                     :storage_time, :start_time, :end_time, :is_read,
                     :outgoing, :flags, :bytes_sent, :bytes_received,
                     :local_uid, :local_name, :remote_uid, :channel,
                    :free_text, :group_uid)"""
                    )

    query.bindValue(":service_id", 3)
    query.bindValue(":event_type_id", 11)
    query.bindValue(":storage_time", now)
    query.bindValue(":start_time", now)
    query.bindValue(":end_time", 0)
    query.bindValue(":is_read", 1)
    query.bindValue(":outgoing", 1)
    query.bindValue(":flags", 0)
    query.bindValue(":bytes_sent", 0)
    query.bindValue(":bytes_received", 0)
    query.bindValue(":local_uid", "ring/tel/ring")
    query.bindValue(":local_name", "<SelfHandle>")
    query.bindValue(":remote_uid", num)
    query.bindValue(":channel", "")
    query.bindValue(":free_text", msg)
    query.bindValue(":group_uid", group_uid)
    status = query.exec_()

    db.close()
