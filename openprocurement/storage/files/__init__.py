from openprocurement.storage.files.storage import FilesStorage


def includeme(config):
    settings = config.registry.settings

    config.registry.storage = FilesStorage(settings)
