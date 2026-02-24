# SolentCloud BGP Traffic Engineering Runbook: POC Phase

**Document Purpose:** This runbook provides SolentCloud engineers with the exact procedures to manually trigger Ansible playbooks that manipulate BGP attributes during the Proof of Concept (POC) phase. 

**Infrastructure Context:** SolentCloud is a cloud provider based in the South of England. They provide a range of cloud services to large enterprises across the UK. The network is comprised of Cisco equipment. The edge topology consists of four 25G connections, currently transitioning to a hybrid model of 2 Transit ISPs and 2 Internet Exchange Points (IXPs), favoring the IXPs to lower operational costs. At busiest times, bandwidth consumption at the Internet edge has peaked at 72Gbps.

---

## 1. Failover Trigger Conditions & Thresholds

During the POC, alerting systems will notify the engineer, who must validate the condition before manually executing the corresponding Ansible playbook. BGP attribute manipulation is used to shift traffic away from a problematic ISP or IXP.

### A. Hard Failures (State/Protocol Changes)
* **Physical Link Loss:** Carrier loss of signal (interface `down/down`).
    * **Action:** Immediate failover.
    * **Revert:** Link remains consistently `up/up` for 5 minutes.
* **BGP Peer/Protocol Loss:** Physical link is up, but BGP session drops.
    * **Action:** Immediate failover.
    * **Revert:** BGP session established and stable for 3 minutes.
* **IXP Route Server Failure:** Loss of session specifically to the IXP Route Server.
    * **Action:** Shift general peer traffic to ISPs, but maintain bilateral direct BGP sessions if still active.
    * **Revert:** Route Server session stable for 5 minutes.

### B. Soft Failures (Quality Degradation)
* **Severe Packet Loss:** Packet loss >= 50% sustained for 10 seconds.
    * **Revert:** Packet loss < 2.5% sustained for 2 minutes.
    * **Note:** SolentCloud has experienced packet loss and high latency via certain ISPs, making this a primary failover driver.
* **Moderate Packet Loss:** Packet loss > 5% sustained for 1 minute.
    * **Revert:** Packet loss < 2.5% sustained for 2 minutes.
* **Latency (RTT) Spikes:** RTT exceeds > 10ms average over 30 seconds.
    * **Revert:** RTT < 5ms average over 1 minute.
* **Jitter (Delay Variation):** Jitter variance > 5ms over a 30-second window.
    * **Revert:** Jitter stabilizes to < 2ms for 2 minutes.

### C. Capacity & Hardware Conditions
* **Link Saturation:** Egress utilization on any 25G link exceeds 85% for 3 minutes.
    * **Action:** Shed specific low-priority prefixes to a secondary link to avoid buffer drops.
    * **Revert:** Target link utilization drops below 70% for 5 minutes.
* **Router Resource Exhaustion:** Cisco edge router CPU > 90% or Memory > 85% for 3 minutes.
    * **Action:** Temporarily suspend full-table BGP peering on the affected router (fallback to default route peering) to relieve control-plane stress.
    * **Revert:** CPU < 60% and Memory < 70% for 5 minutes.

---

## 2. Execution Procedure (POC Phase)

### Phase 1: Alert Validation
1.  Receive critical alert matching one of the thresholds in **Section 1**.
2.  Log into the affected Cisco edge router via SSH/Console.
3. Run diagnostic commands to confirm the issue is isolated to the specific ISP/IXP link and not an internal SolentCloud DC issue.
    * *Command:* `show ip bgp summary` (Check peer state)
    * *Command:* `show interface [ID]` (Check link utilization and physical errors)

### Phase 2: Ansible Playbook Execution (Isolation)
From the Ansible Control Node, execute the playbook corresponding to the degraded path. These playbooks manipulate BGP attributes for inbound and outbound traffic. 
* *Outbound Manipulation:* Lowers `Local_Pref` to 50 for routes learned from the degraded peer.
* *Inbound Manipulation:* Prepends the SolentCloud ASN 3 times to route advertisements sent to the degraded peer.

**Playbook Commands:**
* Degraded ISP 1: `ansible-playbook /opt/runbooks/bgp/isolate_isp1.yml`
* Degraded ISP 2: `ansible-playbook /opt/runbooks/bgp/isolate_isp2.yml`
* Degraded IXP 1: `ansible-playbook /opt/runbooks/bgp/isolate_ixp1.yml`
* Degraded IXP 2: `ansible-playbook /opt/runbooks/bgp/isolate_ixp2.yml`

### Phase 3: Post-Execution Verification
1.  **Verify Egress Traffic (Immediate):** Run `show ip bgp` on the edge routers to confirm the best path has updated and no longer prefers the degraded link.
2.  **Verify Ingress Traffic (Delayed):** Monitor flow analytics. Inbound traffic will drain gradually over 2 to 5 minutes as the AS-Path prepending propagates across the global internet.
3. **Monitor Capacity:** Ensure the combined traffic on the remaining links does not exceed their cumulative capacity, keeping in mind peak loads can reach 72Gbps.

### Phase 4: Reversion (Rollback)
Once monitoring confirms the degraded link has met the "Revert" criteria defined in **Section 1**, restore the traffic flow.

1.  Execute the restoration playbook to remove the AS-Path prepending and restore standard `Local_Pref`:
    * *Command (Example):* `ansible-playbook /opt/runbooks/bgp/restore_isp1.yml`
2.  Verify link utilization balances out to expected baseline levels across the topology.
