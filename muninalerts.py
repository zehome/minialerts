#!/usr/bin/env python

import logging
import urllib2
import urllib
import json
import sys
import os

logger = logging.getLogger("muninalerts")

# sample_data="""
# {"group":"cbm76", "host":"faxverdun.cbm76", "category":"disk", "title":"Filesystem usage (in %)", "warnings": [ {"label":"/", "value":"95.00", "wrange":":92", "crange":":98", "extinfo":""} ], "criticals": [  ], "unknown": [ {"label":"/", "value":"95.00", "wrange":":92", "crange":":98", "extinfo":""} ]}
# {"group":"labomaine", "host":"nemesis2psstech.labomaine", "category":"", "title":"Pending packages", "warnings": [ {"label":"pending", "value":"152.00", "wrange":"0:0", "crange":":", "extinfo":"acpid apache2 apache2-mpm-prefork apache2-utils apache2.2-bin apache2.2-common aptitude base-files bind9-host bzip2 ca-certificates cifs-utils cups cups-bsd cups-client cups-common cups-ppdc debian-archive-keyring dhcp3-client dnsutils dpkg dpkg-dev file foomatic-filters git git-core grub-common grub-pc initscripts iotop isc-dhcp-client isc-dhcp-common krb5-multidev libapache2-mod-php5 libapr1 libbind9-60 libbz2-1.0 libc-ares2 libc-bin libc-dev-bin libc6 libc6-dev libcups2 libcupscgi1 libcupsdriver1 libcupsimage2 libcupsmime1 libcupsppdc1 libcurl3 libcurl3-gnutls libcurl4-openssl-dev libdbd-pg-perl libdns69 libdpkg-perl libecpg-compat3 libecpg-dev libecpg6 libexpat1 libexpat1-dev libfreetype6 libfreetype6-dev libgl1-mesa-dev libgl1-mesa-glx libglu1-mesa libglu1-mesa-dev libgnutls-dev libgnutls26 libgssapi-krb5-2 libgssrpc4 libisc62 libisccc60 libisccfg62 libjasper1 libk5crypto3 libkadm5clnt-mit7 libkadm5srv-mit7 libkdb5-4 libkrb5-3 libkrb5-dev libkrb5support0 liblwres60 libmagic1 libmagickcore3 libpam-modules libpam-runtime libpam0g libpcap0.8 libperl5.10 libpgtypes3 libpng12-0 libpng12-dev libpq-dev libpq5 libssl-dev libssl0.9.8 libtasn1-3 libtasn1-3-dev libtiff4 libvorbis0a libvorbisenc2 libxi-dev libxi6 libxml2 libxml2-dev libxslt1.1 links linux-libc-dev locales mdadm mesa-common-dev module-init-tools mysql-common nfs-common openssh-client openssh-server openssl perl perl-base perl-modules perlmagick php5-cli php5-common php5-pgsql postgresql-8.4 postgresql-9.1 postgresql-client-8.4 postgresql-client-9.1 postgresql-client-common postgresql-common postgresql-contrib-9.1 postgresql-server-dev-8.4 procps python python-dev python-minimal smbfs sudo sysv-rc sysvinit sysvinit-utils tshark tzdata update-inetd usbutils vsftpd wireshark-common x11-common xorg-dev xpdf xpdf-reader xpdf-utils xserver-xorg-dev"} ], "criticals": [  ], "unknown": [ {"label":"pending", "value":"152.00", "wrange":"0:0", "crange":":", "extinfo":"acpid apache2 apache2-mpm-prefork apache2-utils apache2.2-bin apache2.2-common aptitude base-files bind9-host bzip2 ca-certificates cifs-utils cups cups-bsd cups-client cups-common cups-ppdc debian-archive-keyring dhcp3-client dnsutils dpkg dpkg-dev file foomatic-filters git git-core grub-common grub-pc initscripts iotop isc-dhcp-client isc-dhcp-common krb5-multidev libapache2-mod-php5 libapr1 libbind9-60 libbz2-1.0 libc-ares2 libc-bin libc-dev-bin libc6 libc6-dev libcups2 libcupscgi1 libcupsdriver1 libcupsimage2 libcupsmime1 libcupsppdc1 libcurl3 libcurl3-gnutls libcurl4-openssl-dev libdbd-pg-perl libdns69 libdpkg-perl libecpg-compat3 libecpg-dev libecpg6 libexpat1 libexpat1-dev libfreetype6 libfreetype6-dev libgl1-mesa-dev libgl1-mesa-glx libglu1-mesa libglu1-mesa-dev libgnutls-dev libgnutls26 libgssapi-krb5-2 libgssrpc4 libisc62 libisccc60 libisccfg62 libjasper1 libk5crypto3 libkadm5clnt-mit7 libkadm5srv-mit7 libkdb5-4 libkrb5-3 libkrb5-dev libkrb5support0 liblwres60 libmagic1 libmagickcore3 libpam-modules libpam-runtime libpam0g libpcap0.8 libperl5.10 libpgtypes3 libpng12-0 libpng12-dev libpq-dev libpq5 libssl-dev libssl0.9.8 libtasn1-3 libtasn1-3-dev libtiff4 libvorbis0a libvorbisenc2 libxi-dev libxi6 libxml2 libxml2-dev libxslt1.1 links linux-libc-dev locales mdadm mesa-common-dev module-init-tools mysql-common nfs-common openssh-client openssh-server openssl perl perl-base perl-modules perlmagick php5-cli php5-common php5-pgsql postgresql-8.4 postgresql-9.1 postgresql-client-8.4 postgresql-client-9.1 postgresql-client-common postgresql-common postgresql-contrib-9.1 postgresql-server-dev-8.4 procps python python-dev python-minimal smbfs sudo sysv-rc sysvinit sysvinit-utils tshark tzdata update-inetd usbutils vsftpd wireshark-common x11-common xorg-dev xpdf xpdf-reader xpdf-utils xserver-xorg-dev"} ]}
# {"group":"labomaine", "host":"backupserverpsstech.labomaine", "category":"", "title":"Pending packages", "warnings": [ {"label":"pending", "value":"121.00", "wrange":"0:0", "crange":":", "extinfo":"acpid aptitude base-files bind9-host bzip2 ca-certificates cups-common cups-ppdc debian-archive-keyring dhcp3-client dnsutils dpkg dpkg-dev file foomatic-filters git grub-common grub-pc initscripts iotop isc-dhcp-client isc-dhcp-common krb5-multidev libapr1 libbind9-60 libbz2-1.0 libc-ares2 libc-bin libc-dev-bin libc6 libc6-dev libc6-i386 libcups2 libcupscgi1 libcupsdriver1 libcupsimage2 libcupsmime1 libcupsppdc1 libcurl3 libcurl3-gnutls libcurl4-openssl-dev libdns69 libdpkg-perl libexpat1 libfreetype6 libfreetype6-dev libgl1-mesa-dev libgl1-mesa-glx libglu1-mesa libglu1-mesa-dev libgnutls-dev libgnutls26 libgssapi-krb5-2 libgssrpc4 libisc62 libisccc60 libisccfg62 libjasper1 libk5crypto3 libkadm5clnt-mit7 libkadm5srv-mit7 libkdb5-4 libkrb5-3 libkrb5-dev libkrb5support0 liblwres60 libmagic1 libmagickcore3 libpam-modules libpam-runtime libpam0g libpcap0.8 libperl5.10 libpng12-0 libpng12-dev libpq5 libssl-dev libssl0.9.8 libtasn1-3 libtasn1-3-dev libtiff4 libvorbis0a libvorbisenc2 libwbclient0 libxi6 libxml2 linux-libc-dev locales mdadm mesa-common-dev module-init-tools mysql-common nfs-common openssh-client openssh-server openssl perl perl-base perl-modules perlmagick postgresql-client-8.4 postgresql-client-9.1 postgresql-client-common procps python python-minimal samba-common smbclient sudo sysv-rc sysvinit sysvinit-utils tshark tzdata update-inetd usbutils wireshark-common x11-common xpdf xpdf-reader xpdf-utils"} ], "criticals": [  ], "unknown": [ {"label":"pending", "value":"121.00", "wrange":"0:0", "crange":":", "extinfo":"acpid aptitude base-files bind9-host bzip2 ca-certificates cups-common cups-ppdc debian-archive-keyring dhcp3-client dnsutils dpkg dpkg-dev file foomatic-filters git grub-common grub-pc initscripts iotop isc-dhcp-client isc-dhcp-common krb5-multidev libapr1 libbind9-60 libbz2-1.0 libc-ares2 libc-bin libc-dev-bin libc6 libc6-dev libc6-i386 libcups2 libcupscgi1 libcupsdriver1 libcupsimage2 libcupsmime1 libcupsppdc1 libcurl3 libcurl3-gnutls libcurl4-openssl-dev libdns69 libdpkg-perl libexpat1 libfreetype6 libfreetype6-dev libgl1-mesa-dev libgl1-mesa-glx libglu1-mesa libglu1-mesa-dev libgnutls-dev libgnutls26 libgssapi-krb5-2 libgssrpc4 libisc62 libisccc60 libisccfg62 libjasper1 libk5crypto3 libkadm5clnt-mit7 libkadm5srv-mit7 libkdb5-4 libkrb5-3 libkrb5-dev libkrb5support0 liblwres60 libmagic1 libmagickcore3 libpam-modules libpam-runtime libpam0g libpcap0.8 libperl5.10 libpng12-0 libpng12-dev libpq5 libssl-dev libssl0.9.8 libtasn1-3 libtasn1-3-dev libtiff4 libvorbis0a libvorbisenc2 libwbclient0 libxi6 libxml2 linux-libc-dev locales mdadm mesa-common-dev module-init-tools mysql-common nfs-common openssh-client openssh-server openssl perl perl-base perl-modules perlmagick postgresql-client-8.4 postgresql-client-9.1 postgresql-client-common procps python python-minimal samba-common smbclient sudo sysv-rc sysvinit sysvinit-utils tshark tzdata update-inetd usbutils wireshark-common x11-common xpdf xpdf-reader xpdf-utils"} ]}
# {"group":"fontenay", "host":"vpn1bondy.fontenay", "category":"disk", "title":"Disk usage (in percent)", "warnings": [ {"label":"/var/tmp", "value":"97.00", "wrange":":92", "crange":":98", "extinfo":""} ], "criticals": [  ], "unknown": [ {"label":"/var/tmp", "value":"97.00", "wrange":":92", "crange":":98", "extinfo":""} ]}
# {"group":"clarisysinfra", "host":"claribox4.clarisys.fr", "category":"disk", "title":"S.M.A.R.T values for drive sdb", "warnings": [ {"label":"smartctl_exit_status", "value":"64.00", "wrange":":1", "crange":":", "extinfo":""} ], "criticals": [  ], "unknown": [ {"label":"smartctl_exit_status", "value":"64.00", "wrange":":1", "crange":":", "extinfo":""} ]}
# {"group":"mirialis", "host":"mca.mirialis", "category":"", "title":"Pending packages", "warnings": [ {"label":"pending", "value":"91.00", "wrange":"0:0", "crange":":", "extinfo":"acpid apache2 apache2-mpm-prefork apache2-utils apache2.2-bin apache2.2-common base-files bind9-host debian-archive-keyring dhcp3-client dnsutils dpkg dpkg-dev file foomatic-filters initscripts isc-dhcp-client isc-dhcp-common krb5-multidev libapache2-mod-php5 libapr1 libbind9-60 libc-bin libc-dev-bin libc6 libc6-dev libdns69 libdpkg-perl libecpg-compat3 libecpg-dev libecpg6 libexpat1 libexpat1-dev libgssapi-krb5-2 libgssrpc4 libisc62 libisccc60 libisccfg62 libk5crypto3 libkadm5clnt-mit7 libkadm5srv-mit7 libkdb5-4 libkrb5-3 libkrb5-dev libkrb5support0 liblwres60 libmagic1 libmagickcore3 libperl5.10 libpgtypes3 libpq-dev libpq5 libssl-dev libssl0.9.8 libtiff4 libwbclient0 libxi-dev libxi6 libxml2 libxml2-dev links linux-libc-dev locales mysql-common openssh-client openssh-server openssl perl perl-base perl-modules perlmagick php5-common php5-pgsql postgresql-8.4 postgresql-client-8.4 postgresql-client-common postgresql-common postgresql-server-dev-8.4 procps python python-dev python-minimal samba-common smbclient sudo sysv-rc sysvinit sysvinit-utils tshark tzdata wireshark-common"} ], "criticals": [  ], "unknown": [ {"label":"pending", "value":"91.00", "wrange":"0:0", "crange":":", "extinfo":"acpid apache2 apache2-mpm-prefork apache2-utils apache2.2-bin apache2.2-common base-files bind9-host debian-archive-keyring dhcp3-client dnsutils dpkg dpkg-dev file foomatic-filters initscripts isc-dhcp-client isc-dhcp-common krb5-multidev libapache2-mod-php5 libapr1 libbind9-60 libc-bin libc-dev-bin libc6 libc6-dev libdns69 libdpkg-perl libecpg-compat3 libecpg-dev libecpg6 libexpat1 libexpat1-dev libgssapi-krb5-2 libgssrpc4 libisc62 libisccc60 libisccfg62 libk5crypto3 libkadm5clnt-mit7 libkadm5srv-mit7 libkdb5-4 libkrb5-3 libkrb5-dev libkrb5support0 liblwres60 libmagic1 libmagickcore3 libperl5.10 libpgtypes3 libpq-dev libpq5 libssl-dev libssl0.9.8 libtiff4 libwbclient0 libxi-dev libxi6 libxml2 libxml2-dev links linux-libc-dev locales mysql-common openssh-client openssh-server openssl perl perl-base perl-modules perlmagick php5-common php5-pgsql postgresql-8.4 postgresql-client-8.4 postgresql-client-common postgresql-common postgresql-server-dev-8.4 procps python python-dev python-minimal samba-common smbclient sudo sysv-rc sysvinit sysvinit-utils tshark tzdata wireshark-common"} ]}
# {"group":"mirialis", "host":"clarilab.mirialis", "category":"", "title":"Pending packages", "warnings": [ {"label":"pending", "value":"92.00", "wrange":"0:0", "crange":":", "extinfo":"acpid apache2-mpm-prefork apache2-utils apache2.2-bin apache2.2-common base-files bind9-host debian-archive-keyring dhcp3-client dnsutils dpkg dpkg-dev file foomatic-filters initscripts isc-dhcp-client isc-dhcp-common krb5-multidev libapache2-mod-php5 libapr1 libbind9-60 libc-bin libc-dev-bin libc6 libc6-dev libdns69 libdpkg-perl libexpat1 libexpat1-dev libgssapi-krb5-2 libgssrpc4 libisc62 libisccc60 libisccfg62 libk5crypto3 libkadm5clnt-mit7 libkadm5srv-mit7 libkdb5-4 libkrb5-3 libkrb5-dev libkrb5support0 liblwres60 libmagic1 libmagickcore3 libperl5.10 libpq-dev libpq5 libssl-dev libssl0.9.8 libtiff4 libtiff4-dev libtiffxx0c2 libwbclient0 libxi-dev libxi6 libxml2 libxslt1.1 links linux-libc-dev locales mysql-common openssh-client openssh-server openssl perl perl-base perl-modules perlmagick php5-cli php5-common php5-pgsql postgresql-8.4 postgresql-9.1 postgresql-client-8.4 postgresql-client-9.1 postgresql-client-common postgresql-common postgresql-contrib-9.1 postgresql-server-dev-8.4 postgresql-server-dev-9.1 procps python python-minimal samba-common smbclient sudo sysv-rc sysvinit sysvinit-utils tshark tzdata wireshark-common"} ], "criticals": [  ], "unknown": [ {"label":"pending", "value":"92.00", "wrange":"0:0", "crange":":", "extinfo":"acpid apache2-mpm-prefork apache2-utils apache2.2-bin apache2.2-common base-files bind9-host debian-archive-keyring dhcp3-client dnsutils dpkg dpkg-dev file foomatic-filters initscripts isc-dhcp-client isc-dhcp-common krb5-multidev libapache2-mod-php5 libapr1 libbind9-60 libc-bin libc-dev-bin libc6 libc6-dev libdns69 libdpkg-perl libexpat1 libexpat1-dev libgssapi-krb5-2 libgssrpc4 libisc62 libisccc60 libisccfg62 libk5crypto3 libkadm5clnt-mit7 libkadm5srv-mit7 libkdb5-4 libkrb5-3 libkrb5-dev libkrb5support0 liblwres60 libmagic1 libmagickcore3 libperl5.10 libpq-dev libpq5 libssl-dev libssl0.9.8 libtiff4 libtiff4-dev libtiffxx0c2 libwbclient0 libxi-dev libxi6 libxml2 libxslt1.1 links linux-libc-dev locales mysql-common openssh-client openssh-server openssl perl perl-base perl-modules perlmagick php5-cli php5-common php5-pgsql postgresql-8.4 postgresql-9.1 postgresql-client-8.4 postgresql-client-9.1 postgresql-client-common postgresql-common postgresql-contrib-9.1 postgresql-server-dev-8.4 postgresql-server-dev-9.1 procps python python-minimal samba-common smbclient sudo sysv-rc sysvinit sysvinit-utils tshark tzdata wireshark-common"} ]}
# {"group":"bionecy", "host":"plateau.bionecy", "category":"disk", "title":"Disk usage in percent", "warnings": [  ], "criticals": [ {"label":"/lib/init/rw", "value":"100.00", "wrange":":92", "crange":":98", "extinfo":""},{"label":"/var/tmp", "value":"100.00", "wrange":":92", "crange":":98", "extinfo":""},{"label":"/var/log", "value":"100.00", "wrange":":92", "crange":":98", "extinfo":""} ], "unknown": [  ]}
# {"group":"bionecy", "host":"foron.bionecy", "category":"disk", "title":"Disk usage in percent", "warnings": [  ], "criticals": [ {"label":"/lib/init/rw", "value":"100.00", "wrange":":92", "crange":":98", "extinfo":""},{"label":"/var/tmp", "value":"100.00", "wrange":":92", "crange":":98", "extinfo":""},{"label":"/var/log", "value":"100.00", "wrange":":92", "crange":":98", "extinfo":""} ], "unknown": [  ]}
# {"group":"siemens", "host":"angouleme2.changouleme.siemens", "category":"", "title":"Pending packages", "warnings": [ {"label":"pending", "value":"1.00", "wrange":"0:0", "crange":":", "extinfo":"ca-certificates"} ], "criticals": [  ], "unknown": [ {"label":"pending", "value":"1.00", "wrange":"0:0", "crange":":", "extinfo":"ca-certificates"} ]}
# {"group":"siemens", "host":"dalvik1.mariotti.siemens", "category":"", "title":"Pending packages", "warnings": [ {"label":"pending", "value":"67.00", "wrange":"0:0", "crange":":", "extinfo":"acpid apache2 apache2-mpm-prefork apache2-utils apache2.2-bin apache2.2-common base-files file foomatic-filters initscripts libapache2-mod-php5 libapr1 libc-bin libc-dev-bin libc6 libc6-dev libcurl3 libcurl3-gnutls libcurl4-openssl-dev libdbd-pg-perl libecpg-compat3 libecpg-dev libecpg6 libfreetype6 libfreetype6-dev libgnutls-dev libgnutls26 libmagic1 libmagickcore3 libpgtypes3 libpng12-0 libpng12-dev libpq-dev libpq5 libssl-dev libssl0.9.8 libtasn1-3 libtasn1-3-dev libtiff4 libvorbis0a libvorbisenc2 libwbclient0 libxi-dev libxi6 libxml2 libxml2-dev linux-libc-dev locales openssh-client openssh-server openssl perlmagick php5-common php5-pgsql postgresql-8.4 postgresql-client-8.4 postgresql-server-dev-8.4 procps python python-dev python-minimal samba-common smbclient sysv-rc sysvinit sysvinit-utils tzdata"} ], "criticals": [  ], "unknown": [ {"label":"pending", "value":"67.00", "wrange":"0:0", "crange":":", "extinfo":"acpid apache2 apache2-mpm-prefork apache2-utils apache2.2-bin apache2.2-common base-files file foomatic-filters initscripts libapache2-mod-php5 libapr1 libc-bin libc-dev-bin libc6 libc6-dev libcurl3 libcurl3-gnutls libcurl4-openssl-dev libdbd-pg-perl libecpg-compat3 libecpg-dev libecpg6 libfreetype6 libfreetype6-dev libgnutls-dev libgnutls26 libmagic1 libmagickcore3 libpgtypes3 libpng12-0 libpng12-dev libpq-dev libpq5 libssl-dev libssl0.9.8 libtasn1-3 libtasn1-3-dev libtiff4 libvorbis0a libvorbisenc2 libwbclient0 libxi-dev libxi6 libxml2 libxml2-dev linux-libc-dev locales openssh-client openssh-server openssl perlmagick php5-common php5-pgsql postgresql-8.4 postgresql-client-8.4 postgresql-server-dev-8.4 procps python python-dev python-minimal samba-common smbclient sysv-rc sysvinit sysvinit-utils tzdata"} ]}
# {"group":"siemens", "host":"bioesterel1.bioesterel", "category":"", "title":"Pending packages", "warnings": [ {"label":"pending", "value":"15.00", "wrange":"0:0", "crange":":", "extinfo":"bind9-host dnsutils ganeti2 libbind9-60 libdns69 libisc62 libisccc60 libisccfg62 liblwres60 libtiff4 libxml2 mysql-common perl perl-base perl-modules"} ], "criticals": [  ], "unknown": [ {"label":"pending", "value":"15.00", "wrange":"0:0", "crange":":", "extinfo":"bind9-host dnsutils ganeti2 libbind9-60 libdns69 libisc62 libisccc60 libisccfg62 liblwres60 libtiff4 libxml2 mysql-common perl perl-base perl-modules"} ]}
# {"group":"siemens", "host":"amiens2.amiens.siemens", "category":"", "title":"Pending packages", "warnings": [ {"label":"pending", "value":"76.00", "wrange":"0:0", "crange":":", "extinfo":"acpid base-files bzip2 dpkg dpkg-dev file foomatic-filters initscripts iotop kpartx krb5-multidev libapr1 libbz2-1.0 libc-ares2 libc-bin libc-dev-bin libc6 libc6-dev libc6-i386 libcurl3 libcurl3-gnutls libcurl4-openssl-dev libdpkg-perl libfreetype6 libfreetype6-dev libgnutls-dev libgnutls26 libgssapi-krb5-2 libgssrpc4 libjasper1 libk5crypto3 libkadm5clnt-mit7 libkadm5srv-mit7 libkdb5-4 libkrb5-3 libkrb5-dev libkrb5support0 libmagic1 libpng12-0 libpng12-dev libpq5 libsmbios-doc libssl-dev libssl0.9.8 libtasn1-3 libtasn1-3-dev libtiff4 libvorbis0a libvorbisenc2 libwbclient0 libxi6 libxml2 linux-libc-dev locales mdadm module-init-tools nfs-common openssh-client openssh-server openssl postgresql-client-8.4 procps python python-minimal samba-common smbclient sysv-rc sysvinit sysvinit-utils tshark tzdata wireshark-common x11-common xpdf xpdf-reader xpdf-utils"} ], "criticals": [  ], "unknown": [ {"label":"pending", "value":"76.00", "wrange":"0:0", "crange":":", "extinfo":"acpid base-files bzip2 dpkg dpkg-dev file foomatic-filters initscripts iotop kpartx krb5-multidev libapr1 libbz2-1.0 libc-ares2 libc-bin libc-dev-bin libc6 libc6-dev libc6-i386 libcurl3 libcurl3-gnutls libcurl4-openssl-dev libdpkg-perl libfreetype6 libfreetype6-dev libgnutls-dev libgnutls26 libgssapi-krb5-2 libgssrpc4 libjasper1 libk5crypto3 libkadm5clnt-mit7 libkadm5srv-mit7 libkdb5-4 libkrb5-3 libkrb5-dev libkrb5support0 libmagic1 libpng12-0 libpng12-dev libpq5 libsmbios-doc libssl-dev libssl0.9.8 libtasn1-3 libtasn1-3-dev libtiff4 libvorbis0a libvorbisenc2 libwbclient0 libxi6 libxml2 linux-libc-dev locales mdadm module-init-tools nfs-common openssh-client openssh-server openssl postgresql-client-8.4 procps python python-minimal samba-common smbclient sysv-rc sysvinit sysvinit-utils tshark tzdata wireshark-common x11-common xpdf xpdf-reader xpdf-utils"} ]}
# {"group":"siemens", "host":"eracles.chclermontfd.siemens", "category":"", "title":"Pending packages", "warnings": [ {"label":"pending", "value":"13.00", "wrange":"0:0", "crange":":", "extinfo":"apache2 apache2-mpm-prefork apache2-utils apache2.2-bin apache2.2-common libperl5.10 libtiff4 libxml2 libxml2-dev mysql-common perl perl-base perl-modules"} ], "criticals": [  ], "unknown": [ {"label":"pending", "value":"13.00", "wrange":"0:0", "crange":":", "extinfo":"apache2 apache2-mpm-prefork apache2-utils apache2.2-bin apache2.2-common libperl5.10 libtiff4 libxml2 libxml2-dev mysql-common perl perl-base perl-modules"} ]}
# {"group":"siemens", "host":"amiens-envtest.amiens.siemens", "category":"", "title":"Pending packages", "warnings": [ {"label":"pending", "value":"103.00", "wrange":"0:0", "crange":":", "extinfo":"acpid apache2 apache2-mpm-prefork apache2-utils apache2.2-bin apache2.2-common base-files bzip2 cifs-utils dpkg dpkg-dev file foomatic-filters initscripts iotop krb5-multidev libapache2-mod-php5 libapr1 libbz2-1.0 libc-ares2 libc-bin libc-dev-bin libc6 libc6-dev libcurl3 libcurl3-gnutls libcurl4-openssl-dev libdbd-pg-perl libdpkg-perl libecpg-compat3 libecpg-dev libecpg6 libfreetype6 libfreetype6-dev libgnutls-dev libgnutls26 libgssapi-krb5-2 libgssrpc4 libicu44 libjasper1 libk5crypto3 libkadm5clnt-mit7 libkadm5srv-mit7 libkdb5-4 libkrb5-3 libkrb5-dev libkrb5support0 libmagic1 libmagickcore3 libperl5.10 libpgtypes3 libpng12-0 libpng12-dev libpq-dev libpq5 libssl-dev libssl0.9.8 libtasn1-3 libtasn1-3-dev libtiff4 libvorbis0a libvorbisenc2 libwbclient0 libxi-dev libxi6 libxml2 libxml2-dev linux-libc-dev locales mdadm module-init-tools nfs-common openssh-client openssh-server openssl perl perl-base perl-modules perlmagick php5-common php5-pgsql postgresql-8.4 postgresql-client-8.4 postgresql-server-dev-8.4 procps python python-dev python-minimal samba-common smbclient smbfs sysv-rc sysvinit sysvinit-utils tshark tzdata wireshark-common x11-common xorg-dev xpdf xpdf-reader xpdf-utils xserver-xorg-dev"} ], "criticals": [  ], "unknown": [ {"label":"pending", "value":"103.00", "wrange":"0:0", "crange":":", "extinfo":"acpid apache2 apache2-mpm-prefork apache2-utils apache2.2-bin apache2.2-common base-files bzip2 cifs-utils dpkg dpkg-dev file foomatic-filters initscripts iotop krb5-multidev libapache2-mod-php5 libapr1 libbz2-1.0 libc-ares2 libc-bin libc-dev-bin libc6 libc6-dev libcurl3 libcurl3-gnutls libcurl4-openssl-dev libdbd-pg-perl libdpkg-perl libecpg-compat3 libecpg-dev libecpg6 libfreetype6 libfreetype6-dev libgnutls-dev libgnutls26 libgssapi-krb5-2 libgssrpc4 libicu44 libjasper1 libk5crypto3 libkadm5clnt-mit7 libkadm5srv-mit7 libkdb5-4 libkrb5-3 libkrb5-dev libkrb5support0 libmagic1 libmagickcore3 libperl5.10 libpgtypes3 libpng12-0 libpng12-dev libpq-dev libpq5 libssl-dev libssl0.9.8 libtasn1-3 libtasn1-3-dev libtiff4 libvorbis0a libvorbisenc2 libwbclient0 libxi-dev libxi6 libxml2 libxml2-dev linux-libc-dev locales mdadm module-init-tools nfs-common openssh-client openssh-server openssl perl perl-base perl-modules perlmagick php5-common php5-pgsql postgresql-8.4 postgresql-client-8.4 postgresql-server-dev-8.4 procps python python-dev python-minimal samba-common smbclient smbfs sysv-rc sysvinit sysvinit-utils tshark tzdata wireshark-common x11-common xorg-dev xpdf xpdf-reader xpdf-utils xserver-xorg-dev"} ]}
# {"group":"siemens", "host":"balcon.changouleme.siemens", "category":"", "title":"Pending packages", "warnings": [ {"label":"pending", "value":"38.00", "wrange":"0:0", "crange":":", "extinfo":"apache2 apache2-mpm-prefork apache2-utils apache2.2-bin apache2.2-common aptitude base-files ca-certificates git git-core grub-common grub-pc krb5-multidev libgl1-mesa-dev libgl1-mesa-glx libglu1-mesa libglu1-mesa-dev libgssapi-krb5-2 libgssrpc4 libk5crypto3 libkadm5clnt-mit7 libkadm5srv-mit7 libkdb5-4 libkrb5-3 libkrb5-dev libkrb5support0 libpcap0.8 libssl-dev libssl0.9.8 linux-libc-dev mesa-common-dev openssh-client openssh-server openssl tzdata update-inetd usbutils vsftpd"} ], "criticals": [  ], "unknown": [ {"label":"pending", "value":"38.00", "wrange":"0:0", "crange":":", "extinfo":"apache2 apache2-mpm-prefork apache2-utils apache2.2-bin apache2.2-common aptitude base-files ca-certificates git git-core grub-common grub-pc krb5-multidev libgl1-mesa-dev libgl1-mesa-glx libglu1-mesa libglu1-mesa-dev libgssapi-krb5-2 libgssrpc4 libk5crypto3 libkadm5clnt-mit7 libkadm5srv-mit7 libkdb5-4 libkrb5-3 libkrb5-dev libkrb5support0 libpcap0.8 libssl-dev libssl0.9.8 linux-libc-dev mesa-common-dev openssh-client openssh-server openssl tzdata update-inetd usbutils vsftpd"} ]}
# {"group":"siemens", "host":"bioesterel-ol2.bioesterel.siemens", "category":"", "title":"Pending packages", "warnings": [ {"label":"pending", "value":"23.00", "wrange":"0:0", "crange":":", "extinfo":"apache2 apache2-mpm-prefork apache2-utils apache2.2-bin apache2.2-common bind9-host dnsutils libbind9-60 libdns69 libisc62 libisccc60 libisccfg62 liblwres60 libperl5.10 libtiff4 libxml2 libxml2-dev mysql-common perl perl-base perl-modules postgresql-client-common postgresql-common"} ], "criticals": [  ], "unknown": [ {"label":"pending", "value":"23.00", "wrange":"0:0", "crange":":", "extinfo":"apache2 apache2-mpm-prefork apache2-utils apache2.2-bin apache2.2-common bind9-host dnsutils libbind9-60 libdns69 libisc62 libisccc60 libisccfg62 liblwres60 libperl5.10 libtiff4 libxml2 libxml2-dev mysql-common perl perl-base perl-modules postgresql-client-common postgresql-common"} ]}
# {"group":"siemens", "host":"bioesterel2.bioesterel.siemens", "category":"", "title":"Pending packages", "warnings": [ {"label":"pending", "value":"23.00", "wrange":"0:0", "crange":":", "extinfo":"apache2 apache2-mpm-prefork apache2-utils apache2.2-bin apache2.2-common bind9-host dnsutils libbind9-60 libdns69 libisc62 libisccc60 libisccfg62 liblwres60 libperl5.10 libtiff4 libxml2 libxml2-dev mysql-common perl perl-base perl-modules postgresql-client-common postgresql-common"} ], "criticals": [  ], "unknown": [ {"label":"pending", "value":"23.00", "wrange":"0:0", "crange":":", "extinfo":"apache2 apache2-mpm-prefork apache2-utils apache2.2-bin apache2.2-common bind9-host dnsutils libbind9-60 libdns69 libisc62 libisccc60 libisccfg62 liblwres60 libperl5.10 libtiff4 libxml2 libxml2-dev mysql-common perl perl-base perl-modules postgresql-client-common postgresql-common"} ]}
# {"group":"siemens", "host":"amiens1.amiens.siemens", "category":"", "title":"Pending packages", "warnings": [ {"label":"pending", "value":"76.00", "wrange":"0:0", "crange":":", "extinfo":"acpid base-files bzip2 dpkg dpkg-dev file foomatic-filters ganeti2 initscripts iotop kpartx krb5-multidev libapr1 libbz2-1.0 libc-ares2 libc-bin libc-dev-bin libc6 libc6-dev libc6-i386 libcurl3-gnutls libdpkg-perl libfreetype6 libfreetype6-dev libgnutls-dev libgnutls26 libgssapi-krb5-2 libgssrpc4 libjasper1 libk5crypto3 libkadm5clnt-mit7 libkadm5srv-mit7 libkdb5-4 libkrb5-3 libkrb5-dev libkrb5support0 libmagic1 libpng12-0 libpng12-dev libpq5 libsmbios-doc libssl-dev libssl0.9.8 libtasn1-3 libtasn1-3-dev libtiff4 libvorbis0a libvorbisenc2 libwbclient0 libxi6 libxml2 linux-libc-dev locales mdadm module-init-tools nfs-common openssh-client openssh-server openssl postgresql-client postgresql-client-8.4 procps python python-minimal samba-common smbclient sysv-rc sysvinit sysvinit-utils tshark tzdata wireshark-common x11-common xpdf xpdf-reader xpdf-utils"} ], "criticals": [  ], "unknown": [ {"label":"pending", "value":"76.00", "wrange":"0:0", "crange":":", "extinfo":"acpid base-files bzip2 dpkg dpkg-dev file foomatic-filters ganeti2 initscripts iotop kpartx krb5-multidev libapr1 libbz2-1.0 libc-ares2 libc-bin libc-dev-bin libc6 libc6-dev libc6-i386 libcurl3-gnutls libdpkg-perl libfreetype6 libfreetype6-dev libgnutls-dev libgnutls26 libgssapi-krb5-2 libgssrpc4 libjasper1 libk5crypto3 libkadm5clnt-mit7 libkadm5srv-mit7 libkdb5-4 libkrb5-3 libkrb5-dev libkrb5support0 libmagic1 libpng12-0 libpng12-dev libpq5 libsmbios-doc libssl-dev libssl0.9.8 libtasn1-3 libtasn1-3-dev libtiff4 libvorbis0a libvorbisenc2 libwbclient0 libxi6 libxml2 linux-libc-dev locales mdadm module-init-tools nfs-common openssh-client openssh-server openssl postgresql-client postgresql-client-8.4 procps python python-minimal samba-common smbclient sysv-rc sysvinit sysvinit-utils tshark tzdata wireshark-common x11-common xpdf xpdf-reader xpdf-utils"} ]}
# {"group":"siemens", "host":"angouleme1.changouleme.siemens", "category":"", "title":"Pending packages", "warnings": [ {"label":"pending", "value":"32.00", "wrange":"0:0", "crange":":", "extinfo":"aptitude base-files ca-certificates git grub-common grub-pc krb5-multidev libgl1-mesa-dev libgl1-mesa-glx libglu1-mesa libglu1-mesa-dev libgssapi-krb5-2 libgssrpc4 libk5crypto3 libkadm5clnt-mit7 libkadm5srv-mit7 libkdb5-4 libkrb5-3 libkrb5-dev libkrb5support0 libpcap0.8 libssl-dev libssl0.9.8 linux-libc-dev mesa-common-dev openssh-client openssh-server openssl tzdata update-inetd usbutils vsftpd"} ], "criticals": [  ], "unknown": [ {"label":"pending", "value":"32.00", "wrange":"0:0", "crange":":", "extinfo":"aptitude base-files ca-certificates git grub-common grub-pc krb5-multidev libgl1-mesa-dev libgl1-mesa-glx libglu1-mesa libglu1-mesa-dev libgssapi-krb5-2 libgssrpc4 libk5crypto3 libkadm5clnt-mit7 libkadm5srv-mit7 libkdb5-4 libkrb5-3 libkrb5-dev libkrb5support0 libpcap0.8 libssl-dev libssl0.9.8 linux-libc-dev mesa-common-dev openssh-client openssh-server openssl tzdata update-inetd usbutils vsftpd"} ]}
# {"group":"siemens", "host":"bioesterel1.bioesterel.siemens", "category":"", "title":"Pending packages", "warnings": [ {"label":"pending", "value":"15.00", "wrange":"0:0", "crange":":", "extinfo":"bind9-host dnsutils ganeti2 libbind9-60 libdns69 libisc62 libisccc60 libisccfg62 liblwres60 libtiff4 libxml2 mysql-common perl perl-base perl-modules"} ], "criticals": [  ], "unknown": [ {"label":"pending", "value":"15.00", "wrange":"0:0", "crange":":", "extinfo":"bind9-host dnsutils ganeti2 libbind9-60 libdns69 libisc62 libisccc60 libisccfg62 liblwres60 libtiff4 libxml2 mysql-common perl perl-base perl-modules"} ]}
# {"group":"siemens", "host":"bioesterel2.bioesterel", "category":"", "title":"Pending packages", "warnings": [ {"label":"pending", "value":"15.00", "wrange":"0:0", "crange":":", "extinfo":"bind9-host dnsutils ganeti2 libbind9-60 libdns69 libisc62 libisccc60 libisccfg62 liblwres60 libtiff4 libxml2 mysql-common perl perl-base perl-modules"} ], "criticals": [  ], "unknown": [ {"label":"pending", "value":"15.00", "wrange":"0:0", "crange":":", "extinfo":"bind9-host dnsutils ganeti2 libbind9-60 libdns69 libisc62 libisccc60 libisccfg62 liblwres60 libtiff4 libxml2 mysql-common perl perl-base perl-modules"} ]}
# """

class Alert(object):
    def __init__(self, atype, data):
        super(Alert, self).__init__()
        assert(atype in ("warning", "critical"))
        self.data = data
        self.type = atype
        self.label = data["label"]
        self.value = data["value"]
        self.extinfo = data["extinfo"]
        if atype == "warning":
            self.range = data.get("wrange", "")
        elif atype == "critical":
            self.range = data.get("crange", "")

class HostAlert(object):
    def __init__(self, json_data):
        super(HostAlert, self).__init__()
        self.json_data = json_data
        self.host = self.json_data["host"]
        self.group = self.json_data["group"]
        self.category = self.json_data["category"]
        self.title = self.json_data["title"]
        self.alerts = []
        for warn in self.json_data.get("warnings", []):
            self.alerts.append(Alert("warning", warn))
        for crit in self.json_data.get("criticals", []):
            self.alerts.append(Alert("critical", crit))

    def alertsdict(self):
        ret = []
        for alert in self.alerts:
            ret.append({
                "host": self.host, "group": self.group,
                "category": self.category, "title": self.title,
                "type": alert.type, "label": alert.label,
                "value": alert.value, "range": alert.range,
                "extinfo": alert.extinfo})
        return ret

    def __str__(self):
        return "%s@%s %d warnings %d criticals" % (self.json_data["host"],
                                      self.json_data["group"],
                                      len(self.json_data.get("warnings", [])),
                                      len(self.json_data.get("criticals", [])))
    def __repr__(self):
        return self.__str__()

class Decoder(object):
    """Read inputfile and decode using json.loads each line."""
    def __init__(self, inputfile):
        self.inputfile = inputfile
        self.output = []

    def read(self):
        self.output = []

        lineidx = 0
        while True:
            line = self.inputfile.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue
            lineidx += 1
            try:
                self.output.append(self.decode(line))
            except ValueError:
                logger.exception("Unable to decode line %d." % (lineidx,))
        return self.output

    def decode(self, line):
        return json.loads(line)

class AlertFactory(object):
    def __init__(self, hostalertklass=HostAlert):
        self.klass = hostalertklass
        super(AlertFactory, self).__init__()

    def build(self, json_data):
        return self.klass(json_data)

class DBSync(object):
    def __init__(self, db):
        self.db = db
        super(DBSync, self).__init__()

    def sync(self, hostalerts):
        c = self.db.cursor()
        for host in hostalerts:
            for alert in host.alerts:
                c.execute("""INSERT INTO muninalerts (host, "group", category, title, label, value, type, range) """ \
                          """ VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
                    (host.host, host.group, host.category, host.title, alert.label, alert.value, alert.type, alert.range))
        self.db.commit()

class HttpSync(object):
    def __init__(self, url):
        self.url = url

    def sync(self, hostalerts):
        alerts = []
        for host in hostalerts:
            alerts.extend(host.alertsdict())
        postdata = {'alerts': json.dumps(alerts) }
        request = urllib2.Request(url=self.url, data=urllib.urlencode(postdata))
        request.add_header('User-agent', 'MuninAlerts/1.0')
        try:
            urlf = urllib2.urlopen(request, timeout=20)
            rawdata = urlf.read()
            logger.debug("Received: %s", rawdata)
            urlf.close()
        except urllib2.URLError, e:
            if hasattr(e, "read"):
                print e.read()
            else:
                logger.exception(u"URLError. No internet access?")
            raise
        except urllib2.HTTPError, e:
            if e.code == 403:
                logger.error(u"Access denied.")
            raise
        except Exception, e:
            logger.exception("URLLIB2 exception.")
            raise

if __name__ == "__main__":
    from cStringIO import StringIO
    logging.basicConfig(level=logging.DEBUG)

    factory = AlertFactory()
    
    sio = StringIO()
    # sio.write(sample_data)
    sio.write(sys.stdin.read())
    sio.seek(0)

    decoder = Decoder(sio)
    hostalerts = []
    for json_alert in decoder.read():
        hostalerts.append(factory.build(json_alert))

    # DB SYNC
    # import sqlite3
    # db = sqlite3.connect(os.path.join(
    #         os.path.abspath(os.path.dirname(__file__)),
    #         "minialerts", "muninalerts.db"))

    # dbsync = DBSync(db)
    # dbsync.sync(hostalerts)

    # db.close()

    # HTTP Sync
    syncer = HttpSync("http://10.31.254.20:8000/alerts/push/")
    syncer.sync(hostalerts)

    sys.exit(0)
