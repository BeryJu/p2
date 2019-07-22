package main

import (
	"git.beryju.org/BeryJu.org/p2/tier0/cmd"
	"git.beryju.org/BeryJu.org/p2/tier0/internal"
	log "github.com/sirupsen/logrus"
)

func main() {
	log.SetFormatter(&log.JSONFormatter{})
	log.SetLevel(log.DebugLevel)
	log.Debugf("Starting p2-tier0 Version %s", internal.Version)
	cmd.Execute()
}
