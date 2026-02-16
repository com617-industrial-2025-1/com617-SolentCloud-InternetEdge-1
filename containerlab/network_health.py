import subprocess
import re

nodes = [
    "core_router_1", "core_router_2", 
    "dc_router_1", "dc_router_2",
    "edge_router_1", "edge_router_2",
    "isp_bt", "isp_vmo2"
]

def run_cmd(node, cmd):
    full_cmd = f"docker exec clab-ixp-te-lab-{node} sr_cli '{cmd}'"
    try:
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
        return result.stdout.lower()
    except Exception:
        return ""

print(f"\n{'Node':<20} | {'OSPF (Full)':<15} | {'BGP (Established)'}")
print("-" * 55)

for node in nodes:
    # Get raw text outputs
    ospf_out = run_cmd(node, "show network-instance default protocols ospf neighbor")
    bgp_out = run_cmd(node, "show network-instance default protocols bgp neighbor")
    
    # Count OSPF Full states
    ospf_count = ospf_out.count("full")
    
    # Extract BGP Established count using Regex to find "X configured sessions are established"
    bgp_match = re.search(r'(\d+)\s+configured sessions are established', bgp_out)
    bgp_count = int(bgp_match.group(1)) if bgp_match else 0
    
    # Format the output
    ospf_str = f"{ospf_count} Neighbors"
    bgp_str = f"{bgp_count} Up"
    
    print(f"{node:<20} | {ospf_str:<15} | {bgp_str}")
