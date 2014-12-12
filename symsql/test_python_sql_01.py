#!/usr/bin/python

from sql import *
import symex.fuzzy as fuzzy
import z3
import symsqlutils

pc_query_dict = {}
query_list = []

def sym_output(query):
    global query_pc_dict
    whole_pc = fuzzy.const_bool(True)
    is_first = True
    for pc in fuzzy.cur_path_constr:
        if is_first:
            whole_pc = pc
            is_first = False
        else:
            sym_add(whole_pc, pc)
    if whole_pc in pc_query_dict:
        print("Warning: identical path condition is found!")
    query_list.append(query)
    pc_query_dict[whole_pc] = query

def test_func():
    sym_table_name = fuzzy.mk_str("sym_tname")
    table = Table(sym_table_name)
    query = table.select()
    query = symsqlutils.symStrInterpolation(query)
    sym_output(query)

if __name__ == '__main__':
    fuzzy.concolic_test(test_func)
    print query_list
    for pc, query in pc_query_dict.iteritems():
        result, example = symsqlutils.checkSqlInjection(query, pc)
        if result == z3.sat:
            print("UNSAFE: ", example)
        else:
            print("SAFE")
