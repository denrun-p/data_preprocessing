""" Base Class for all Steps.

Steps are defined with a dictionary. Each step requires a key ('type'). The
type defines which step to use. Steps are used in the processing pipeline.
There are data loaders and normalize_text steps.
"""

import hashlib

from data_preprocessing.utils.logger import setup_logging


class Steps:
    """ Base Steps Class.

    Args:
        config (obj): config for the step
    """
    def __init__(self, config):
        """Initialize steps base class."""
        self.config = config
        self.log = self._logger()
        self.log.info("Initializing {} step".format(config.get('type')))

    def item_model(self, item):
        """Format each record into a standard item format.

        Each incoming record needs to be converted into the item model. The
        item model is a dictionary with three keys, id, data and tags.

        Args:
            item (dict): Dictionary containing the data
        Returns:
            dict: Containing the proper item format

        Example:
            .. code-block::

                from data_preprocessing.steps.base import Steps

                config = {
                    "name": "normalize_text",
                    "type": "lowercase",
                    "log_level": "DEBUG"
                }
                step = Steps(config)

                record = "this is a test"
                record = step.item_model(record)
                print(record)
        """
        if isinstance(item, str):
            item = {
                "data": item
            }
        if not isinstance(item, dict):
            self.log.error("Item is not in the correct format")
            return {}

        if "data" not in item.keys():
            self.log.error("Item is missing the data key")
            return {}

        formatted_item = {
            "id": "",
            "data": item["data"],
            "tags": {}
        }
        if not item.get("id"):
            formatted_item["id"] = self._create_id(item["data"])
        else:
            formatted_item["id"] = item["id"]

        return formatted_item

    def _create_id(self, text):
        """Create unique id from text.

        Args:
            text (str): Text for the item
        Returns:
            str: Id created from hashing the text
        """
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    def _logger(self):
        """Helper function to setup the logger."""
        log = setup_logging(
            self.config["type"],
            self.config.get("log_level")
        )
        return log
