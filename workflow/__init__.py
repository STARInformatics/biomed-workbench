"""
This module sets up endpoints for querying the modules of workflow2. The modules
can take a very long time to run, and so I designed this module to run modules
in their own process and then terminate that process if connection breaks. We do
not want to waste resources by running modules when the answer will not be
returned to the user.

The solution is hacky. We stream back empty strings and if the connection
breaks then an exception is thrown the next time we yield an empty string. We
then catch this exception, and attempt to terminate the process running the
requested module. If the module finishes without connection being broken, then
we yield the whole response and finish the stream.

The module can be run directly:
    python -m workflow
"""


from flask import Flask, Response
from enum import Enum

import json
import multiprocessing

app = Flask(__name__)
logger = multiprocessing.get_logger()
pool = None

class Module(Enum):
    mod0=1
    mod1a=2
    mod1e=3
    mod1b1=4

def work(mondo_id:str, module:Module, finished:multiprocessing.Event, queue:multiprocessing.Queue) -> None:
    logger.info('started {} {}'.format(module, multiprocessing.current_process()))
    try:
        import workflow.module as workflow

        result = None

        if module is Module.mod0:
            result = workflow.mod0_disease_lookup(mondo_id)
        elif module is Module.mod1a:
            result = workflow.mod1a_functional_similarity(workflow.mod0_disease_lookup(mondo_id))
        elif module is Module.mod1e:
            result = workflow.mod1e_gene_interactions(workflow.mod0_disease_lookup(mondo_id))
        elif module is Module.mod1b1:
            result = workflow.mod1b1_phenotype_similarity(workflow.mod0_disease_lookup(mondo_id))
        else:
            raise Exception('Invalid module: {}'.format(module))

        queue.put(result)
    finally:
        finished.set()

def build_worker(mondo_id:str, module:Module) -> Response:
    queue = multiprocessing.Queue()
    finished = multiprocessing.Event()
    process = multiprocessing.Process(target=work, args=(mondo_id, module, finished, queue))
    process.start()

    def stream():
        try:
            """
            If this throws an exception then we know the connection to the
            client has closed, and we should terminate the process.
            """
            while not finished.wait(timeout=1):
                yield ''
            if not queue.empty():
                yield json.dumps(queue.get_nowait())
        finally:
            process.terminate()
            logger.info('terminated {} {}: {}'.format(module, multiprocessing.current_process(), process.is_alive()))

    return Response(stream(), mimetype='application/json')

@app.route('/api/workflow/mod0/<string:mondo_id>')
def mod0(mondo_id:str) -> Response:
    return build_worker(mondo_id, Module.mod0)

@app.route('/api/workflow/mod1a/<string:mondo_id>')
def mod1a(mondo_id:str) -> Response:
    return build_worker(mondo_id, Module.mod1a)

@app.route('/api/workflow/mod1b1/<string:mondo_id>')
def mod1b1(mondo_id:str) -> Response:
    return build_worker(mondo_id, Module.mod1b1)

@app.route('/api/workflow/mod1e/<string:mondo_id>')
def mod1e(mondo_id:str) -> Response:
    return build_worker(mondo_id, Module.mod1e)

def run():
    """
    Runs the flask app
    """
    process_count = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=process_count) as _pool:
        pool = _pool
        app.run(port=8080)

if __name__=='__main__':
    run()
