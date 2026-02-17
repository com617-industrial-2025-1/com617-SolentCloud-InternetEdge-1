import subprocess
import re
import json

# Dictionary mapping node names to their OS type
nodes = {
    "core_router_1": "sr_linux", 
    "core_router_2": "sr_linux", 
    "dc_router_1": "sr_linux", 
    "dc_router_2": "sr_linux",
    "edge_router_1": "sr_linux", 
    "edge_router_2": "sr_linux",
    "isp_bt": "sr_linux", 
    "isp_vmo2": "sr_linux",
    "ixp_lon": "frr",
    "ixp_man": "frr"
}

def run_cmd(node, node_type, cmd):
    # Use sr_cli for Nokia routers, vtysh for FRR route servers
    if node_type == "sr_linux":
        full_cmd = f"docker exec clab-ixp-te-lab-{node} sr_cli '{cmd}'"
    elif node_type == "frr":
        full_cmd = f"docker exec clab-ixp-te-lab-{node} vtysh -c '{cmd}'"
        
    try:
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception:
        return ""

print(f"\n{'Node':<20} | {'OSPF (Full)':<15} | {'BGP (Established)'}")
print("-" * 55)

for node, node_type in nodes.items():
    if node_type == "sr_linux":
        # Check Nokia SR Linux Nodes
        ospf_out = run_cmd(node, node_type, "show network-instance default protocols ospf neighbor")
        bgp_out = run_cmd(node, node_type, "show network-instance default protocols bgp neighbor")
        
        # Count OSPF Full states
        ospf_count = ospf_out.lower().count("full")
        
        # Extract BGP Established count
        bgp_match = re.search(r'(\d+)\s+configured sessions are established', bgp_out.lower())
        bgp_count = int(bgp_match.group(1)) if bgp_match else 0
        
        ospf_str = f"{ospf_count} Neighbors"
        bgp_str = f"{bgp_count} Up"
        
    elif node_type == "frr":
        # IXPs do not run OSPF in this topology
        ospf_str = "N/A"
        
        # Request BGP Summary in JSON format for easy parsing
        bgp_out = run_cmd(node, node_type, "show bgp summary json")
        bgp_count = 0
        
        try:
            data = json.loads(bgp_out)
            # Traverse the JSON tree to find IPv4 Unicast peers
            peers = data.get("ipv4Unicast", {}).get("peers", {})
            for peer_ip, peer_data in peers.items():
                if peer_data.get("state") == "Established":
                    bgp_count += 1
        except Exception:
            # Fallback to standard text parsing if JSON fails
            bgp_text = run_cmd(node, node_type, "show bgp summary").lower()
            for line in bgp_text.split('\n'):
                # Look for lines that start with an IP address
                if re.search(r'^\s*(?:[0-9]{1,3}\.){3}[0-9]{1,3}', line):
                    # If the state isn't active, idle, or connect, it is established
                    if not any(state in line for state in ['active', 'idle', 'connect']):
                        bgp_count += 1
                        
        bgp_str = f"{bgp_count} Up"

    print(f"{node:<20} | {ospf_str:<15} | {bgp_str}")
