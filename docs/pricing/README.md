# SolentCloud Pricing Analysis

This project calculates and graphs the cost difference between two different internet edge architectures for SolentCloud:

1.  **2x ISP & 2x IXP**: Connecting via two Internet Service Providers and two Internet Exchange Points (LINX LON & MAN).
2.  **4x ISP Only**: Connecting purely via four Internet Service Providers.

The tool generates a graph comparing monthly costs as the "Cost per Mbps" for ISP transit increases.

## Setup

1.  Navigate to the `pricing` directory:
    ```bash
    cd pricing
    ```
2.  Ensure you have Python 3 installed.
3.  Install the required dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

Run the module from the `pricing` directory:

```bash
python3 -m run
```

## Expected Output

1.  The script will calculate costs for both scenarios over a range of ISP bandwidth prices (starting at £0.01/Mbps).
2.  It will generate a line graph showing:
    *   **X-Axis**: Cost per Mbps charged by ISPs.
    *   **Y-Axis**: Total Monthly Cost for SolentCloud.
    *   **Crossover Point**: The ISP price point where one solution becomes cheaper than the other.
    *   **Max Saving**: The widest cost gap at the starting price point.
3.  The graph is saved to: `graphs/`

## Formulas

The total monthly cost is calculated as follows:

$$
\text{Total Cost} = \text{IXP Membership} + \text{IXP Port Fees} + \text{IXP Bandwidth} + \text{ISP Transit Costs}
$$

Where:
*   **IXP Membership**: Fixed monthly fee.
*   **IXP Port Fees**: (Number of Ports $\times$ Port Fee).
*   **IXP Bandwidth**: (London Bandwidth Fee + Manchester Bandwidth Fee).
*   **ISP Transit Costs**: (Gbps required $\times$ 1000 $\times$ Price per Mbps $\times$ Number of ISPs).