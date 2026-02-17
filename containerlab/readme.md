# Solent Cloud - Internet Edge Lab

## Boot Instructions

**Important Note:** The IXP nodes act as Layer 2 bridges and BGP Route Servers. Their virtual cables must be fully connected by the hypervisor before their internal bridges can be built. To guarantee the lab boots successfully, you must follow this exact sequence.

### Prerequisites
Navigate to the `containerlab` directory where the topology and scripts are located:
```bash
cd containerlab
```

Step 1: Deploy the Lab

Use Containerlab to build the virtual wiring, boot all containers, and apply the startup configurations to the Nokia SR Linux routers.

```bash
sudo containerlab deploy -t solent_cloud.clab.yaml
```

(Note: If you are recovering from a broken state or applying new configuration files, append --reconfigure to the command to force a clean rebuild).
Step 2: Initialise the IXP Route Servers

Once Containerlab finishes deploying, the FRR containers will be online, but their Layer 2 bridges and BGP daemons need to be initialised.

Run the included setup script. This safely builds the br0 interfaces, assigns the IP addresses, and natively starts the BGP daemon (bgpd) for both the London and Manchester IXPs.
Bash

# Ensure the script is executable (only needed once)

``chmod +x setup_ixps.sh``

# Run the initialisation

``./setup_ixps.sh``

Step 3: Verify Network Health

BGP sessions typically take between 15 to 30 seconds to establish after the IXPs are initialised. You can monitor the status of the entire lab using the custom Python health script.
Bash

``python3 network_health.py``

Expected Output for a 100% Healthy Lab:

```Plaintext

Node                 | OSPF (Full)     | BGP (Established)
-------------------------------------------------------
core_router_1        | 5 Neighbors     | 3 Up
core_router_2        | 5 Neighbors     | 3 Up
dc_router_1          | 2 Neighbors     | 0 Up
dc_router_2          | 2 Neighbors     | 0 Up
edge_router_1        | 2 Neighbors     | 5 Up
edge_router_2        | 2 Neighbors     | 5 Up
isp_bt               | 0 Neighbors     | 1 Up
isp_vmo2             | 0 Neighbors     | 1 Up
ixp_lon              | N/A             | 2 Up
ixp_man              | N/A             | 2 Up
```

(If the Edge Routers are stuck at 4 Up or 3 Up, wait 10 more seconds and run the script again.)

# Accessing the Nodes

You can access the command line interface of any router in the lab using Docker:

For Nokia SR Linux Routers (Core, DC, Edge, ISPs):

```Bash
docker exec -it clab-ixp-te-lab-edge_router_1 sr_cli
```
For FRRouting Route Servers (IXPs):

```Bash
docker exec -it clab-ixp-te-lab-ixp_lon vtysh
```
Teardown

To gracefully stop the lab and destroy the virtual network cables (this does not delete your saved configuration files):

```Bash
sudo containerlab destroy -t solent_cloud.clab.yaml
```
