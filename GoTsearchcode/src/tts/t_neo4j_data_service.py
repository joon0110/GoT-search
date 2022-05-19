from src import service_factory
import json

s_factory = service_factory.ServiceFactory()


def get_neo4j_svc():
    return s_factory.neo4j_db_service


def t1():
    sv = get_neo4j_svc()
    sv = list(sv.list_resources())
    print("t1 resources: ", json.dumps(sv, indent=2, default=str))

def t2():
     sv = get_neo4j_svc()

     f = {"seasonNum": 1}
     p = ["episodeNum", "episodeTitle", "episodeAirDate"]
     res = sv.get_by_template("", f, p)
     print("t2 result: ", json.dumps(res, indent=2, default=str))

if __name__ == "__main__":
    #get_neo4j_svc()
    t1()
    #t2()

