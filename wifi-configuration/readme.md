# Enabling Work@Home
This document contains the commands and manual steps that need to be done to enable the optional feature of working from home on this hardware test-bed.
This feature provides SSH access to gain entry into the hardware test-bed.
It also allows reaching and managing all other switches and components through an out-of-band channel to not affect the test-setup.
In this example, the Raspberry Pi's are reached through a WiFi hotspot, and the NXP switches are reached through a serial interface.
It is loosely based on the following documentation:  https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-routed-wireless-access-point

## Preparing the device
Run the following commands to install the required packages and enable the required services:
```bash
sudo apt update
sudo apt upgrade
sudo apt install hostapd dnsmasq netfilter-persistent iptables-persistent
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
```

## Configuring the device
In addition to installing the required packages and service, they need to be configured.
To do this we recommend taking the device offline and manually copying the configuration files to the microSD card.

Make sure to do the following steps:
- Manually copy the configuration file to `/etc/dhcpcd.conf`
- Manually copy the configuration file to `/etc/dnsmasq.conf`
- Manually copy the configuration file to `/etc/hostapd/hostapd.conf`
- Manually copy the configuration file to `/etc/sysctl.conf`
- Manually copy the configuration file to `/etc/iptables/rules.v4`

All devices that are required to make a connection to the created hotspot should place the `wpa_supplicant.conf` file in `/etc/wpa_supplicant/wpa_supplicant.conf`.

## Crontab to find the rPi
During the experimenting phase, the hardware testbed was remotely accessible while running in the TU Delft building.
It did not have a hostname and therefore the IP address might change.
I have used the following cronjob to always be able to find it:

```* * * * * /usr/bin/curl -I https://adriaandevos.nl/here-i-am/$(/usr/bin/curl ifconfig.me) >/dev/null 2>&1```

