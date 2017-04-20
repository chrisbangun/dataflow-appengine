#!/usr/bin/env python


class Tables(object):

    def __init__(self, dataset, source_schema, table_name, columns):
        self.dataset = dataset
        self.source_schema = source_schema
        self.table_name = table_name
        self.columns = columns
        self.output_table = self.dataset+"."+self.table_name+"_test_copy"
