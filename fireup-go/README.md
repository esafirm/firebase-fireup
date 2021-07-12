## FireUp

Upload files to Firebse Storage

```
Fireup is CLI tool to upload files to Firebase storage with minimal config

Usage:
  fireup [flags]

Flags:
  -d, --dest string     Destination file in Firebase Storage
  -h, --help            help for fireup
  -o, --origin string   Origin file
  -s, --stdout          Used to for stdout capture
```

## Usage:

Set `FIREUP_CONFIG` environment variables to config json files. Example

```json
{
  "storageBucket": "testing.appspot.com",
  "serviceAccount": "./firebasadmin-sa.json"
}
```

### Upload

```bash
$ fireup -o <file> -d <path>

# Example
$ fireup -o some.apk -d apk/testing.apk
```

## Building

```
$ go build -v
```

## License

MIT @ Esa Firman
