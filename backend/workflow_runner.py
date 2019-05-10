import backend.workflow as workflow

import sys
import threading
import trace
import time
import kthread
import multiprocessing
import json

from flask import Response
from enum import Enum
from typing import Callable, List

class Module(Enum):
    mod0=1
    mod1a=2
    mod1e=3
    mod1b1=4

def mod0(mondo_id):
    return workflow.mod0_disease_lookup(mondo_id)

class WorkflowRunner(object):
    def __init__(self):
        pass

    def run(self, mondo_id:str, module:Module):
        if module is Module.mod0:
            return self._build_response(module, lambda: workflow.mod0_disease_lookup(mondo_id))
        elif module is Module.mod1a:
            return self._build_response(module, lambda: workflow.mod1a_functional_similarity(workflow.mod0_disease_lookup(mondo_id)))
        elif module is Module.mod1e:
            return self._build_response(module, lambda: workflow.mod1e_gene_interactions(workflow.mod0_disease_lookup(mondo_id)))
        elif module is Module.mod1b1:
            return self._build_response(module, lambda: workflow.mod1b1_phenotype_similarity(workflow.mod0_disease_lookup(mondo_id)))
        else:
            raise Exception('Invalid module: {}'.format(module))

    def _build_response(self, module:Module, run_module:Callable[[str], List]):
        """
        Builds a streaming response that will keep the connection to the client
        open and, if that connection breaks, will terminate the process executing
        run_module.
        """
        finished = multiprocessing.Event()

        def work(finished, connection):
            print('worker {} started'.format(module))
            try:
                connection.send(run_module())
            finally:
                finished.set()

        parent_connection, child_connection = multiprocessing.Pipe()
        process = multiprocessing.Process(target=work, args=(finished, child_connection,))
        process.start()

        def stream():
            try:
                """
                If this throws an exception then we know the connection to the
                client has closed, and we should terminate the process.
                """
                while not finished.wait(timeout=1):
                    yield '.'
                if parent_connection.poll():
                    yield json.dumps(parent_connection.recv())
            finally:
                parent_connection.close()
                child_connection.close()
                process.terminate()
                print('worker {} terminated: {}'.format(module, process.is_alive()))
                return

        return Response(stream(), mimetype='application/json')
