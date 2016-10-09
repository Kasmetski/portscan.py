#!/usr/bin/python
import argparse
import os
import socket
import sys
import time

# This mark for custom ports to scan
flag = 0
# Clear console
os.system('clear')
drawBigLine = '+' * 88
drawSmallLine = '+' * 33
description = drawBigLine + '''\n Simple port scanner made to train Python (c) Martin Kasmetski
Example usage: python portscan.py 192.168.0.1 1 1080
The above command will scan ip 192.168.0.1 from port 1 to 1000
To scan for most common ports, just use: python portsca.py www.exampledomain.com\n''' + drawBigLine + '\n'

parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('host', metavar='H', help='Hostname to scan')
parser.add_argument('startport', metavar='P1', nargs='?', help='Start from this port')
parser.add_argument('endport', metavar='P2', nargs='?', help='Stop after this port')
args = parser.parse_args()

host = args.host
# convert hostname into ip
ip = socket.gethostbyname(host)

if args.startport and args.endport:
    startPort = int(args.startport)
    endPort = int(args.endport)
else:
    # if ports are not valid, the script will scan for most common ports
    flag = 1

# list for open ports
openPorts = []

# dictionary of most popular ports
commonPorts = {
    '21': 'FTP',
    '22': 'SSH',
    '23': 'TELNET',
    '25': 'SMTP',
    '53': 'DNS',
    '69': 'TFTP',
    '80': 'HTTP',
    '109': 'POP2',
    '110': 'POP3',
    '123': 'NTP',
    '137': 'NETBIOS-NS',
    '138': 'NETBIOS-DGM',
    '139': 'NETBIOS-SSN',
    '143': 'IMAP',
    '156': 'SQL-SERVER',
    '389': 'LDAP',
    '443': 'HTTPS',
    '546': 'DHCP-CLIENT',
    '547': 'DHCP-SERVER',
    '995': 'POP3-SSL',
    '993': 'IMAP-SSL',
    '2086': 'WHM/CPANEL',
    '2087': 'WHM/CPANEL',
    '2082': 'CPANEL',
    '2083': 'CPANEL',
    '3306': 'MYSQL',
    '8443': 'PLESK',
    '10000': 'VIRTUALMIN/WEBMIN'
}

startTime = time.time()
print drawSmallLine
print '\tToo simple port scanner, made with love <3'
print drawSmallLine

if flag:
    print "scanning for most common ports on %s" % host
else:
    print 'Scanning %s from port %s - %s: ' % (host, startPort, endPort)
print "scanning started at %s" % (time.strftime('%I:%M:%S %p'))


# scanning ports function
def check_port(host, port, result=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        r = sock.connect_ex((host, port))

        if r == 0:
            result = r
        sock.close()
    except Exception, e:
        pass

    return result


# check dictionary

def get_service(port):
    port = str(port)
    if port in commonPorts:
        return commonPorts[port]
    else:
        return 0


try:
    print 'Scan in progress...'
    print 'Connecting to Port: ',

    if flag:
        for p in sorted(commonPorts):
            sys.stdout.flush()
            p = int(p)
            print p,
            response = check_port(host, p)
            if response == 0:
                openPorts.append(p)
                sys.stdout.write('\b' * len(str(p)))
    else:
        for p in range(startPort, endPort + 1):
            sys.stdout.flush()
            print p,
            response = check_port(host, p)
            if response == 0:
                openPorts.append(p)
            if not p == endPort:
                sys.stdout.write('\b' * len(str(p)))

    print '\nScanning competed at %s' % (time.strftime('%I:%M:%S %p'))
    endTime = time.time()
    totalTime = endTime - startTime
    print drawSmallLine
    print '\tScan report: %s' % host
    print drawSmallLine

    if totalTime <= 60:
        totalTime = str(round(totalTime, 2))
        print 'Scan took %s seconds' % totalTime
    else:
        totalTime /= 60
        print 'Scan took %s minutes' % totalTime

    if openPorts:
        print 'Open Ports:'
        for i in sorted(openPorts):
            service = get_service(i)
            if not service:
                service = 'This service is not in the database'
            print '\t %s %s: Open' % (i, service)
    else:
        print 'Sorry, We can\'t find open ports...'

# if user pres ctrl+c
except KeyboardInterrupt:
    print 'You pressed ctrl+c. Exiting the program'
    sys.exit(1)
