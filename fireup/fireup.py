from fireup.pyre import pyreup

import argparse
import json
import os
from datetime import datetime

# Manually change this before uploading
IS_DEBUG = False
DEFAULT_CHUNK_SIZE = 2  # in MB


class FireUp:
    def __init__(self):
        self._storage = self.init_storage()

    def init_storage(self):
        config_file = os.environ["FIREUP_CONFIG"]
        if len(config_file) == 0 or not(os.path.exists(config_file)):
            raise Exception("Please set the config file path to FIREUP_CONFIG environment")

        file = open(config_file)
        config_json = json.load(file)
        file.close()

        config = {
            "apiKey": config_json["apiKey"],
            "storageBucket": config_json["storageBucket"],
            "authDomain": config_json["authDomain"],
            "databaseURL": config_json["databaseURL"],
            "serviceAccount": config_json["serviceAccount"]
        }

        firebase = pyreup.initialize_app(config)
        return firebase.storage()

    def upload(self, origin, dest, chunk=DEFAULT_CHUNK_SIZE, return_stdout=False):
        if not return_stdout:
            print("Uploading {} to {}...".format(origin, dest))

        self._storage.child(dest).put(origin, chunk)
        url = self.url(bucket_path=dest)

        print(url)
        return url

    def url(self, bucket_path):
        return self._storage.child('/').get_url(bucket_path)

    def list(self, path, expire):
        today = datetime.now().replace(tzinfo=None)
        blob = self._storage.list_files(prefix=path)

        filtered_list = []

        if expire is None:
            filtered_list = blob
        else:
            for b in blob:
                diff = today - b.updated.replace(tzinfo=None)
                if diff.days >= expire:
                    filtered_list.append(b)

        return filtered_list

    def delete(self, file_list):
        for f in file_list:
            self._storage.delete(name=f.name)
            print("{} deleted.".format(f.name))


def main():
    parser = argparse.ArgumentParser(description="Firebase storage management tools")

    subparser = parser.add_subparsers(help="Sub commands", dest="command")

    delete_parser = subparser.add_parser('delete', help="Delete files in firebase storage")
    delete_parser.add_argument("--path", dest="path", type=str, help="Delete path")
    delete_parser.add_argument("--expire", dest="expire", type=int,
                               help="Delete files with diff equal or more than expire")

    upload_parser = subparser.add_parser('upload', help="Upload file use --origin and --dest")
    upload_parser.add_argument("--origin", dest="origin", type=str, help="Origin file path. Ex: /home/test.apk")
    upload_parser.add_argument("--dest", dest="dest", type=str, help="Destination path. Ex: /apk/test.apk")
    upload_parser.add_argument("--chunk", dest="chunk", type=int, help="Optional. Chunk size in Mb")
    upload_parser.add_argument("--stdout", action="store_true", help="Return stdout mode")

    list_parser = subparser.add_parser('list', help="List files in --target dir")
    list_parser.add_argument("--path", dest="path", type=str, default="/", help="Path directory in Firebase storage")
    list_parser.add_argument("--expire", dest="expire", type=int,
                             help="List only files that modifier more than expire days")

    args = parser.parse_args()

    if IS_DEBUG:
        print("")
        print("=> Mode: {}".format(args))
        print("")

    fire = FireUp()

    if args.command == 'upload':
        fire.upload(origin=args.origin, dest=args.dest, chunk=args.chunk, return_stdout=args.stdout)
    if args.command == 'list':
        list = fire.list(path=args.path, expire=args.expire)
        for l in list:
            print(l)
    if args.command == 'delete':
        list = fire.list(path=args.path, expire=args.expire)
        fire.delete(list)
