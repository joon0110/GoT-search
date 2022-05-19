#
# DFF TODO: Accessing database directly from resource is an anti-pattern.
# You did not learn this from me.
#
from src.resources.base_data_service import BaseDataService
from py2neo import Graph
import json


class Neo4jDataService(BaseDataService):

    def __init__(self, config_info):
        super().__init__(config_info)

    def _get_connection(self):
        """
        :return:
        """
        if self.connection is None:
            db_url = self.config_info.db_url
            auth = self.config_info.auth
            self.connection = Graph(db_url, auth = auth)

        return self.connection

    def _close_connection(self):
        """

        :return:
        """
        pass

    def _get_collection(self, collection_name):
        conn = self._get_connection()
        db = self._get_db()
        coll = db[collection_name]
        return coll

    def _get_db(self):
        conn = self._get_connection()
        result = conn[self.confg_info.db_name]
        return result

    def get_by_template(self,
                        collection_name,
                        template=None,
                        field_list=None
                        ):
            """
            project_c = None
            if field_list:
                project_c = dict()
                for f in field_list:
                    project_c[f] = 1

            coll = self._get_collection(collection_name)
            result = coll.find(template, project_c)
            result = list(result)

            return result
            """

            q = "MATCH (n) RETURN distinct labels(n)"
            conn = self._get_collection(collection_name)
            result = conn.find(template,q)
            result = list(result)
            return result


    def list_resources(self):
        q = "MATCH (n) RETURN distinct labels(n)"
        conn = self._get_connection()
        result = conn.run(q)
        result = result.data()

        return result

    def run_query(self, query):
        conn = self._get_connection()
        result = conn.run(query)
        result = result.data()
        return result