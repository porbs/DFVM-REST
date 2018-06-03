from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

import os
import subprocess
import json
import pathlib
from uuid import uuid4

@api_view(['POST'])
def process_graph(request):
    backend_node_path = os.path.join(os.getcwd(), 'dfvm_node_backend.exe')
    data = json.loads(request.body.decode('ascii'))
    storage_path = os.path.join(os.getcwd(), 'storage')
    pathlib.Path(storage_path).mkdir(parents=True, exist_ok=True)

    file_name = str(uuid4()) + '.json'
    computing_graph_path = os.path.join(storage_path, file_name)

    with open(computing_graph_path, 'w') as f:
        json.dump(data, f)

    print()
    proc = subprocess.run([backend_node_path, computing_graph_path], stdout=subprocess.PIPE)
    stdout = proc.stdout.decode('ascii')
    result = dict()
    result[data["outputs"][0]['name']] = stdout[stdout.rfind(':') + 1:].strip()

    return JsonResponse(result, safe=False, status=status.HTTP_200_OK)