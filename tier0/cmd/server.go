package cmd

import (
	"git.beryju.org/BeryJu.org/p2/tier0/internal"
	"github.com/spf13/cobra"
)

// serverCmd represents the server command
var serverCmd = &cobra.Command{
	Use:   "server",
	Short: "Run the tier0 Server",
	Long:  `Start the main Server on Port 8092, the caching Server on Port 8093 and the Metrics Server on 9001.`,
	Run: func(cmd *cobra.Command, args []string) {
		internal.Main()
	},
}

func init() {
	rootCmd.AddCommand(serverCmd)
}
