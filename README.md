SSH geoip filter
================

Scripts to filter SSH logins based on IP address geolocation.

These scripts were inspired by
[Ralph Slooten at axllent.org](https://www.axllent.org/docs/view/ssh-geoip/)
with modification from
[Markus Ullmann](https://gist.github.com/jokey2k/a74f56955124880749e7).

These scripts have been tested on Ubuntu and Debian, but they should work
on other Linux distrubtion as well, provided that you have available
the necessary geoip binaries and data, i.e. the equivalent of `geoip-bin` --
especially `geoiplookup` and `geoip-database`.


## Directory and file structure
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
└── README.md
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
    * `files/usr/local/bin/sshfilter` to `/usr/local/bin/sshfilter`
    * `files/usr/local/bin/update-geoip` to `/usr/local/bin/update-geoip`

5. Update the geoip database, you will need administrative privileges because
the database is saved in `/usr/share/GeoIP/`:
```
$ sudo /usr/local/bin/update-geoip
GeoIP successfully updated
```

6. Test if `sshfilter` is working:
```bash
$ sshfilter -v 8.8.8.8
[2018-04-24_14:15:45][info]	DENY sshd connection from 8.8.8.8 (US)
```
You can also check the logs st `/var/auth.log`:
```bash
$ [sudo] tail -n1 /var/auth.log
Apr 24 14:15:45 inara cristian: DENY sshd connection from 8.8.8.8 (US)
```

7. Copy `files/etc/hosts.allow` and `files/etc/hosts.deny` to
   `/etc/hosts.allow` and `/etc/hosts.deny` respectively

8. Add a crontab job (as root) to update the geoip database:
```bash
(sudo crontab -l && echo '
# Update GeoIP database every 15 days
05  06  */15   *    *     /usr/local/bin/update-geoip >> /var/log/geoip.log
') | sudo crontab -
```
