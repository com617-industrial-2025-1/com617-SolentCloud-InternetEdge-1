# Answers

- Largest IXP in UK
- Worldwide in top 3 or 4.
- Largest in World that is Membership Owned.
- Years ago, saving money was more of a factor in switching to IXP as transit costs via ISP was more expensive
- Transit pricing has been a 'race to the bottom' over the last 20 years or so for ISPs.
- Probably not a huge difference in price nowadays
- IXP main advantage is in control over connectivity:
- ISPs still rely on upstream connectivity. Issue in ISP network or unusual paths result in the 3rd party (ISP) have sole control over your problem.
- Pricing on IXP is pay for package, no matter how little you use - then, you pay a surcharge for 'burst' traffic up to port speed (100Gbps) - you should pay for more than you use (50%-70%) to allow for traffic peaks. But you still pay for that bandwidth.
- Mbps costs we found are fairly accurate.
- 4.5c per Mbps is cheapest Mike @ Linx has seen.
- IXP Pricing sheet(https://docs.google.com/spreadsheets/d/18ztPX_ysWYqEhJlf2SKQQsTNRbkwoxPSfaC6ScEZAG8/edit?gid=0#gid=0)
- LON1 and LON2 difference is just resiliency.

## Onboarding

- Become a member - application form on website
- Order port at any site.
- IXP don't deal with connectivity - Customers do. They're available in most London DCs. SolentCloud will Need some equipment in London or Slough.
- Establish peering to all networks we can available in exchange.
- You can use a 'routeserver' (operated by IXP - any member can establish BGP with that server, and these routes will be advertised to other BGP peers with the server ~40% use this)
- EVPN(https://www.juniper.net/documentation/us/en/software/junos/evpn/topics/concept/evpns-overview.html)

## IXP internal layout

- Simple Layer two
-STP not used really
- 1x MAC address allowed from connected device.
- Use Juniper & Nokia
- Use EVPN (most cases) or MPLS
- ISP grade hardware
- Called a fabric as they offer other services (such as private VLAN anywhere in the IXP net)
 
## Rogue BGP Routes

- Linx is hands off unless other company doesn't respond to issues/requests. This is membership requirement.

## SLA

- Traditionally no SLAs with IXPs.
- Should always have a 2nd path to destination.
- Just relies on membership custom as a drive to be reliable and deliver.
- You can buy an SLA service (added fees). If LINX goes down, guarantees availability of the LINX fabric. Doesn't change the service. For companies who must have an SLA.
- LINX monitors their network internally. Make measurements available to members.
- Internal goals are 99.999% uptime.

## Two Sites

- Two networks with two different equipment vendors/versions
- Companies peer with both if they want additional availability to companies connected to both.
- LON2 is cheaper as you can reach fewer networks from that exchange. Same with Manchester.

