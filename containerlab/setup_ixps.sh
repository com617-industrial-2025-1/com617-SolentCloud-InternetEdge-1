#!/bin/bash

echo "--- Configuring London IXP ---"
docker exec -i clab-ixp-te-lab-ixp_lon ip link add br0 type bridge 2>/dev/null
docker exec -i clab-ixp-te-lab-ixp_lon ip link set eth1 master br0
docker exec -i clab-ixp-te-lab-ixp_lon ip link set eth2 master br0
docker exec -i clab-ixp-te-lab-ixp_lon ip link set eth3 master br0
docker exec -i clab-ixp-te-lab-ixp_lon ip link set br0 up
docker exec -i clab-ixp-te-lab-ixp_lon ip addr add 185.1.1.254/24 dev br0 2>/dev/null

# Force BGP process to start and inject config
docker exec -i clab-ixp-te-lab-ixp_lon sed -i 's/bgpd=no/bgpd=yes/' /etc/frr/daemons
docker exec -d clab-ixp-te-lab-ixp_lon /usr/lib/frr/bgpd -d 2>/dev/null
sleep 2

echo "--- Configuring Manchester IXP ---"
docker exec -i clab-ixp-te-lab-ixp_man ip link add br0 type bridge 2>/dev/null
docker exec -i clab-ixp-te-lab-ixp_man ip link set eth1 master br0
docker exec -i clab-ixp-te-lab-ixp_man ip link set eth2 master br0
docker exec -i clab-ixp-te-lab-ixp_man ip link set eth3 master br0
docker exec -i clab-ixp-te-lab-ixp_man ip link set br0 up
docker exec -i clab-ixp-te-lab-ixp_man ip addr add 185.2.2.254/24 dev br0 2>/dev/null

# Force BGP process to start and inject config
docker exec -i clab-ixp-te-lab-ixp_man sed -i 's/bgpd=no/bgpd=yes/' /etc/frr/daemons
docker exec -d clab-ixp-te-lab-ixp_man /usr/lib/frr/bgpd -d 2>/dev/null

echo "--- Done! BGP Sessions will establish within 15-30 seconds ---"
