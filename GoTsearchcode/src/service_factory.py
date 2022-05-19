from src.resources.mongodb_data_service import MongoDBDataService
from src.resources.neo4j_data_service import Neo4jDataService
from src.resources.seasons_resource import SeasonsResource
import dns

class MongoDBDataServiceConfig:

    def __init__(self, db_url, db_name):
        self.db_url = db_url
        self.db_name = db_name


class Neo4jDataServiceConfig:

    def __init__(self, db_url, auth):
        self.db_url = db_url
        self.auth = auth


class SeasonsResourceConfig:

    def __init__(self, data_service, collection_name):
        self.data_service = data_service
        self.collection_name = collection_name


class ServiceFactory:

    def __init__(self):

        self.mongo_db_svc_config = \
            MongoDBDataServiceConfig(
                "mongodb://sa3883:Dkstmdwns011001@cluster0-shard-00-00.2xeqe.mongodb.net:27017,"    
                "cluster0-shard-00-01.2xeqe.mongodb.net:27017,"
                "cluster0-shard-00-02.2xeqe.mongodb.net:27017/GoT?ssl=true&replicaSet=atlas-xl16ms-shard"
                "-0&authSource=admin&retryWrites=true&w=majority",
                "GoT"
            )
        self.mongo_db_service = MongoDBDataService(self.mongo_db_svc_config)
        self.seasons_service_config = SeasonsResourceConfig(self.mongo_db_service, "episodes")
        self.seasons_resource = SeasonsResource(self.seasons_service_config)

        self.neo_url = "neo4j+s://49c116b0.databases.neo4j.io:7687"
        self.neo_auth = ("neo4j", "VFLNhvEccOtCymemeMwPiyaghv7sd78-4UwLSLWBdpE")

        self.neo4j_db_svc_config = Neo4jDataServiceConfig(self.neo_url, self.neo_auth)
        self.neo4j_db_service =  Neo4jDataService(self.neo4j_db_svc_config)


    def get(self, resource_name, default):
        if resource_name != "seasons":
            self.seasons_service_config = SeasonsResourceConfig(self.mongo_db_service, resource_name)
            self.seasons_resource = SeasonsResource(self.seasons_service_config)
            result = self.seasons_resource
        else:
            result = self.seasons_resource

        return result



