from src import service_factory
import json

s_factory = service_factory.ServiceFactory()


def get_mongo_svc():
    return s_factory.mongo_db_service


def t1():
    sv = get_mongo_svc()
    sv = list(sv.list_resources())
    print("MongoDBs: ", json.dumps(sv, indent=2, default=str))


def t2():
    sv = get_mongo_svc()

    f = {"seasonNum": 1}
    p = ["episodeTitle", "episodeDescription", "episodeAirDate"]
    res = sv.get_by_template("episodes", f, p)
    print("t2 result: ", json.dumps(res, indent=2, default=str))

def create_scene_view():

    sv = get_mongo_svc()

    pipeline = [{
        '$unwind': {
            'path': '$scenes',
            'includeArrayIndex': 'sceneNum'
        }
    }, {
        '$project': {
            'episodeNum': 1,
            'seasonNum': 1,
            'sceneNum': {
                '$add': [
                    '$sceneNum', 1
                ]
            },
            'sceneLocation': '$scenes.location',
            'sceneSubLocation': '$scenes.subLocation',
            'sceneStart': '$scenes.sceneStart',
            'sceneEnd': '$scenes.sceneEnd'
        }
    }
    ]

    res = sv.create_view("scenes", "episodes", pipeline)



if __name__ == "__main__":
    #get_mongo_svc()
    #t1()
    t2()
    #create_scene_view()
