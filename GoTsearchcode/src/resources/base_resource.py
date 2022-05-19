from abc import ABC, abstractmethod

class BaseResource(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def get_full_collection_name(self):
        pass

    @abstractmethod
    def get_resource_by_id(self, id):
        """
        :param id: The 'primary key' of the resource instance relative to the collection.
        :return: The resource or None if not found.
        """
        pass

    @abstractmethod
    def get_data_service(self):
        pass

    def get_by_template(self,
                        relative_path=None,
                        path_parameters=None,
                        template=None,
                        field_list=None,
                        limit=None,
                        offset=None,
                        order_by=None,
                        ):
        """

        """

        if path_parameters is None:
            final_path_parameters = {}
        else:
            final_path_parameters = path_parameters

        if template is None:
            final_template = {}
        else:
            final_template = template

        full_tempate = {**final_path_parameters, **final_template}

        d_service = self.get_data_service()
        result = d_service.get_by_template(
            self.get_full_collection_name(),
            full_tempate,
            field_list
        )

        return result

    @abstractmethod
    def create(self, view_name, source_name, seasonNum, episodeNum):
        d_service = self.get_data_service()
        pipeline = [{
            '$unwind': {
                'path': '$scenes',
                'includeArrayIndex': 'sceneNum'
            }
        }, {
            '$project': {
                'episodeNum': episodeNum,
                'seasonNum': seasonNum,
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
        }]
        result = d_service.create_view(view_name, source_name, pipeline)
        return result