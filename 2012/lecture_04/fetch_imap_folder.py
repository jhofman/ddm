#!/usr/bin/env python2.6
#
# file: fetch imap folder
#
# description: gets messages from specified folder on imap server, and
#  saves each message to an individual file
#
# usage: ./fetch_imap_folder.py 
#  (enter credentials when prompted)
#  see ./fetch_imap_folder.py --help for more usage information
#
# author: jake hofman (gmail: jhofman)
#
# todo:
#

# module to get password from command line
from getpass import getpass

# module to speak to imap server
import imaplib

# modules to parse command line options
from optparse import OptionParser

import sys
import os


def fetch_imap_folder(username, password, n, server, folder):
    """
    fetches last n sent messages from given folder on imap server
    """

    # connect and login
    conn = imaplib.IMAP4_SSL(server)
    conn.login(username, password)

    # get number of messages in folder
    status, num_msgs = conn.select(folder)
    num_msgs = int(num_msgs[0])

    msg_range = '%s:%s' % (max(num_msgs-n,1), num_msgs)

    dir = server + "/" + username + "/" + folder
    if not os.path.isdir(dir):
        os.makedirs(dir)

    # count backwards to get range for last n messages
    msg_range = range(max(num_msgs-n,1), num_msgs)

    for msg in msg_range:
        # grab messages
        status, data = conn.fetch(msg, "(RFC822)")

        file = "%s/%d.txt" % (dir, msg)
        f = open(file, 'w')
        f.write(data[0][1])
        f.close()


def parse_options():
    usage="usage: %prog [options] arg"
    parser=OptionParser(usage)
    parser.add_option("-s","--server",
                      dest="server",
                      default="",
                      help="imap server")
    parser.add_option("-f","--folder",
                      dest="folder",
                      default="",
                      help="imap folder")
    parser.add_option("-u","--username",
                      dest="username",
                      default="",
                      help="username for imap server")
    parser.add_option("-m","--msgs",
                      dest="msgs",
                      default="",
                      help="maximum number of sent messages to retrieve")
    parser.add_option("-p","--password",
                      dest="password",
                      default=False,
                      action="store_true",
                      help="read password from stdin (otherwise prompted for password)")

    options, args = parser.parse_args()

    try:
        options.msgs=int(options.msgs)
    except ValueError:
        options.msgs=0

    return options.server, options.folder, options.username, options.password, options.msgs


if __name__=='__main__':

    server, folder, username, p, n = parse_options()

    # get credentials from user
    if len(server) == 0:
        server = raw_input('server: ').lower()
    if len(folder) == 0:
        folder = raw_input('folder: ')
    if len(username) == 0:
        username = raw_input('username: ')

    if p:
        password = sys.stdin.readline().rstrip('\n')
    else:
        password = getpass()

    if n <= 0:
        n = int(raw_input('max messages: '))

    # fetch messages
    fetch_imap_folder(username,password,n,server,folder)


