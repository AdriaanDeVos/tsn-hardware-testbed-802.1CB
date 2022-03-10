# https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-routed-wireless-access-point
sudo apt update
sudo apt upgrade
sudo apt install hostapd dnsmasq netfilter-persistent iptables-persistent
sudo systemctl unmask hostapd
sudo systemctl enable hostapd

# Manually copy the configuration file to /etc/dhcpcd.conf
# Manually copy the configuration file to /etc/dnsmasq.conf
# Manually copy the configuration file to /etc/hostapd/hostapd.conf
# Manually copy the configuration file to /etc/sysctl.conf
# Manually copy the configuration file to /etc/iptables/rules.v4
