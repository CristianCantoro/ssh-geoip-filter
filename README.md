SSH geoip filter
================

Scripts to filter SSH logins based on IP address geolocation.

These scripts were inspired by
[Ralph Slooten at axllent.org](https://www.axllent.org/docs/view/ssh-geoip/)
with modifications from
[Markus Ullmann](https://gist.github.com/jokey2k/a74f56955124880749e7).

These scripts have been tested on Ubuntu and Debian, but they should work
on other Linux distrubtion as well, provided that you have available
the necessary geoip binaries and data, i.e. the equivalent of `geoip-bin`
-- especially `geoiplookup` -- and `geoip-database`.


## Directories and files
```
.
├── files
│   ├── etc
│   │   ├── hosts.allow
│   │   └── hosts.deny
│   └── usr
│       └── local
│           └── bin
│               ├── sshfilter
│               └── update-geoip
├── LICENSE
├── README.md
└── utils
    └── sgf-parse-log.py
```

## How to install

1. Install geoip packages:
```bash
apt install geoip-bin geoip-database
```

2. Clone the repo:
```bash
git clone git@github.com:CristianCantoro/ssh-geoip-filter.git
```

3. Get into the repo directory: `cd ssh-geoip-filter`

4. Copy:
    * `files/etc/sshfilter.conf` to `/etc/sshfilter.conf`
    * `files/usr/local/bin/sshfilter` to `/usr/local/bin/sshfilter`
    * `files/usr/local/bin/update-geoip` to `/usr/local/bin/update-geoip`
  (you will need administrative privilege to perform these copies)

5. Update the configuration file at `/etc/sshfilter.conf` and set the values
of the variables `ALLOW_COUNTRIES` and `LOG_FACILITY`

6. Update the geoip database, you will need administrative privileges to run
this command because the database is saved in `/usr/share/GeoIP/`:
```
$ sudo /usr/local/bin/update-geoip
GeoIP successfully updated
```

7. Test if `sshfilter` is working:
```bash
$ sshfilter -v 8.8.8.8
[2018-04-24_14:15:45][info]	DENY sshd connection from 8.8.8.8 (US)
```
You can also check the logs at `/var/log/auth.log`:
```bash
$ [sudo] tail -n1 /var/log/auth.log
Apr 24 14:15:45 inara cristian: DENY sshd connection from 8.8.8.8 (US)
```

8. Copy `files/etc/hosts.allow` and `files/etc/hosts.deny` to
   `/etc/hosts.allow` and `/etc/hosts.deny` respectively

9. Add a crontab job (as root) to update the geoip database:
```bash
(sudo crontab -l && echo '
# Update GeoIP database every 15 days
05  06  */15   *    *     /usr/local/bin/update-geoip >> /var/log/geoip.log
') | sudo crontab -
```

## Utils
The script `sgf-parse-log.py` parses timestamps from log file to convert them
to ISO format, so they are easier to process.

`sgf-parse-log.py`:
```
Parse timestamps from log file to convert it to ISO.

Usage:
  sgf-parse-log.py [--tz TIMEZONE] [--time-format=TIME_FORMAT]...
                   [<logfile>]...
  sgf-parse-log.py (-h | --help)
  sgf-parse-log.py --version

Argiments:
  <logfile>       Log file to read [default: stdin].

Options:
  --tz TIMEZONE               Timezone of the timestamps in the log file.
  --time-format=TIME_FORMAT   Time format of the timestamps in the log file.
                              It can be specified multiple times.
  -h --help                   Show this screen.
  --version                   Show version.
```

Example usage:

* sample data:
```
$ tail deny.sshd.log 
Apr 22 06:06:34 host root: DENY sshd connection from 119.249.54.217 (CN)
Apr 22 06:06:35 host root: DENY sshd connection from 122.226.181.165 (CN)
Apr 22 06:08:00 host root: DENY sshd connection from 119.249.54.217 (CN)
Apr 22 06:08:20 host root: DENY sshd connection from 122.226.181.167 (CN)
Apr 22 06:08:28 host root: DENY sshd connection from 221.194.44.211 (CN)
Apr 22 06:08:57 host root: DENY sshd connection from 122.226.181.164 (CN)
Apr 22 06:09:29 host root: DENY sshd connection from 119.249.54.217 (CN)
Apr 22 06:09:50 host root: DENY sshd connection from 221.194.47.243 (CN)
Apr 22 06:10:11 host root: DENY sshd connection from 122.226.181.167 (CN)
Apr 22 06:11:56 host root: DENY sshd connection from 122.226.181.164 (CN)
```

* with parsed timestamps:
```
$ tail /tmp/ssh/deny.sshd.log | \
   ./sgf-parse-log.py --tz 'America/Toronto' --time-format 'YYYY MMM D HH:mm:ss'
2018-04-22T06:06:34-04:00 CN 119.249.54.217
2018-04-22T06:06:35-04:00 CN 122.226.181.165
2018-04-22T06:08:00-04:00 CN 119.249.54.217
2018-04-22T06:08:20-04:00 CN 122.226.181.167
2018-04-22T06:08:28-04:00 CN 221.194.44.211
2018-04-22T06:08:57-04:00 CN 122.226.181.164
2018-04-22T06:09:29-04:00 CN 119.249.54.217
2018-04-22T06:09:50-04:00 CN 221.194.47.243
2018-04-22T06:10:11-04:00 CN 122.226.181.167
2018-04-22T06:11:56-04:00 CN 122.226.181.164
```