#!/usr/bin/python 
import symex.fuzzy as fuzzy

# Remove single quotation marks added by the SQL library code.
def elimQuoLit(str_sym_tree, isCat):
    if isinstance(str_sym_tree, fuzzy.const_str) and isCat:
        str_sym_tree.v = str_sym_tree.v.replace("'", "")
        return
    if isinstance(str_sym_tree, fuzzy.sym_func_apply):
        isCat = isinstance(str_sym_tree, fuzzy.sym_concat)
        for arg in str_sym_tree.args:
            elimQuoLit(arg, isCat)
    return str_sym_tree

def symStrInterpolation(query):
    symTemplate, params = tuple(query)
    for param in params:
        placeholderIndex = symTemplate.find("%s")
        firstPart = symTemplate[0, placeholderIndex]
        lastPart = symTemplate[placeholderIndex + 2, len(symTemplate)]
        symTemplate = firstPart + param + lastPart
    return symTemplate

def checkSqlInjection(symSqlQuery, pathCondition):
    # Remove single quotes introduced by the SQL library code.
    elimQuoLit(fuzzy.ast(symSqlQuery), True)
    # Remove single quotes that are properly escaped
    symSqlQuery = symSqlQuery.replace("''","")
    # If the sql query could still contains single quotes, it probably indicates
    # a injection bug in the Sql library code.
    injectionCondition = fuzzy.sym_and(fuzzy.sym_contains(fuzzy.ast(symSqlQuery), fuzzy.ast("'")), pathCondition)
    print "SQL injection condition:"
    print injectionCondition
    return fuzzy.fork_and_check(injectionCondition)
    