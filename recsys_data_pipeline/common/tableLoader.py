#!/usr/bin/env python

import os

import yaml

from table import Tables


class TableLoader(object):

    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.list_of_tables = self.__get_tables(dataset_name)

    def __get_tables(self, dataset_name):
        config_file = self.path_from_here('../config/tables.yaml')
        with open(config_file) as f:
            dataset = yaml.load(f)

        tables = dataset[dataset_name]
        list_of_tables = []

        for table in tables['tables']:
            source_schema = table['source_schema']
            table_name = table['table_name']
            columns = table['columns']
            new_table_object = Tables(dataset_name, source_schema, table_name, columns)
            list_of_tables.append(new_table_object)

        return list_of_tables

    def path_from_here(self, path):
        return os.path.join(os.path.dirname(__file__), path)