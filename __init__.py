def classFactory(iface):
    from .ArcGisAttachmentsReader import ArcGisAttachmentsReader
    return ArcGisAttachmentsReader(iface)