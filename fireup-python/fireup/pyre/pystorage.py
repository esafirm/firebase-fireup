from . import common

from firebase_admin import storage

try:
    from urllib.parse import quote
except:
    from urllib import quote


class Storage:
    """ Firebase Storage Service """

    def __init__(self, storage_bucket, requests):
        self.requests = requests
        self.path = ""
        self.bucket = storage.bucket()
        self.storage_bucket = "https://firebasestorage.googleapis.com/v0/b/" + storage_bucket

    def child(self, *args):
        new_path = "/".join(args)
        if self.path:
            self.path += "/{}".format(new_path)
        else:
            if new_path.startswith("/"):
                new_path = new_path[1:]
            self.path = new_path
        return self

    def put(self, file, chunk_size=None, token=None):
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
        else:
            blob = self.bucket.blob(path)

            # Workaround for slow internet speed when uploading big file
            if chunk_size:
                blob._chunk_size = chunk_size * 1024 * 1024  # 5 MB

            if isinstance(file, str):
                return blob.upload_from_filename(filename=file)
            else:
                return blob.upload_from_file(file_obj=file)

    def delete(self, name):
        self.bucket.delete_blob(name)

    def download(self, filename, token=None):
        # remove leading backlash
        path = self.path
        self.path = None
        if path.startswith('/'):
            path = path[1:]

        blob = self.bucket.get_blob(path)
        blob.download_to_filename(filename)

    def get_url(self, path):
        self.path = None
        if path.startswith('/'):
            path = path[1:]
        return "{0}/o/{1}?alt=media".format(self.storage_bucket, quote(path, safe=''))

    def list_files(self, prefix):
        return self.bucket.list_blobs(prefix=prefix)
