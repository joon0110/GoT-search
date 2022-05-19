from src.resources.base_resource import BaseResource


class EpisodesResource(BaseResource):

    def __init__(self, config):
        super().__init__(config)
        self.data_service = None

    def _get_project_fields(self):

        result = []
        return result

    def _map_template(self, in_template):
        if in_template is None:
            result = in_template
        else:
            new_template = {}
            for k, v in in_template.items():
                if k in ["seasonNum", "epdisodeNum"]:
                    v = int(v)
                new_template[k] = v
            result = new_template
        return result

    def get_full_collection_name(self):
        return self.config.collection_name

    def get_by_template(self,
                        relative_path=None,
                        path_parameters=None,
                        template=None,
                        field_list=None,
                        limit=None,
                        offset=None,
                        order_by=None):
        pass

    def get_data_service(self):

        if self.data_service is None:
            self.data_service = self.config.data_service
        return self.data_service

    def get_resource_by_id(self, id):
        pass

    def get_full_table_name(self):
        pass

    def create(self, new_resource):
        pass

    def update_resource_by_id(self, id, new_values):
        pass

    def delete_resource_by_id(self, id):
        pass
