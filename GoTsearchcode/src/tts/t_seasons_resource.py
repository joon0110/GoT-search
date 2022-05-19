from src import service_factory
import json

s_factory = service_factory.ServiceFactory()


def get_seasons_resource():
    return s_factory.seasons_resource


def t1():
    s = get_seasons_resource()
    print("t1: s = ", s)


def t2():
    s = get_seasons_resource()
    f = {"seasonNum": 1}
    res = s.get_by_template(template=f)
    print("t2: res = \n", json.dumps(res, indent=2, default=str))


def t3():
    s = get_seasons_resource()
    f = {"seasonNum": 1}
    res = s.get_by_template(template=f)
    print("t2: res = \n", json.dumps(res, indent=2, default=str))

if __name__ == "__main__":
    #get_seasons_resource()
    #t1()
    t2()
