#!/usr/bin/python3

# tran_control.py
# Version 1.00


# Look here for logging examples. 
# https://docs.python.org/3/howto/logging-cookbook.html

# Very simple python program to change the settings of the transmission
# daemon by using transmissionrpc client object. 

# Look here for information on transmissionrpc
# https://pythonhosted.org/transmissionrpc/reference/transmissionrpc.html#id3

from os import *
from datetime import datetime
import transmissionrpc
import logging

curentTime = datetime.now().time()

tranClient = transmissionrpc.Client(address='localhost',port=9091,timeout=None)

tranClient.set_session(timeout=None, alt_speed_time_end=##)

tranClient.set_session(timeout=None, speed_limit_down=##Kbps)


    
exit()

"""
This is not needed but is here for my reference.

4.   Session Requests

4.1.  Session Arguments

   string                           | value type | description
   ---------------------------------+------------+-------------------------------------
   "alt-speed-down"                 | number     | max global download speed (KBps)
   "alt-speed-enabled"              | boolean    | true means use the alt speeds
   "alt-speed-time-begin"           | number     | when to turn on alt speeds (units: minutes after midnight)
   "alt-speed-time-enabled"         | boolean    | true means the scheduled on/off times are used
   "alt-speed-time-end"             | number     | when to turn off alt speeds (units: same)
   "alt-speed-time-day"             | number     | what day(s) to turn on alt speeds (look at tr_sched_day)
   "alt-speed-up"                   | number     | max global upload speed (KBps)
   "blocklist-url"                  | string     | location of the blocklist to use for "blocklist-update"
   "blocklist-enabled"              | boolean    | true means enabled
   "blocklist-size"                 | number     | number of rules in the blocklist
   "cache-size-mb"                  | number     | maximum size of the disk cache (MB)
   "config-dir"                     | string     | location of transmission's configuration directory
   "download-dir"                   | string     | default path to download torrents
   "download-queue-size"            | number     | max number of torrents to download at once (see download-queue-enabled)
   "download-queue-enabled"         | boolean    | if true, limit how many torrents can be downloaded at once
   "dht-enabled"                    | boolean    | true means allow dht in public torrents
   "encryption"                     | string     | "required", "preferred", "tolerated"
   "idle-seeding-limit"             | number     | torrents we're seeding will be stopped if they're idle for this long
   "idle-seeding-limit-enabled"     | boolean    | true if the seeding inactivity limit is honored by default
   "incomplete-dir"                 | string     | path for incomplete torrents, when enabled
   "incomplete-dir-enabled"         | boolean    | true means keep torrents in incomplete-dir until done
   "lpd-enabled"                    | boolean    | true means allow Local Peer Discovery in public torrents
   "peer-limit-global"              | number     | maximum global number of peers
   "peer-limit-per-torrent"         | number     | maximum global number of peers
   "pex-enabled"                    | boolean    | true means allow pex in public torrents
   "peer-port"                      | number     | port number
   "peer-port-random-on-start"      | boolean    | true means pick a random peer port on launch
   "port-forwarding-enabled"        | boolean    | true means enabled
   "queue-stalled-enabled"          | boolean    | whether or not to consider idle torrents as stalled
   "queue-stalled-minutes"          | number     | torrents that are idle for N minuets aren't counted toward seed-queue-size or download-queue-size
   "rename-partial-files"           | boolean    | true means append ".part" to incomplete files
   "rpc-version"                    | number     | the current RPC API version
   "rpc-version-minimum"            | number     | the minimum RPC API version supported
   "script-torrent-done-filename"   | string     | filename of the script to run
   "script-torrent-done-enabled"    | boolean    | whether or not to call the "done" script
   "seedRatioLimit"                 | double     | the default seed ratio for torrents to use
   "seedRatioLimited"               | boolean    | true if seedRatioLimit is honored by default
   "seed-queue-size"                | number     | max number of torrents to uploaded at once (see seed-queue-enabled)
   "seed-queue-enabled"             | boolean    | if true, limit how many torrents can be uploaded at once
   "speed-limit-down"               | number     | max global download speed (KBps)
   "speed-limit-down-enabled"       | boolean    | true means enabled
   "speed-limit-up"                 | number     | max global upload speed (KBps)
   "speed-limit-up-enabled"         | boolean    | true means enabled
   "start-added-torrents"           | boolean    | true means added torrents will be started right away
   "trash-original-torrent-files"   | boolean    | true means the .torrent file of added torrents will be deleted
   "units"                          | object     | see below
   "utp-enabled"                    | boolean    | true means allow utp
   "version"                        | string     | long version string "$version ($revision)"
   ---------------------------------+------------+-----------------------------+
   units                            | object containing:                       |
                                    +--------------+--------+------------------+
                                    | speed-units  | array  | 4 strings: KB/s, MB/s, GB/s, TB/s
                                    | speed-bytes  | number | number of bytes in a KB (1000 for kB; 1024 for KiB)
                                    | size-units   | array  | 4 strings: KB/s, MB/s, GB/s, TB/s
                                    | size-bytes   | number | number of bytes in a KB (1000 for kB; 1024 for KiB)
                                    | memory-units | array  | 4 strings: KB/s, MB/s, GB/s, TB/s
                                    | memory-bytes | number | number of bytes in a KB (1000 for kB; 1024 for KiB)
                                    +--------------+--------+------------------+

   "rpc-version" indicates the RPC interface version supported by the RPC server.
   It is incremented when a new version of Transmission changes the RPC interface.

   "rpc-version-minimum" indicates the oldest API supported by the RPC server.
   It is changes when a new version of Transmission changes the RPC interface
   in a way that is not backwards compatible.  There are no plans for this
   to be common behavior.

4.1.1.  Mutators

   Method name: "session-set"
   Request arguments: one or more of 4.1's arguments, except: "blocklist-size",
                      "config-dir", "rpc-version", "rpc-version-minimum", and
                      "version"
   Response arguments: none

4.1.2.  Accessors

   Method name: "session-get"
   Request arguments: none
   Response arguments: all of 4.1's arguments

4.2.  Session Statistics

   Method name: "session-stats"

   Request arguments: none

   Response arguments:

   string                     | value type
   ---------------------------+-------------------------------------------------
   "activeTorrentCount"       | number
   "downloadSpeed"            | number
   "pausedTorrentCount"       | number
   "torrentCount"             | number
   "uploadSpeed"              | number
   ---------------------------+-------------------------------+
   "cumulative-stats"         | object, containing:           |
                              +------------------+------------+
                              | uploadedBytes    | number     | tr_session_stats
                              | downloadedBytes  | number     | tr_session_stats
                              | filesAdded       | number     | tr_session_stats
                              | sessionCount     | number     | tr_session_stats
                              | secondsActive    | number     | tr_session_stats
   ---------------------------+-------------------------------+
   "current-stats"            | object, containing:           |
                              +------------------+------------+
                              | uploadedBytes    | number     | tr_session_stats
                              | downloadedBytes  | number     | tr_session_stats
                              | filesAdded       | number     | tr_session_stats
                              | sessionCount     | number     | tr_session_stats
                              | secondsActive    | number     | tr_session_stats

4.3.  Blocklist

   Method name: "blocklist-update"
   Request arguments: none
   Response arguments: a number "blocklist-size"

4.4.  Port Checking

   This method tests to see if your incoming peer port is accessible
   from the outside world.

   Method name: "port-test"
   Request arguments: none
   Response arguments: a bool, "port-is-open"

4.5.  Session shutdown

   This method tells the transmission session to shut down.

   Method name: "session-close"
   Request arguments: none
   Response arguments: none

4.6.  Queue Movement Requests

   Method name          | libtransmission function
   ---------------------+-------------------------------------------------
   "queue-move-top"     | tr_torrentQueueMoveTop()
   "queue-move-up"      | tr_torrentQueueMoveUp()
   "queue-move-down"    | tr_torrentQueueMoveDown()
   "queue-move-bottom"  | tr_torrentQueueMoveBottom()

   Request arguments:

   string      | value type & description
   ------------+----------------------------------------------------------
   "ids"       | array   torrent list, as described in 3.1.

   Response arguments: none

4.7.  Free Space

   This method tests how much free space is available in a
   client-specified folder.

   Method name: "free-space"

   Request arguments:

   string      | value type & description
   ------------+----------------------------------------------------------
   "path"      | string  the directory to query

   Response arguments:

   string      | value type & description
   ------------+----------------------------------------------------------
   "path"      | string  same as the Request argument
   "size-bytes"| number  the size, in bytes, of the free space in that directory


5.0.  Protocol Versions

  The following changes have been made to the RPC interface:

   RPC   | Release | Backwards |                      |
   Vers. | Version | Compat?   | Method               | Description
   ------+---------+-----------+----------------------+-------------------------------
   1     | 1.30    | n/a       | n/a                  | Initial version
   ------+---------+-----------+----------------------+-------------------------------
   2     | 1.34    | yes       | torrent-get          | new arg "peers"
   ------+---------+-----------+----------------------+-------------------------------
   3     | 1.41    | yes       | torrent-get          | added "port" to "peers"
         |         | yes       | torrent-get          | new arg "downloaders"
         |         | yes       | session-get          | new arg "version"
         |         | yes       | torrent-remove       | new method
   ------+---------+-----------+----------------------+-------------------------------
   4     | 1.50    | yes       | session-get          | new arg "rpc-version"
         |         | yes       | session-get          | new arg "rpc-version-minimum"
         |         | yes       | session-stats        | added "cumulative-stats"
         |         | yes       | session-stats        | added "current-stats"
         |         | yes       | torrent-get          | new arg "downloadDir"
   ------+---------+-----------+----------------------+-------------------------------
   5     | 1.60    | yes       |                      | new method "torrent-reannounce"
         |         | yes       |                      | new method "blocklist-update"
         |         | yes       |                      | new method "port-test"
         |         |           |                      |
         |         | yes       | session-get          | new arg "alt-speed-begin"
         |         | yes       | session-get          | new arg "alt-speed-down"
         |         | yes       | session-get          | new arg "alt-speed-enabled"
         |         | yes       | session-get          | new arg "alt-speed-end"
         |         | yes       | session-get          | new arg "alt-speed-time-enabled"
         |         | yes       | session-get          | new arg "alt-speed-up"
         |         | yes       | session-get          | new arg "blocklist-enabled"
         |         | yes       | session-get          | new arg "blocklist-size"
         |         | yes       | session-get          | new arg "peer-limit-per-torrent"
         |         | yes       | session-get          | new arg "seedRatioLimit"
         |         | yes       | session-get          | new arg "seedRatioLimited"
         |         |        NO | session-get          | renamed "pex-allowed" to "pex-enabled"
         |         |        NO | session-get          | renamed "port" to "peer-port"
         |         |        NO | session-get          | renamed "peer-limit" to "peer-limit-global"
         |         |           |                      |
         |         | yes       | torrent-add          | new arg "files-unwanted"
         |         | yes       | torrent-add          | new arg "files-wanted"
         |         | yes       | torrent-add          | new arg "priority-high"
         |         | yes       | torrent-add          | new arg "priority-low"
         |         | yes       | torrent-add          | new arg "priority-normal"
         |         |           |                      |
         |         | yes       | torrent-set          | new arg "bandwidthPriority"
"""