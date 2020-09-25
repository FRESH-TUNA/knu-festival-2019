from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.staticfiles.storage import ManifestFilesMixin

class MediaStorage(S3Boto3Storage):
    location = 'media'

    # def read_manifest(self):
    #     try:
    #         return super(ManifestStaticFilesStorage,self).read_manifest()
    #     except IOError:
    #         return None
    