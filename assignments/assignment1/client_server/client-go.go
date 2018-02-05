/*****************************************************************************
 * client-go.go                                                                 
 * Name:
 * NetId:
 *****************************************************************************/

package main

import (
  "fmt"
  "io"
  "os"
  "log"
  "net"
  "bufio"
)

const SEND_BUFFER_SIZE = 2048

/* TODO: client()
 * Open socket and send message from stdin.
*/
func client(server_ip string, server_port string) {

}

// Main parses command-line arguments and calls client function
func main() {
  if len(os.Args) != 3 {
    log.Fatal("Usage: ./client-go [server IP] [server port] < [message file]")
  }
  server_ip := os.Args[1]
  server_port := os.Args[2]
  client(server_ip, server_port)
}
