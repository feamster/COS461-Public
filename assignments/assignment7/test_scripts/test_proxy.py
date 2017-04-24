#!/usr/bin/env python

import os
import random
import sys
import signal
import socket
import telnetlib
import time
import threading
import urlparse

try:
     import proxy_grade_private
     use_private = True
except ImportError:
     use_private = False

# pub_urls - The list of URLs to compare between the proxy
# and a direct connection.
#
# You can create additional automated tests for your proxy by
# adding URLs to this array.  This will have no effect on your
# grade, but may be helpful in testing and debugging your proxy.
#
# When you are testing against real web servers on the Internet,
# you may see minor differences between the proxy-fetched page and
# the regular page- possibly due to load balancing or dynamically
# generated content.  If there is only a single line that doesn't
# match between the two, it is likely a product of this sort of
# variation.
#
# Note that since this test script compares transaction output from
# the proxy and the direct connection, using invalid URLs may
# produce unexpected results, including the abnormal termination
# of the testing script.
#
pub_urls = ['http://example.com/', 'http://sns.cs.princeton.edu/',
            'http://www.cs.princeton.edu/people/faculty/',
            'https://www.cs.princeton.edu/~feamster/',];

# timeout_secs - Individual tests will be killed if they do not
# complete within this span of time.
timeout_secs = 30.0

def main():
     global pub_urls
     try:
          proxy_bin = sys.argv[1]
     except IndexError:
          usage()
          sys.exit(2)
     try:
          port = sys.argv[2]
     except IndexError:
          port = str(random.randint(1025, 49151))

     print 'Binary: %s' % proxy_bin
     print 'Running on port %s' % port

     # Start the proxy running in the background
     cid = os.spawnl(os.P_NOWAIT, proxy_bin, proxy_bin, port)
     # Give the proxy time to start up and start listening on the port
     time.sleep(2)

     passcount = 0
     for url in pub_urls:
          print '### Testing: ' + url
          passed = run_test(compare_url, (url, port), cid)
          if not live_process(cid):
               print '!!!Proxy process experienced abnormal termination during test- restarting proxy!'
               (cid, port) = restart_proxy(proxy_bin, port)
               passed = False

          if passed:
               print '%s: [PASSED]\n' % url
               passcount += 1
          else:
               print '%s: [FAILED]\n' % url

     if (use_private):
          (priv_passed, test_count, cid) = proxy_grade_private.runall(port, cid, proxy_bin)

     # Cleanup
     terminate(cid)

     print 'Summary: '
     print '\t%d of %d tests passed.' % (passcount, len(pub_urls))
     if (use_private):
          print '%d of %d extended tests passed' % (priv_passed, test_count)

def usage():
     print "Usage: proxy_grader.py path/to/proxy/binary port"
     print "Omit the port argument for a randomly generated port."

def run_test(test, args, childid):
     '''
     Run a single test function, monitoring its execution with a timer thread.

     * test: A function to execute.  Should take a tuple as its sole
     argument and return True for a passed test, and False otherwise.
     * args: Tuple that contains arguments to the test function
     * childid: Process ID of the running proxy

     The amount of time that the monitor waits before killing
     the proxy process can be set by changing timeout_secs at the top of this
     file.

     Returns True for a passed test, False otherwise.
     '''
     monitor = threading.Timer(timeout_secs, do_timeout, [childid])
     monitor.start()
     if not test(args):
          passed = False
     else:
          passed = True
     monitor.cancel()
     return passed

def compare_url(argtuple):
     '''
     Compare proxy output to the output from a direct server transaction.

     A simple sample test: download a web page via the proxy, and then fetch the
     same page directly from the server.  Compare the two pages for any
     differences, ignoring the Date header field if it is set.

     Argument tuples is in the form (url, port), where url is the URL to open, and
     port is the port the proxy is running on.
     '''
     (url, port) = argtuple
     urldata = urlparse.urlparse(url)
     try:
          (host, hostport) = urldata[1].split(':')
     except ValueError:
          host = urldata[1]
          hostport = 80

     # Retrieve via proxy
     try:
          proxy_data = get_data('localhost', port, url)
     except socket.error:
          print '!!!! Socket error while attempting to talk to proxy!'
          return False

     # Retrieve directly
     direct_data = get_direct(host, hostport, urldata[2])

     passed = True
     for (proxy, direct) in zip(proxy_data, direct_data):
          if proxy != direct and not (proxy.startswith('Date') and direct.startswith('Date')) and not (proxy.startswith('Expires') and direct.startswith('Expires')):
               print 'Proxy: %s' % proxy
               print 'Direct: %s'  % direct
               passed = False

     return passed

def get_direct(host, port, url):
     '''Retrieve a URL using direct HTTP/1.1 GET.'''
     getstring = 'GET %s HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n'
     data = http_exchange(host, port,  getstring % (url, host))
     return data.split('\n')

def get_data(host, port, url):
     '''Retrieve a URL using proxy HTTP/1.1 GET.'''
     getstring = 'GET %s HTTP/1.1\r\nConnection: close\r\n\r\n'
     data = http_exchange(host, port,  getstring % url)
     return data.split('\n')

def http_exchange(host, port, data):
     conn = telnetlib.Telnet()
     conn.open(host, port)
     conn.write(data)
     ret_data = conn.read_all()
     conn.close()
     return ret_data

def live_process(pid):
     '''Check that a process is still running.'''
     try:
          os.kill(pid, 0)
          return True
     except OSError:
          return False

def do_timeout(id):
     '''Callback function run by the monitor threads to kill a long-running operation.'''
     print '!!!! Proxy transaction timed out after %d seconds' % timeout_secs
     terminate(id)

def terminate(id):
     '''Stops and cleans up a running child process.'''
     assert(live_process(id))
     os.kill(id, signal.SIGINT)
     os.kill(id, signal.SIGKILL)
     try:
          os.waitpid(id, 0)
     except OSError:
          pass

def restart_proxy(binary, oldport):
     '''Restart the proxy on a new port number.'''
     newport = str(int(oldport) + 1)
     cid = os.spawnl(os.P_NOWAIT, binary, binary, newport)
     time.sleep(3)
     return (cid, newport)

if __name__ == '__main__':
     main()
