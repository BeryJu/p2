package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "tier0",
	Short: "p2 Caching Server",
	Long:  `Fast frontend which serves files from p2. Caches files in memory, and automatically distributes the cache to its peers.`,
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
