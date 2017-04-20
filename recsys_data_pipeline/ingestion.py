#!/usr/bin/env python

import logging

import apache_beam as beam
from apache_beam.io import ReadFromAvro
from apache_beam.utils.pipeline_options import GoogleCloudOptions
from apache_beam.utils.pipeline_options import PipelineOptions
from apache_beam.utils.pipeline_options import SetupOptions
from apache_beam.utils.pipeline_options import StandardOptions

from common.tableLoader import TableLoader
from common.configReader import ConfigReader


class IngestionToBigQuery(object):

    def __init__(self, config, tables):
        self.config = config
        self.tables = tables
        self.pipeline = self.__init_pipeline()

    def __init_pipeline(self):
        pipeline_args = self.config['pipeline_args']
        options = PipelineOptions()
        google_cloud_options = options.view_as(GoogleCloudOptions)
        google_cloud_options.project = pipeline_args['project']
        google_cloud_options.job_name = pipeline_args['job_name']
        google_cloud_options.staging_location = pipeline_args['staging_location']
        google_cloud_options.temp_location = pipeline_args['temp_location']
        options.view_as(StandardOptions).runner = pipeline_args['runner']
        options.view_as(SetupOptions).setup_file = pipeline_args['setup_file']
        options.view_as(SetupOptions).save_main_session = True
        return beam.Pipeline(options=options)


    def __filter_columns(self, record, columns):
        return {col: record.get(col, '') for col in columns}

    def __run_ingestion(self, storage_input_path, columns, output_table):
        (self.pipeline
         | output_table + ': read table ' >> ReadFromAvro(storage_input_path)
         | output_table + ': filter columns' >> beam.Map(self.__filter_columns, columns=columns)
         | output_table + ': write to BigQuery' >> beam.Write(
            beam.io.BigQuerySink(output_table,
                                 create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,
                                 write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)))

    def ingest_table(self):
        bucket_name = self.config['gs_bucket']
        avro_prefix = self.config['final_avro_prefix']
        avro_suffix = self.config['final_avro_suffix']


        for table in self.tables:
            path_format = ('gs://{gs_bucket}{final_avro_prefix}'
                           '{source_schema}.{table_name}{final_avro_suffix}')

            gs_input_path = path_format.format(gs_bucket=bucket_name,
                                           final_avro_prefix=avro_prefix,
                                           final_avro_suffix=avro_suffix,
                                           source_schema=table.source_schema,
                                           table_name=table.table_name)

            self.__run_ingestion(gs_input_path, table.columns, table.output_table)

        self.pipeline.run().wait_until_finish()  #  block until pipeline completion


def main():
    logging.getLogger().setLevel(logging.INFO)
    config = ConfigReader('columbus-config')  #TODO read from args
    tables = TableLoader('experience')
    ingestor = IngestionToBigQuery(config.configuration, tables.list_of_tables)
    ingestor.ingest_table()

if __name__ == '__main__':
    main()
