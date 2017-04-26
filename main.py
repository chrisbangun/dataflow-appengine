mport logging

from apache_beam.utils import processes

from recsys_data_pipeline.common.tableLoader import TableLoader
from recsys_data_pipeline.ingestion import IngestionToBigQuery
from recsys_data_pipeline.common.configReader import ConfigReader

from flask import Flask
from flask import request

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.config['DEBUG'] = False

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/halo')
def index():
	return 'Main Page', 200


@app.route('/launchdfjob', methods=['GET', 'POST'])
def launch_df_job():
    logging.getLogger().setLevel(logging.INFO)    	
    config = ConfigReader('columbus-config')  # TODO read from args
    tables = TableLoader('experience')
    ingestor = IngestionToBigQuery(config.configuration, tables.list_of_tables)
    ingestor.ingest_table()
    return 'OK', 200


@app.route('/print-access-token')
def print_access_token():
    gcloud_process = processes.Popen(['gcloud', 'auth', 'print-access-token'], stdout=processes.PIPE)
    output, _ = gcloud_process.communicate()
    return 'token="{}"'.format(output.strip()), 200


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
