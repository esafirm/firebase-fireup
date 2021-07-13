package cmd

import (
	"fmt"
	"github.com/spf13/cobra"
	"os"

	storage "github.com/esafirm/fireup/storage"
)

var origin string
var dest string
var returnStdout bool

var rootCmd = &cobra.Command{
	Use:   "fireup",
	Short: "Upload file to Firebase Storage",
	Long:  `Fireup is CLI tool to upload files to Firebase storage with minimal config`,
	Args:  cobra.MaximumNArgs(0),
	Run: func(cmd *cobra.Command, args []string) {
		storage.Upload(origin, dest, returnStdout)
	},
}

func init() {
	rootCmd.Flags().StringVarP(&origin, "origin", "o", "", "Origin file")
	rootCmd.Flags().StringVarP(&dest, "dest", "d", "", "Destination file in Firebase Storage")
	rootCmd.Flags().BoolVarP(&returnStdout, "stdout", "s", false, "Used to for stdout capture")
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
