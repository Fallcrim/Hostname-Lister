import asyncio
import socket
import subprocess
import platform
import logging

from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp


logging.basicConfig(level=logging.INFO, filename="scan_hostnames.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")


def arp_scan(ip_range: str) -> list:
    """
    Scan the network for devices using ARP requests.
    :param ip_range:
    :return:
    """
    # Send an ARP request to the broadcast address
    logging.info(f"Scanning network for range {ip_range}...")
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)
    # Send the request and store the response
    arp_response = srp(arp_request, timeout=2, verbose=False)[0]
    # Extract the MAC and IP addresses from the response
    devices = []
    for s, r in arp_response:
        device = {"ip": r.psrc, "mac": r.hwsrc}
        devices.append(device)
    return devices


async def get_hostname(ip: str) -> str:
    """
    Resolve the hostname of an IP address.
    :param ip:
    :return:
    """
    # Use the gethostbyaddr() function to resolve the hostname
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        logging.warning(f"Hostname not found for {ip}")
        hostname = None
    return hostname


async def resolve_hostnames(devices: list) -> list:
    # Create a list of tasks to resolve the hostnames
    results = []
    logging.info("Resolving hostnames...")
    for device in devices:
        results.append(await get_hostname(device["ip"]))
    # Add the hostnames to the devices
    for i in range(len(devices)):
        devices[i]["hostname"] = results[i]
    return devices


def get_default_gateway_windows():
    # Get the default gateway using the "wmic" command
    output = subprocess.check_output(["wmic", "nicconfig", "where", "IPEnabled=true", "get", "DefaultIPGateway"])

    # Parse the output to get the default gateway
    lines = output.splitlines()
    for line in lines:
        if b"." in line:
            default_gateway = line.decode("utf-8").replace('"', "").replace('{', "").replace('}', "").strip()
            break
    else:
        default_gateway = None
    return default_gateway


def get_default_gateway_linux():
    # Get the default gateway using the "ip" command
    output = subprocess.check_output(["ip", "route", "show", "default"])

    # Parse the output to get the default gateway
    default_gateway = output.split()[3].decode("utf-8")

    return default_gateway


def runner(window):
    while window.isVisible():
        if platform.system() == "Windows":
            logging.info("OS type: Windows")
            gateway = get_default_gateway_windows()
        else:
            logging.info("OS type: Linux/Unix")
            gateway = get_default_gateway_linux()
        logging.info(f"Default gateway found as `{gateway}`")
        devices = arp_scan(f"{gateway}/24")
        asyncio.run(resolve_hostnames(devices))
        devices = list(sorted(devices, key=lambda x: int(x["ip"].split(".")[-1]), reverse=False))
        window.hostnameList.clear()
        for device in devices:
            try:
                window.hostnameList.addItem(f'{device["ip"]} - {device["mac"]} - {device["hostname"]}')
            except AttributeError:
                window.hostnameList.addItem(f'{device["ip"]} - {device["mac"]} - Unknown')
