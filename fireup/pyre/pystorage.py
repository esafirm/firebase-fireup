from . import common

from gcloud.storage import bucket
from gcloud import storage
import requests

try:
    from urllib.parse import quote
except:
    from urllib import quote


class Storage:
    """ Firebase Storage Service """

    def __init__(self, credentials, storage_bucket, requests):
        self.storage_bucket = "https://firebasestorage.googleapis.com/v0/b/" + storage_bucket
        self.credentials = credentials
        self.requests = requests
        self.path = ""
        if credentials:
            self.client = storage.Client(credentials=credentials, project=storage_bucket)
            self.bucket = self.client.get_bucket(storage_bucket)

    def child(self, *args):
        new_path = "/".join(args)
        if self.path:
            self.path += "/{}".format(new_path)
        else:
            if new_path.startswith("/"):
                new_path = new_path[1:]
            self.path = new_path
        return self

    def put(self, file, token=None):
        # reset path
        path = self.path
        self.path = None
        if isinstance(file, str):
            file_object = open(file, 'rb')
        else:
            file_object = file
        request_ref = self.storage_bucket + "/o?name={0}".format(path)
        if token:
            headers = {"Authorization": "Firebase " + token}
            request_object = self.requests.post(request_ref, headers=headers, data=file_object)
            common.raise_detailed_error(request_object)
            return request_object.json()
        elif self.credentials:
            blob = self.bucket.blob(path)
            if isinstance(file, str):
                return blob.upload_from_filename(filename=file)
            else:
                return blob.upload_from_file(file_obj=file)
        else:
            request_object = self.requests.post(request_ref, data=file_object)
            common.raise_detailed_error(request_object)
            return request_object.json()

    def delete(self, name):
        self.bucket.delete_blob(name)

    def download(self, filename, token=None):
        # remove leading backlash
        path = self.path
        url = self.get_url(token)
        self.path = None
        if path.startswith('/'):
            path = path[1:]
        if self.credentials:
            blob = self.bucket.get_blob(path)
            blob.download_to_filename(filename)
        else:
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)

    def get_url(self, token):
        path = self.path
        self.path = None
        if path.startswith('/'):
            path = path[1:]
        if token:
            return "{0}/o/{1}?alt=media&token={2}".format(self.storage_bucket, quote(path, safe=''), token)
        return "{0}/o/{1}?alt=media".format(self.storage_bucket, quote(path, safe=''))

    def list_files(self, prefix):
        return self.bucket.list_blobs(prefix=prefix)
