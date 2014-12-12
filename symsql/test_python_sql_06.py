#!/usr/bin/python

from sql import *
import symex.fuzzy as fuzzy

pc_query_dict = {}

def sym_output(query):
    global query_pc_dict
    whole_pc = None
    is_first = True
    for pc in fuzzy.cur_path_constr:
        if is_first:
            whole_pc = pc
            is_first = False
        else:
            sym_add(whole_pc, pc)
    if whole_pc in pc_query_dict:
        print("Warning: identical path condition is found!")
    pc_query_dict[whole_pc] = query

def test_func():
    sym_table_name = fuzzy.mk_str("sym_tname")
    table = Table(sym_table_name)
    sym_column_1 = fuzzy.mk_str("sym_colname_1")
    sym_column_2 = fuzzy.mk_str("sym_colname_2")
    query = table.select(getattr(table, sym_column_1), \
                         getattr(table, sym_column_2))
    sym_str_1 = fuzzy.mk_str("sym_str_1")
    sym_str_2 = fuzzy.mk_str("sym_str_2")
    sym_column_3 = fuzzy.mk_str("sym_colname_3")
    query.where = (getattr(table, sym_column_2) == sym_str_1) & \
                  (getattr(table, sym_column_3) == sym_str_2) 
    process(query)
    sym_output(query)

if __name__ == '__main__':
    fuzzy.concolic_test(test_func)
    for pc, query in pc_query_dict.iteritems():
        result, example = check(query, pc)
        if result == "sat":
            print("UNSAFE: ", example)
        else
            print("SAFE")