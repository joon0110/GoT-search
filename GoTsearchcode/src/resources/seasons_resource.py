from src.resources.base_resource import BaseResource

class SeasonsResource(BaseResource):
    def __init__(self, config):
        super().__init__(config)
        self.data_service = None

    def _get_project_fields(self, scenes):

        if scenes:
            result = set([
                "seasonNum", "episodeNum", "sceneNum", "sceneLocation", "sceneSubLocation", "sceneStart", "sceneEnd"
            ])

        else:
            result = set([
                "seasonNum", "episodeNum", "episodeTitle", "episodeAirDate", "episodeDescription", "scenes"
            ])
        return result

    def get_full_collection_name(self):
        return self.config.collection_name

    def _map_template(self, in_template):
        if in_template is None:
            result = in_template
        else:
            new_template = {}
            for k, v in in_template.items():
                if k in ["seasonNum", "episodeNum", "sceneNum"]:
                    v = int(v)
                new_template[k] = v
            result = new_template

        return result

    def get_by_template(self,
                        relative_path=None,
                        path_parameters=None,
                        template=None,
                        field_list=None,
                        limit=None,
                        offset=None,
                        order_by=None,
                        scenes=None
                        ):
        if field_list:
            full_field_list = self._get_project_fields(False).intersection(set(field_list))
        elif scenes:
            full_field_list = self._get_project_fields(True)
        else:
            full_field_list = self._get_project_fields(False)

        final_template = self._map_template(template)

        result = super().get_by_template(relative_path, path_parameters, final_template, full_field_list, limit, offset, order_by)

        return result

    def get_data_service(self):
        if self.data_service is None:
            self.data_service = self.config.data_service
        return self.data_service

    def get_resource_by_id(self, seasonNum, episodeNum, sceneNum):
        if seasonNum and episodeNum and sceneNum:
            template = {'seasonNum': seasonNum, 'episodeNum': episodeNum, 'sceneNum': sceneNum}
            result = self.get_by_template(template=template, scenes=True)
        elif seasonNum and episodeNum and not sceneNum:
            template = {'seasonNum': seasonNum, 'episodeNum': episodeNum}
            result = self.get_by_template(template=template, scenes=False)
        elif seasonNum and not episodeNum and not sceneNum:
            template = {'seasonNum': seasonNum}
            result = self.get_by_template(template=template, scenes=False)

        return result

    def create(self, view_name, source_name, seasonNum, episodeNum):
        result = super().create(view_name, source_name, seasonNum, episodeNum)
        return result