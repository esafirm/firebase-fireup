## FireUp

Upload, delete, and list your files in Firebse Storage

```
Firebase storage management tools

positional arguments:
  {delete,upload,list}  Sub commands
    delete              Delete files in firebase storage
    upload              Upload file use --origin and --dest
    list                List files in --target dir

optional arguments:
  -h, --help            show this help message and exit
```

## Usage:

Set `FIREUP_CONFIG` environment variables to config json files. Example

```json
{
  "apiKey": "12312asdasdzxc123123213",
  "storageBucket": "testing.appspot.com",
  "authDomain": "testing.firebaseapp.com",
  "databaseURL": "https://testing.firebaseio.com",
  "serviceAccount": "./firebasadmin-sa.json"
}
```

### Upload

```bash
$ fireup upload --origin <file> --dest <path>

# Example
$ fireup upload --origin some.apk --dest apk/testing.apk
```

### Delete

```bash
$ fireup delete --path <path> --expire <expire_in_days>

# Example
$ fireup delete --path apk/ --expire 1
```

### List	

```bash
$ fireup list --path <path> --expire <expire_in_days>

# Example
$ fireup list --path /apk
```

## License

MIT @ Esa Firman