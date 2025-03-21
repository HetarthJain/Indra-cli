import os
import requests
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()

def handle(args):
    base_url = os.getenv("MGMT_SERVER")

    if not base_url:
        print("Error: MGMT_SERVER URL not set in environment variables.")
        return

    endpoint = "/cli/vms/a" if args.all else "/cli/vms/all"
    url = f"{base_url}{endpoint}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

        data = response.json()
        
        if not data:
            print("No VMs found.")
            return
        # Extract relevant fields
        table_data = []
        
        active_vms = data.get("active_vms",[])
        if not active_vms:
            print("No active VMs found.")
            return
        table_data = [
            [
                vm.get("vm_id", "N/A"),
                vm.get("vm_name", "N/A"),
                vm.get("provider_name", "N/A"),
                vm.get("wireguard_ip", "N/A"),
                "✅ Connected" if vm.get("wireguard_status") else "❌ Disconnected"
            ]
            for vm in active_vms
        ]
        
        # Define headers
        headers = ["VM ID", "VM Name", "Provider", "WireGuard IP", "WireGuard Status"]
        
        # Print table
        print(tabulate(table_data, headers=headers))

    except requests.exceptions.RequestException as e:
        print(f"Error fetching VMs: {e}")