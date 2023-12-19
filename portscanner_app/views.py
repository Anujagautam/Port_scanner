
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import asyncio
import socket
import time


def home_view(request):
    return HttpResponse("Welcome to the Port Scanner app!")


def home_view(request):
    return render(request, 'scan_page.html')


async def scan_port(ip, port):
    writer = None
    try:
        reader, writer = await asyncio.open_connection(ip, port)
        print(f"IP {ip} is UP on port {port}")
        return port
    except (socket.timeout, socket.error):
        return None
    finally:
        if writer is not None:
            writer.close()
            await writer.wait_closed()


async def scan_ip(ip, start_port=1, end_port=1024):
    open_ports = await asyncio.gather(*(scan_port(ip, port) for port in range(start_port, end_port + 1)))
    open_ports = {port for port in open_ports if port is not None}
    return ip, open_ports


async def scan_network(start_ip, end_ip):
    ip_addresses = [
        f"{a}.{b}.{c}.{d}"
        for a in range(int(start_ip[0]), int(end_ip[0]) + 1)
        for b in range(int(start_ip[1]), int(end_ip[1]) + 1)
        for c in range(int(start_ip[2]), int(end_ip[2]) + 1)
        for d in range(int(start_ip[3]), int(end_ip[3]) + 1)
    ]

    reachable_ips = []
    tasks = [scan_ip(ip) for ip in ip_addresses]

    results = await asyncio.gather(*tasks)

    for ip, open_ports in results:
        if open_ports is not None:
            if open_ports:
                reachable_ips.append((ip, open_ports))

    reachable_ips.sort(key=lambda x2: int(
        ''.join(f'{int(i):03d}' for i in x2[0].split('.'))))

    output_filename = "scan_ips.txt"
    with open(output_filename, "w") as f_results:
        for ip, open_ports in reachable_ips:
            ports_message = ', '.join(str(port) for port in open_ports)
            f_results.write(
                f"IP {ip} is UP with open ports: {ports_message}\n")
            print(f"IP {ip} is UP with open ports: {ports_message}")

    return reachable_ips


async def scan_view(request):
    start_ip = "192.168.2.0"
    end_ip = "192.168.2.100"

    start_time = time.time()

    console_output = []
    reachable_ips = await scan_network(start_ip.split('.'), end_ip.split('.'))

    if reachable_ips is not None:
        for ip, open_ports in reachable_ips:
            ports_message = ', '.join(str(port) for port in open_ports)
            console_output.append(
                f"IP {ip} is UP with open ports: {ports_message}")

    execution_time_minutes = ((time.time() - start_time) / 60)
    output_message = f"Execution time: {execution_time_minutes:.2f} minutes"

    response_data = {
        'output': '\n''<br>'.join(console_output + [output_message]),
    }

    return JsonResponse(response_data)

    return render(request, 'scan_result.html', context=response_data)
