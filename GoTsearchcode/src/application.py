from flask import Flask, Response, request
from flask_cors import CORS
import json
from datetime import datetime
import pymongo
from src.tts.t_neo4j_data_service import get_neo4j_svc

from service_factory import ServiceFactory

import rest_utils

app = Flask(__name__)
CORS(app)

service_factory = ServiceFactory()

##################################################################################################################

# DFF TODO A real service would have more robust health check methods.
# This path simply echoes to check that the app is working.
# The path is /health and the only method is GETs
@app.route("/health", methods=["GET"])
def health_check():
    rsp_data = {"status": "healthy", "time": str(datetime.now())}
    rsp_str = json.dumps(rsp_data)
    rsp = Response(rsp_str, status=200, content_type="application/json")
    return rsp


# TODO Remove later. Solely for explanatory purposes.
# The method take any REST request, and produces a response indicating what
# the parameters, headers, etc. are. This is simply for education purposes.
#
@app.route("/api/demo/<parameter1>", methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/api/demo/", methods=["GET", "POST", "PUT", "DELETE"])
def demo(parameter1=None):
    """
    Returns a JSON object containing a description of the received request.

    :param parameter1: The first path parameter.
    :return: JSON document containing information about the request.
    """

    # DFF TODO -- We should wrap with an exception pattern.
    #

    # Mostly for isolation. The rest of the method is isolated from the specifics of Flask.
    inputs = rest_utils.RESTContext(request, {"parameter1": parameter1})

    # DFF TODO -- We should replace with logging.
    r_json = inputs.to_json()
    msg = {
        "/demo received the following inputs": inputs.to_json()
    }
    print("/api/demo/<parameter> received/returned:\n", msg)

    rsp = Response(json.dumps(msg), status=200, content_type="application/json")
    return rsp

##################################################################################################################


@app.route('/')
def hello_world():
    return '<u>Hello World. Recitation rocks!</u>'


@app.route('/api/<resource_collection>', methods=['GET', 'POST'])
def do_resource_collection(resource_collection):
    """
    1. HTTP GET return all resources.
    2. HTTP POST with body --> create a resource, i.e --> database.
    :return:
    """
    request_inputs = rest_utils.RESTContext(request, resource_collection)

    svc = service_factory.get(resource_collection, None)

    if request_inputs.method == "GET":
        """ res = svc.get_by_template(
                        relative_path=None,
                        path_parameters=None,
                        template=None,
                        field_list=None,
                        limit=None,
                        offset=None,
                        order_by=None):
        """
        res = svc.get_by_template(
            template=request_inputs.args,
            field_list=request_inputs.fields
        )

        # res = request_inputs.add_pagination(res)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

    elif request_inputs.method == "POST":
        raise NotImplementedError("Did not implement POST")
    else:
        rsp = Response("NOT IMPLEMENTED", status=501, content_type="text/plain")

    return rsp


@app.route('/api/<resource_collection>/<resource_id>', methods=['GET', 'PUT', 'DELETE'])
def specific_resource(resource_collection, resource_id):
    """
    1. Get a specific one by ID.
    2. Update body and update.
    3. Delete would ID and delete it.
    :param user_id:
    :return:
    """
    request_inputs = rest_utils.RESTContext(request, resource_collection)
    svc = service_factory.get(resource_collection, None)

    if request_inputs.method == "GET":
        res = svc.get_resource_by_id(resource_id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    elif request_inputs.method == "PUT":
        new_values = request_inputs.data
        print(new_values)
    else:
        rsp = Response("NOT IMPLEMENTED", status=501, content_type="text/plain")
    return rsp



@app.route('/seasons', methods=['GET'])
def seasons():
    request_inputs = rest_utils.RESTContext(request, "seasons")
    svc = service_factory.get("seasons", None)

    cleanedOutput = []
    result = svc.get_by_template(template=request_inputs.args, field_list=request_inputs.fields)

    for episode in result:
        cleanedOutput.append(str(episode["seasonNum"]) + " " + str(episode["episodeNum"]) + " " + episode["episodeTitle"] + " " + episode["episodeAirDate"])
    rsp = Response(json.dumps(cleanedOutput, default=str), status=200, content_type="application/json")

    return rsp

@app.route('/seasons/<seasonNum>', methods=['GET'])
def sea_num(seasonNum=None):
    svc = service_factory.get("seasons", None)

    cleanedOutput = []
    result = svc.get_resource_by_id(seasonNum, None, None)

    for episode in result:
        cleanedOutput.append(str(episode["seasonNum"]) + " " + str(episode["episodeNum"]) + " " + episode["episodeTitle"] + " " + episode["episodeAirDate"])
    rsp = Response(json.dumps(cleanedOutput, default=str), status=200, content_type="application/json")

    return rsp

@app.route('/seasons/<seasonNum>/episodes', methods=['GET'])
def sea_num_epi(seasonNum=None):
    request_inputs = rest_utils.RESTContext(request, "seasons")
    svc = service_factory.get("seasons", None)

    cleanedOutput = []
    t= {"seasonNum": seasonNum}
    new_t = {**t, **request_inputs.args}

    result = svc.get_by_template(template=new_t, field_list=request_inputs.fields)

    for episode in result:
        cleanedOutput.append(
            str(episode["seasonNum"]) + " " + str(episode["episodeNum"]) + " " + episode["episodeTitle"] + " " +
            episode["episodeAirDate"])

    rsp = Response(json.dumps(cleanedOutput, default=str), status=200, content_type="application/json")

    return rsp

@app.route('/seasons/<seasonNum>/episodes/<episodeNum>', methods=['GET'])
def sea_num_epi_num(seasonNum=None, episodeNum=None):
    svc = service_factory.get("seasons", None)

    cleanedOutput = []
    result = svc.get_resource_by_id(seasonNum, episodeNum, None)

    for episode in result:
        cleanedOutput.append(
            str(episode["seasonNum"]) + " " + str(episode["episodeNum"]) + " " + episode["episodeTitle"] + " " +
            episode["episodeAirDate"])
    rsp = Response(json.dumps(cleanedOutput, default=str), status=200, content_type="application/json")

    return rsp

@app.route('/seasons/<seasonNum>/episodes/<episodeNum>/scenes', methods=['GET'])
def sea_num_epi_num_sce(seasonNum=None, episodeNum=None):
    request_inputs = rest_utils.RESTContext(request, "seasons")
    svc = service_factory.get("seasons", None)

    cleanedOutput = []
    t = {'seasonNum': seasonNum, 'episodeNum': episodeNum}

    result = svc.get_by_template(template=t, field_list=request_inputs.fields)

    for episode in result:
        cleanedOutput.append(
            str(episode["seasonNum"]) + " " + str(episode["episodeNum"]) + " " + episode["episodeTitle"] + " " +
            episode["episodeAirDate"] + " " + str(episode["scenes"]))

    rsp = Response(json.dumps(cleanedOutput, default=str), status=200, content_type="application/json")

    return rsp

@app.route('/seasons/<int:seasonNum>/episodes/<int:episodeNum>/scenes/<int:sceneNum>', methods=['GET'])
def sea_num_epi_num_sce_num(seasonNum=None, episodeNum=None, sceneNum=None):
    request_inputs = rest_utils.RESTContext(request, "seasons")
    svc = service_factory.get("seasons", None)

    if request_inputs.method == "GET":
        try:
            svc.create("seasonNumber" + str(seasonNum) + "episodeNumber" + str(episodeNum) + "scenes", "episodes", seasonNum, episodeNum)
        except pymongo.errors.OperationFailure:
            pass
        finally:
            svc = service_factory.get("seasonNumber" + str(seasonNum) + "episodeNumber" + str(episodeNum) + "scenes", None)
            res = svc.get_resource_by_id(seasonNum, episodeNum, sceneNum)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

    return rsp

@app.route('/person', methods=['GET'])
def person():
    svc = get_neo4j_svc()
    q = "MATCH (Person:Person) RETURN Person"
    result = svc.run_query(q)
    rsp = Response(json.dumps(result, default=str), status=200, content_type="application/json")
    return rsp

@app.route('/movie', methods=['GET'])
def movie():
    request_inputs = rest_utils.RESTContext(request, "movie")
    svc = get_neo4j_svc()

    if request_inputs.method == "GET":
        dict_string = ''
        if request_inputs.args:
            dict_string = "{"
            for i, k in enumerate(request_inputs.args):
                dict_string += k + ":"
                dict_string += "\"" + request_inputs.args[k] + "\""
                if i != len(request_inputs.args) - 1:
                    dict_string += ","
                dict_string += "}"
        q = "MATCH (Movie:Movie" + dict_string + ") RETURN Movie"
        result = svc.run_query(q)
        rsp = Response(json.dumps(result, default=str), status=200, content_type="application/json")

    return rsp

@app.route('/person/<name>/acted_in', methods=['GET'])
def person_name_acted_in(name):
    svc = get_neo4j_svc()
    q = "MATCH Person=({name:\'" + name + "\'})-[ACTED_IN]->(Movie) RETURN Movie"
    result = svc.run_query(q)
    rsp = Response(json.dumps(result, default=str), status=200, content_type="application/json")

    return rsp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
