from Model.DBHandler.Query import *
from Model.NLHandler.Parser import Parser
from Model.NLHandler.ParseTree import ParseTree

class Translator:
    def __init__(self, parsetree, schema):
        self.__parsetree = parsetree
        self.__query = Query(schema)

    def translateParsetree(self):
        for node in self.__parsetree.get_nodelist:
            if not node.getTranslated:
                ntype = node.getComponent.get_type
                if ntype == 'SN':
                    node.setTranslated(True)
                if ntype == 'FN':
                    self.translateFN(node)
                if ntype == 'ON':
                    self.translateON(node)
                if ntype == 'GN':
                    self.translateGN(node)
                if ntype == 'OR':
                    self.translateOR(node)
                if ntype == 'DN':
                    self.__query.select.set_distinct(True)
                    node.setTranslated(True)
                if ntype == 'LN':
                    self.__query.where.set_logicop(node.getComponent.get_component)
                    node.setTranslated(True)
                if ntype == 'NN':
                    self.translateNN(node)
                if ntype == 'VN':
                    self.translateVN(node)

        return self.__query

    def translateFN(self, node):
        self.__query.function.set_type(node.getComponent.get_component)
        node.setTranslated(True)
        children = node.getChildren
        if len(children)>=1:
            for ch in children:
                if ch.getComponent.get_type == 'NN':
                    ch.setTranslated(True)
                    chname = ch.getComponent.get_component
                    if '.' in chname:
                        self.__query.function.set_column(chname)
                        table = chname.split('.')[0]
                        self.__query.fromq.addtable(table)
                    else:
                        self.__query.function.set_column('*')
                        self.__query.fromq.addtable(chname)
        else:
            parent = node.getParent
            if (parent.getComponent.get_type == 'NN'):
                parent.setTranslated(True)
                chname = parent.getComponent.get_component
                if '.' in chname:
                    self.__query.function.set_column(chname)
                    table = chname.split('.')[0]
                    self.__query.fromq.addtable(table)
                else:
                    self.__query.function.set_column('*')
                    self.__query.fromq.addtable(chname)
            else:
                print("Failure")

    def translateON(self, node):
        cond = Condition()
        cond.set_operator(node.getComponent.get_component)
        node.setTranslated(True)
        children = node.getChildren
        if len(children)>=1:
            for ch in children:
                if ch.getComponent.get_type == 'VN':
                    ch.setTranslated(True)
                    chcol = ch.getComponent.get_component
                    chname = ch.getWord.get_text()
                    if '.' in chcol:
                        cond.set_column(chcol)
                        cond.set_value(chname)
                        table = chcol.split('.')[0]
                        self.__query.fromq.addtable(table)
        else:
            parent = node.getParent
            if (parent.getComponent.get_type == 'VN'):
                parent.setTranslated(True)
                chcol = parent.getComponent.get_component
                chname = parent.getWord.get_text()
                if '.' in chcol:
                    cond.set_column(chcol)
                    cond.set_value(chname)
                    table = chcol.split('.')[0]
                    self.__query.fromq.addtable(table)
            else:
                print("Failure")
        self.__query.where.addcondition(cond)

    def translateGN(self, node):
        node.setTranslated(True)
        children = node.getChildren
        if len(children)>=1:
            for ch in children:
                if ch.getComponent.get_type == 'NN':
                    ch.setTranslated(True)
                    chname = ch.getComponent.get_component
                    if '.' in chname:
                        self.__query.groupby.set_column(chname)
                        self.__query.select.addcolumn(chname)
                        table = chname.split('.')[0]
                        self.__query.fromq.addtable(table)
        else:
            parent = node.getParent
            if (parent.getComponent.get_type == 'NN'):
                parent.setTranslated(True)
                chname = parent.getComponent.get_component
                if '.' in chname:
                    self.__query.groupby.set_column(chname)
                    self.__query.select.addcolumn(chname)
                    table = chname.split('.')[0]
                    self.__query.fromq.addtable(table)
            else:
                print("Failure")

    def translateOR(self, node):
        self.__query.orderby.set_type(node.getComponent.get_component)
        node.setTranslated(True)
        children = node.getChildren
        if len(children)>=1:
            for ch in children:
                if ch.getComponent.get_type == 'NN':
                    ch.setTranslated(True)
                    chname = ch.getComponent.get_component
                    if '.' in chname:
                        self.__query.orderby.set_column(chname)
                        self.__query.select.addcolumn(chname)
                        table = chname.split('.')[0]
                        self.__query.fromq.addtable(table)
                    else:
                        self.__query.orderby.set_column('*')
                        self.__query.fromq.addtable(chname)
        else:
            parent = node.getParent
            if (parent.getComponent.get_type == 'NN'):
                parent.setTranslated(True)
                chname = parent.getComponent.get_component
                if '.' in chname:
                    self.__query.function.set_column(chname)
                    self.__query.select.addcolumn(chname)
                    table = chname.split('.')[0]
                    self.__query.fromq.addtable(table)
                else:
                    self.__query.function.set_column('*')
                    self.__query.fromq.addtable(chname)
            else:
                print("Failure")

    def translateNN(self, node):
        node.setTranslated(True)
        chname = node.getComponent.get_component
        if '.' in chname:
            self.__query.select.addcolumn(chname)
            table = chname.split('.')[0]
            self.__query.fromq.addtable(table)
        else:
            self.__query.fromq.addtable(chname)

    def translateVN(self, node):
        if node.getParent.getComponent.get_type == 'ON':
            return
        for ch in node.getChildren:
            if ch.getComponent.get_type == 'ON':
                return
        cond = Condition(node.getComponent.get_component, "=", value=node.getWord.get_text())
        self.__query.where.addcondition(cond)
        chname = node.getComponent.get_component
        if '.' in chname:
            table = chname.split('.')[0]
            self.__query.fromq.addtable(table)