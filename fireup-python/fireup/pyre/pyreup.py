from .pystorage import Storage

import requests
import firebase_admin

from firebase_admin import credentials
from requests.packages.urllib3.contrib.appengine import is_appengine_sandbox
from requests_toolbelt.adapters import appengine


def initialize_app(config):
    return Firebase(config)


class Firebase:
    """ Firebase Interface """

    def __init__(self, config):

        self.api_key = config["apiKey"]
        self.auth_domain = config["authDomain"]
        self.database_url = config["databaseURL"]
        self.storage_bucket = config["storageBucket"]
        self.credentials = None
        self.requests = requests.Session()

        if config.get("serviceAccount"):
            service_account_type = type(config["serviceAccount"])
            if service_account_type is str:
                self.credentials = credentials.Certificate(config["serviceAccount"])
            else:
                raise Exception('service account must be a path to the json file')

        # Initialize the Firebase Admin
        firebase_admin.initialize_app(self.credentials, {
            'storageBucket': self.storage_bucket
        })

        if is_appengine_sandbox():
            # Fix error in standard GAE environment
            # is releated to https://github.com/kennethreitz/requests/issues/3187
            # ProtocolError('Connection aborted.', error(13, 'Permission denied'))
            adapter = appengine.AppEngineAdapter(max_retries=3)
        else:
            adapter = requests.adapters.HTTPAdapter(max_retries=3)

        for scheme in ('http://', 'https://'):
            self.requests.mount(scheme, adapter)

    def storage(self):
        return Storage(self.storage_bucket, self.requests)
