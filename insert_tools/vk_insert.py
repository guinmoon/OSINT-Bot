import postgres_helper
from sqlalchemy import create_engine
import os
import json
import glob
import csv
import re

Config = {}


def check_rus_num(num):
    if len(num) != 11:
        return False
    if num[0] != '7':
        return False
    return True


in_file = 'insert_tool/vk_insert.txt'


if __name__ == '__main__':
    with open('config.json', 'r') as f:
        Config = json.load(f)
        Config = Config['configuration']
    engine = create_engine('postgresql+psycopg2://'+Config['db_user']+':' +
                           Config['db_password'] + '@' + Config['db_address']+':'+str(Config['db_port']) + '/' + Config['db_name'])
    connection = engine.connect()

    line_num = 0
    line_insert = 0
    phones = []
    # with open(file=in_file, mode='r', encoding='cp1251') as infile:
    with open(file=in_file, mode='r', encoding='utf-8') as infile:
        for line in infile:
            try:
                if line_num % 100 == 0:
                    print(line_num)

                line = line.replace('\n', '')
                line_data = line.split(',')

                phone = line_data[0]
                # if not check_rus_num(phone):
                #     continue

                name = line_data[1]
                fname = line_data[2]
                uid = line_data[3]
                gender = line_data[4]
                bday = line_data[5]
                city = line_data[6]
                info = '%s %s %s|%s|%s' % (fname, name, gender, bday, city)

                num_id = postgres_helper.db_select_one(
                    connection, "select id from phones where phone = '%s'" % (phone))
                if num_id is None:
                    print("%s Not in base! Inserting..." % phone)
                    res = postgres_helper.db_import(
                        connection, "insert into phones (phone) values ('%s')" % (phone))
                    num_id = postgres_helper.db_select_one(
                        connection, "select id from phones where phone = '%s'" % (phone))
                insert_query = 'insert into phones_info_parsed (phone_id,info_type,uid,info) values (%s,%s,%s,%s)'

                sql = insert_query
                try:
                    result = connection.execute(
                        sql, [(num_id, 6, uid, info)])
                    line_insert += 1
                except Exception as expt:
                    a = 1
                    # print(expt)
                line_num += 1
            except Exception as eexpt:
                print(eexpt)
    print("Inserted %i" % line_insert)
