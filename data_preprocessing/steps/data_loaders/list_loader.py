"""Process data from a list.

This data loader processes data from an in memory list, formats the data to the
item model and processes through the data preprocessing pipeline. An id is
generated by hashing the text.

Example:
    .. code-block::

        # Example: Stand Alone
        from data_preprocessing.steps.data_loaders import list_loader

        config = {
            "data_loader": {
                "type": "list",
                "batch_size": 1000,
                "log_level": "INFO"
            },
            "steps": [
                {
                    "name": "normalize_text",
                    "type": "lowercase",
                    "log_level": "INFO"
                },
            ]
        }

        loader = list_loader.ListDataLoader(config["data_loader"])
        data = ['Process This Data']
        for item in loader.process(data):
            print(item)
            break

        # Example: Using the pipeline
        from data_preprocessing.base import DataPreprocess

        loader = DataPreprocess(config, log_level='INFO')

        for batch in loader.process_data(data):
            print(batch)
            break

"""

from data_preprocessing.steps.base import Steps


class ListDataLoader(Steps):
    """List Data Loader class.

    Args:
        config (json): Json object containing the configuration details

    Example:
        .. code-block::

            config = {
                "type": "list",
                "batch_size": 1000,
                "log_level": "INFO"
            }
    """
    def __init__(self, config):
        super().__init__(config)

    def process(self, data):
        """ Process list of data.
        
        Transform into a valid item and yield the item.

        Args:
            data (list): data to process
        Yields:
            obj: item
        """

        if not isinstance(data, list):
            self.log.error("Bad data type passed to list loader")
            raise TypeError("Data must be a list!")

        for item in data:
            if isinstance(item, dict) or isinstance(item, list):
                self.log.warn("Skipping item bad format- {}".format(item))
                continue
            item = {
                "data": item
            }
            yield self.item_model(item)
