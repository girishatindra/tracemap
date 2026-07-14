from scapy.all import sr
from scapy.layers.inet import IP, ICMP
from collections import defaultdict
import ipaddress
import requests
from flask import Flask, jsonify, render_template, request
import re
import socket

DOMAIN_REGEX = re.compile(r'^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$')
MAX_HOPS = 15
MAX_PROBES = 3

def is_valid_destination(d):
    if not d:
        return False
    
    # Check for valid Public IP

    try:
        addr = ipaddress.ip_address(d)
        return addr.is_global
    except ValueError:
        pass

    # Validate domain format
    if  not DOMAIN_REGEX.match(d):
        return False
    
    # DNS resolution check
    try:
        socket.gethostbyname(d)
    except socket.gaierror:
        return False
    else:
        return True

def tracemap(q):
    hops = defaultdict(list)
    packet_id = 1

    # resolve destination IP once for comparison 

    try:
        dest_ip = socket.gethostbyname(q)
    except socket.gaierror:
        dest_ip = q
    
    for ttl in range(1,MAX_HOPS):
        packets = []
        for _ in range(MAX_PROBES):
            # unique packet_id per probe to correctly match replies   
            packets.append(IP(dst=f"{q}", ttl=ttl, id=packet_id)/ICMP())
            packet_id += 1
        ans, uans = sr(packets, timeout=2, verbose=False)
    
    
        for sent, reply in ans:
            hop_ttl = sent.ttl
            rtt = round((reply.time - sent.sent_time) * 1000, 2)
            hops[hop_ttl].append(({"ip": reply.src, "rtt":  rtt}))

        for sent in uans:
            hop_ttl = sent.ttl
            hops[hop_ttl].append({"ip": "timeout", "rtt": "*"})
        
        replied_ips = [reply.src for _, reply in ans]
        if dest_ip in replied_ips:
            break


    result = []
    for ttl in range(1, MAX_HOPS):
        if ttl not in hops:
            break
        probes = hops.get(ttl, [])
        ip = next((p['ip'] for p in probes if p['ip'] != "timeout"), None)
        rtt = [p['rtt'] for p in probes]
        rtt += ["*"] * max(0,MAX_PROBES - len(rtt))
        
        if not probes or ip is None:
            result.append({"ttl": ttl, "ip": "timeout", "rtts": ["*", "*", "*"], "latitude": None, "longitude": None, "city": None, "state": None, "country": None, "isp": None, "kind": "unknown"})
        elif ip != "timeout" and ipaddress.ip_address(ip).is_global:
            geo_data = geolocate(ip)
            if geo_data is None:
                result.append({"ttl": ttl, "ip": ip, "rtts": rtt, "latitude": None, "longitude": None, "city": None, "state": None, "country": None, "isp": None, "kind": "public"})
            else:
                lat = geo_data["location"]["latitude"]
                lon = geo_data["location"]["longitude"]
                city = geo_data["location"]["city"]
                state = geo_data["location"]["state"]
                country = geo_data["location"]["country"]
                isp = geo_data["isp"]["isp"]
                result.append({"ttl": ttl, "ip": ip, "rtts": rtt, "latitude": lat, "longitude": lon, "city": city, "state": state, "country": country, "isp": isp, "kind": "public"})
        else: 
            result.append({"ttl": ttl, "ip": ip, "rtts": rtt, "latitude": None, "longitude": None, "city": None, "state": None, "country": None, "isp": None, "kind": "private"})
    return result

      
            
def geolocate(ip):
    try:
        geo = requests.get(f"https://api.ipquery.io/{ip}", timeout=5)
        geo.raise_for_status()
        return geo.json()
    except Exception as e:
        return None


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/trace', methods=['POST'])
def trace_ip():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid destination — must be a public IP or valid domain"}), 400
    ip = data.get('ip')
    if ip is None:
        return jsonify({"error": "Invalid destination — must be a public IP or valid domain"}), 400
    if is_valid_destination(ip):
        try:
            result = tracemap(ip)
        except Exception as e:
            return jsonify({"error": "An Error Occured"}), 500
        return jsonify(result)
    return jsonify({"error": "Invalid destination — must be a public IP or valid domain"}), 400

    

if __name__ == '__main__':
    app.run(debug=False)