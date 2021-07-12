package storage

import (
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/url"
	"os"
	"time"

	storage "cloud.google.com/go/storage"
	"golang.org/x/net/context"

	firebase "firebase.google.com/go"
	"google.golang.org/api/option"
)

const (
	ERROR_CODE_INIT   = 1
	ERROR_CODE_UPLOAD = 2
	SHARE_URL         = "https://firebasestorage.googleapis.com/v0/b/%s/o/%s?alt=media"
)

type Config struct {
	Bucket             string `json:"storageBucket"`
	ServiceAccountPath string `json:"serviceAccount"`
}

var bucketHandle *storage.BucketHandle
var bucketPath string

func initializeIfNeeded() {
	if bucketHandle != nil {
		return
	}

	// get environment variables
	configPath := os.Getenv("FIREUP_CONFIG")
	if configPath == "" {
		fmt.Println("Environment variable FIREUP_CONFIG is not set")
		os.Exit(ERROR_CODE_INIT)
	}

	// open file from config
	file, err := os.Open(configPath)
	if err != nil {
		fmt.Println("Error opening config file:", err)
		os.Exit(ERROR_CODE_INIT)
	}
	defer file.Close()

	// File to string
	fileString, err := ioutil.ReadAll(file)
	if err != nil {
		fmt.Println("Error reading config file:", err)
		os.Exit(ERROR_CODE_INIT)
	}

	var configObject = Config{}
	err = json.Unmarshal(fileString, &configObject)
	if err != nil {
		fmt.Println("Error parsing config file:", err)
		os.Exit(ERROR_CODE_INIT)
	}

	// Assign for later use
	bucketPath = configObject.Bucket

	firebaseConfig := &firebase.Config{
		StorageBucket: configObject.Bucket,
	}

	opt := option.WithCredentialsFile(configObject.ServiceAccountPath)
	app, err := firebase.NewApp(context.Background(), firebaseConfig, opt)
	if err != nil {
		fmt.Println(err)
		os.Exit(ERROR_CODE_INIT)
	}

	client, err := app.Storage(context.Background())
	if err != nil {
		fmt.Println(err)
		os.Exit(ERROR_CODE_INIT)
	}

	bucketHandle, err = client.DefaultBucket()
	if err != nil {
		fmt.Println(err)
		os.Exit(ERROR_CODE_INIT)
	}

}

func Upload(origin string, dest string, returnStdout bool) {
	initializeIfNeeded()

	if !returnStdout {
		fmt.Printf("Uploading %s to %s…\n", origin, dest)
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*120)
	defer cancel()

	r, err := os.Open(origin)
	defer r.Close()

	object := bucketHandle.Object(dest)
	wc := object.NewWriter(ctx)

	if _, err = io.Copy(wc, r); err != nil {
		fmt.Println("Error writing to bucket:", err)
		os.Exit(ERROR_CODE_UPLOAD)
	}

	if err := wc.Close(); err != nil {
		fmt.Println("Error closing bucket:", err)
		os.Exit(ERROR_CODE_UPLOAD)
	}

	if !returnStdout {
		fmt.Println("Upload success!")
	}

	encoded_url := fmt.Sprintf(SHARE_URL, bucketPath, url.QueryEscape(dest))
	fmt.Println(encoded_url)
}
