import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from .config import *
from decimal import Decimal

def calculate(
    ixp_mem_fee=IXP_MEM_FEE,
    ixp_port_fee=IXP_PORT_FEE,
    ixp_lon_port_mult=IXP_LON_PORT_MULTIPLIER,
    ixp_man_port_mult=IXP_MAN_PORT_MULTIPLIER,
    ixp_bandwidth_fee_lon=IXP_BANDWIDTH_FEE_LON,
    ixp_lon_30gbps_mult=IXP_LON_30GBPS_MULTIPLIER,
    ixp_bandwidth_fee_man=IXP_BANDWIDTH_FEE_MAN,
    ixp_man_30gbps_mult=IXP_MAN_30GBPS_MULTIPLIER,
    gigabits_per_isp=GIGABITS_REQUIRED_PER_ISP,
    isp_cost_per_mbps=ISP_COST_PER_MBPS,
    isp_mult=ISP_MULTIPLIER,
):
    
    total_ixp_mem = ixp_mem_fee
    total_ports = ixp_lon_port_mult + ixp_man_port_mult
    total_ixp_port_costs = total_ports * ixp_port_fee
    
    ixp_bandwidth_lon = ixp_bandwidth_fee_lon * ixp_lon_30gbps_mult
    ixp_bandwidth_man = ixp_bandwidth_fee_man * ixp_man_30gbps_mult
    total_ixp_bandwidth = ixp_bandwidth_lon + ixp_bandwidth_man
    
    mbps_per_isp = gigabits_per_isp * 1000
    cost_per_single_isp_connection = mbps_per_isp * isp_cost_per_mbps
    total_isp_costs = cost_per_single_isp_connection * isp_mult
    
    total_monthly_cost = (
        total_ixp_mem +
        total_ixp_port_costs +
        total_ixp_bandwidth +
        total_isp_costs
    )
    
    return total_monthly_cost


def graph_difference(
    ixp_mem_fee=IXP_MEM_FEE,
    ixp_port_fee=IXP_PORT_FEE,
    ixp_bandwidth_fee_lon=IXP_BANDWIDTH_FEE_LON,
    ixp_bandwidth_fee_man=IXP_BANDWIDTH_FEE_MAN,
    isp_cost_per_mbps=ISP_COST_PER_MBPS
):

    # Calculate prices for 2x IXP and 2x ISP
    twoixp_twoisp_cost = {}
    for _ in range(11):
        twoixp_twoisp_cost[round(isp_cost_per_mbps, 2)] = round(calculate(isp_cost_per_mbps=isp_cost_per_mbps), 2)
        isp_cost_per_mbps = float(Decimal(str(isp_cost_per_mbps)) + Decimal('0.01'))

    # Calculate prices for 4x ISP 0x IXP
    fourisp_zeroixp_cost = {}
    ixp_mem_fee = 0
    ixp_port_fee = 0
    ixp_bandwidth_fee_lon = 0
    ixp_bandwidth_fee_man = 0

    # Reset the isp_cost_per_mbps to the original value for the second calculation
    isp_cost_per_mbps = ISP_COST_PER_MBPS

    for _ in range(11):
        fourisp_zeroixp_cost[round(isp_cost_per_mbps, 2)] = round(calculate(
            ixp_mem_fee=ixp_mem_fee,
            ixp_port_fee=ixp_port_fee,
            ixp_bandwidth_fee_lon=ixp_bandwidth_fee_lon,
            ixp_bandwidth_fee_man=ixp_bandwidth_fee_man,
            isp_cost_per_mbps=isp_cost_per_mbps,
            isp_mult=4
        ), 2)
        isp_cost_per_mbps = float(Decimal(str(isp_cost_per_mbps)) + Decimal('0.01'))

    # Line graph for comparison by cost per Mbps for ISPs

    # Configure font
    plt.rcParams["font.family"] = GRAPH_FONT

    plt.figure(figsize=(10, 6))
    
    plt.plot(
        list(twoixp_twoisp_cost.keys()), 
        list(twoixp_twoisp_cost.values()), 
        label=TWO_IXP_TWO_ISP_LABEL, 
        color=TWO_IXP_COLOR_HEX,
        marker='o'
    )
    plt.plot(
        list(fourisp_zeroixp_cost.keys()), 
        list(fourisp_zeroixp_cost.values()), 
        label=FOUR_ISP_ZERO_IXP_LABEL, 
        color=FOUR_ISP_COLOR_HEX,
        marker='o'
    )
    
    plt.xlabel(GRAPH_X_LABEL)
    plt.ylabel(GRAPH_Y_LABEL)
    plt.title(GRAPH_TITLE)
    plt.legend()
    plt.grid()
    
    # Format axes with £
    formatter = FuncFormatter(lambda x, pos: f"£{x:.2f}")
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.gca().yaxis.set_major_formatter(formatter)
    
    # Ensure directory exists
    output_dir = "graphs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save to file
    filename = f"{output_dir}/{GRAPH_TITLE}.png"
    plt.savefig(filename, dpi=300)
    print(f"Graph saved to {filename}")


def main():
    graph_difference()

if __name__ == "__main__":
    main()