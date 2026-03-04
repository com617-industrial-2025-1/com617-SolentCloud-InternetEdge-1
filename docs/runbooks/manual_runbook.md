# SolentCloud Traffic Engineering: Manual CLI Runbook

This runbook provides the exact CLI commands to manually perform the BGP traffic shaping operations defined in the Ansible playbooks. These commands should be used if the Ansible control node is unavailable or if a manual, step-by-step intervention is required based on the defined trigger conditions.

## 1. Trigger Conditions Reference

| Condition | Trigger Threshold | Reversion Criteria |
| :--- | :--- | :--- |
| **A. Hard Failures** | | |
| Physical Link Loss | Carrier loss of signal (interface `down/down`) | Link remains consistently `up/up` for 5 minutes |
| BGP Peer/Protocol Loss | Physical link is up, but BGP session drops | BGP session established and stable for 3 minutes |
| IXP Route Server Failure | Loss of session specifically to the IXP Route Server | Route Server session stable for 5 minutes |
| **B. Soft Failures** | | |
| Severe Packet Loss | Packet loss >= 50% sustained for 10 seconds | Packet loss < 2.5% sustained for 2 minutes |
| Moderate Packet Loss | Packet loss > 5% sustained for 1 minute | Packet loss < 2.5% sustained for 2 minutes |
| Latency (RTT) Spikes | RTT exceeds > 10ms average over 30 seconds | RTT < 5ms average over 1 minute |
| Jitter (Delay Variation) | Jitter variance > 5ms over a 30-second window | Jitter stabilizes to < 2ms for 2 minutes |
| **C. Capacity & Hardware** | | |
| Link Saturation | Egress utilization on any 25G link exceeds 85% for 3 minutes | Target link utilization drops below 70% for 5 minutes |
| Router Resource Exhaustion| Cisco edge router CPU > 90% or Memory > 85% for 3 minutes | CPU < 60% and Memory < 70% for 5 minutes |


# 2. Manual Execution Procedures

Before running these commands, log into the specific edge router via SSH:

## ISP Failover (BT & VMO2)

### Degrade BT ISP (Edge Router 1)

Use when BT ISP meets a trigger condition.

```Bash
enter candidate
set / routing-policy policy DEGRADE-ISP default-action policy-result accept
set / routing-policy policy DEGRADE-ISP default-action bgp local-preference set 50
set / routing-policy policy DEGRADE-ISP default-action bgp as-path prepend as-number 65000 repeat-n 3
set / network-instance default protocols bgp group EBGP-BT export-policy [ DEGRADE-ISP ] import-policy [ DEGRADE-ISP ]
commit save
```

### Degrade VMO2 ISP (Edge Router 2)

Use when VMO2 ISP meets a trigger condition.

```Bash
enter candidate
set / routing-policy policy DEGRADE-ROUTE default-action policy-result accept
set / routing-policy policy DEGRADE-ROUTE default-action bgp local-preference set 50
set / routing-policy policy DEGRADE-ROUTE default-action bgp as-path prepend as-number 65000 repeat-n 3
set / network-instance default protocols bgp group EBGP-VMO2 export-policy [ DEGRADE-ROUTE ] import-policy [ DEGRADE-ROUTE ]
commit save
```

## IXP Failover (London & Manchester)

Note: These changes must be applied to both Edge Router 1 and Edge Router 2.

### Degrade London IXP (IXP-LON)

Use when London IXP meets a trigger condition.

```Bash
enter candidate
set / routing-policy policy DEGRADE-ROUTE default-action policy-result accept
set / routing-policy policy DEGRADE-ROUTE default-action bgp local-preference set 50
set / routing-policy policy DEGRADE-ROUTE default-action bgp as-path prepend as-number 65000 repeat-n 3
set / network-instance default protocols bgp group IXP-LON export-policy [ DEGRADE-ROUTE ] import-policy [ DEGRADE-ROUTE ]
commit save
```

### Degrade Manchester IXP (IXP-MAN)

Use when Manchester IXP meets a trigger condition.

```Bash
enter candidate
set / routing-policy policy DEGRADE-ROUTE default-action policy-result accept
set / routing-policy policy DEGRADE-ROUTE default-action bgp local-preference set 50
set / routing-policy policy DEGRADE-ROUTE default-action bgp as-path prepend as-number 65000 repeat-n 3
set / network-instance default protocols bgp group IXP-MAN export-policy [ DEGRADE-ROUTE ] import-policy [ DEGRADE-ROUTE ]
commit save
```

# 3. Restoration Procedures (Reversion)

Once the "Revert" criteria are met, restore the ACCEPT-ALL policy to return to baseline routing.

| Target to Restore | Affected Router(s) | BGP Group | Command to Revert to Normal |
| :--- | :--- | :--- | :--- |
| **BT ISP** | Edge Router 1 | `EBGP-BT` | `set / network-instance default protocols bgp group EBGP-BT export-policy [ ACCEPT-ALL ] import-policy [ ACCEPT-ALL ]` |
| **VMO2 ISP** | Edge Router 2 | `EBGP-VMO2` | `set / network-instance default protocols bgp group EBGP-VMO2 export-policy [ ACCEPT-ALL ] import-policy [ ACCEPT-ALL ]` |
| **London IXP** | Edge 1 & Edge 2 | `IXP-LON` | `set / network-instance default protocols bgp group IXP-LON export-policy [ ACCEPT-ALL ] import-policy [ ACCEPT-ALL ]` |
| **Manchester IXP** | Edge 1 & Edge 2 | `IXP-MAN` | `set / network-instance default protocols bgp group IXP-MAN export-policy [ ACCEPT-ALL ] import-policy [ ACCEPT-ALL ]` |