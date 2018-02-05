/*****************************************************************************
 * server-go.go                                                                 
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

const RECV_BUFFER_SIZE = 2048

/* TODO: server()
 * Open socket and wait for client to connect
 * Print received message to stdout
*/
func server(server_port string) {

}


// Main parses command-line arguments and calls server function
func main() {
  if len(os.Args) != 2 {
    log.Fatal("Usage: ./server-go [server port]")
  }
  server_port := os.Args[1]
  server(server_port)
}
