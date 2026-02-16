docker exec -i clab-ixp-te-lab-ixp_lon sh -c "
  ip link add br0 type bridge 2>/dev/null || true
  ip link set eth1 master br0 && ip link set eth2 master br0
  ip link set br0 up && ip addr add 185.1.1.254/24 dev br0 2>/dev/null || true
  vtysh -c 'conf t' -c 'router bgp 65500' -c 'no bgp ebgp-requires-policy' -c 'neighbor 185.1.1.5 remote-as 65000' -c 'neighbor 185.1.1.6 remote-as 65000'
"
docker exec -i clab-ixp-te-lab-ixp_man sh -c "
  ip link add br0 type bridge 2>/dev/null || true
  ip link set eth1 master br0 && ip link set eth2 master br0
  ip link set br0 up && ip addr add 185.2.2.254/24 dev br0 2>/dev/null || true
  vtysh -c 'conf t' -c 'router bgp 65501' -c 'no bgp ebgp-requires-policy' -c 'neighbor 185.2.2.5 remote-as 65000' -c 'neighbor 185.2.2.6 remote-as 65000'
"
