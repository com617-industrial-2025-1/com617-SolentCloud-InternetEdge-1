#!/bin/bash

# List of target IPs on the internet_client
TARGETS=("8.8.8.2" "9.9.9.2" "185.1.1.100" "185.2.2.100")

echo "Starting sequential traceroutes from dc_server..."
echo "------------------------------------------------"

for IP in "${TARGETS[@]}"; do
    echo "[STARTED] Traceroute to $IP..."
    # Notice we removed the '&' at the end of this line!
    docker exec clab-ixp-te-lab-dc_server traceroute -n "$IP" > "trace_$IP.log" 2>&1
done

echo "------------------------------------------------"
echo "All traceroutes complete. Results saved to .log files."

for IP in "${TARGETS[@]}"; do
    echo -e "\n--- Results for $IP ---"
    cat "trace_$IP.log"
done
