#!/usr/bin/python

from mysql import *
import symex.fuzzy as fuzzy
import symsqlutils
import z3

pc_query_dict = {}

def sym_output(query):
    global query_pc_dict
    whole_pc = fuzzy.const_bool(True)
    is_first = True
    for pc in fuzzy.cur_path_constr:
        if is_first:
            whole_pc = pc
            is_first = False
        else:
            whole_pc = fuzzy.sym_and(whole_pc, pc)
    if whole_pc in pc_query_dict:
        print("Warning: identical path condition is found!")
    pc_query_dict[whole_pc] = query

def test_func():
    sym_table_name = fuzzy.mk_str("sym_tname")
    table = Table(sym_table_name)
    sym_column = fuzzy.mk_str("sym_colname")
    query = table.select(sym_column)
    sym_output(query)

if __name__ == '__main__':
    fuzzy.concolic_test(test_func)
    for pc, query in pc_query_dict.iteritems():
        result, example = symsqlutils.checkSqlInjection(query, pc)
        if result == z3.sat:
            print("UNSAFE: ", example)
        else:
            print("SAFE")
