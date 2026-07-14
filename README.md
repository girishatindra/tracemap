# TraceMap - Follow The Hops.

<div align="center">
  
  <img width="60%" alt="logo" src="./docs/logo.png" />


</div>

<div align="center">
  
[![BACKEND](https://img.shields.io/badge/Backend-Flask-darkblue?style=for-the-badge&labelColor=orange)](https://flask.palletsprojects.com/en/stable/)
[![FRONTEND](https://img.shields.io/badge/Frontend-alpine.js-darkblue?style=for-the-badge&labelColor=orange)](https://alpinejs.dev/)
[![FRONTEND](https://img.shields.io/badge/Frontend-tailwindcss-darkblue?style=for-the-badge&labelColor=orange)]([https://tailwindcss.com/])
[![MAP](https://img.shields.io/badge/MAP-Leaflet.js-darkblue?style=for-the-badge&labelColor=orange)](https://leafletjs.com/)
[![API](https://img.shields.io/badge/API-ipquery-darkblue?style=for-the-badge&labelColor=orange)](https://ipquery.io/)

</div>

<hr>

<br>
<br>

<div align='center'>

 
<img width="755" height="530" alt="tracemap demo" src="./docs/tracemap-demo.gif" />


</div>

<br>
<br>

<div align="center">
  
***Every packet takes a journey. TraceMap shows you the path.***

</div>

TraceMap is a visual traceroute tool that maps the hop-by-hop journey of your packets across the internet. Enter any public IP address or domain and TraceMap traces the route, geolocates every public hop along the way, and plots the path live on an interactive satellite map, turning raw network data into a visual story of how your traffic moves across the globe.

<br>
<br>

<hr>

<br>

# About

<br>

***What Does TraceMap Do ?***

TraceMap sends ICMP probes with incrementing TTL values, collecting the IP address and round-trip time of every router that responds along the path to the destination. Every public hop is enriched with geolocation data — city, state, country, ISP — via the IPQuery API and plotted as a marker on an interactive satellite map. Hops are connected by a polyline showing the physical route your packets travel. Clicking any hop in the results table pans the map to that location and opens its details.
Private and internal hops are shown in the table for completeness but are not plotted on the map since they have no meaningful geolocation. Unresponsive hops are shown as timeouts with `*` RTT values, consistent with standard traceroute output.

<br>
<br>

***What Tech Stack Does TraceMap Use ?***

<br>

| Layer | Technology | Purpose
|-------|------------|--------|
| Packet Engine | Scapy | Sends ICMP Packets |
| Backend | Flask | Serves the frontend |
| Frontend | Alpine.js & Tailwindcss | Reactive UI state management | 
| Geolocation Map | Leaflet.js |Live IP geolocation plotting | 
| OSINT | IPQuery API | IP enrichment |

<br>
<br>

***What Makes TraceMap Different ?***

Most traceroute tools just mimic the traditional tracert command line utility. TraceMap visualizes the hops on an interactive satellite map, giving you a geographical understanding of how your packet travels across the internet. Turning a list of IPs into a visual story.
<br>
<br>

***How Do I Run TraceMap?***

TraceMap requires root or administrator privileges for crafting and sending packets.

```bash

# 1. Clone the repo
git clone https://github.com/girishatindra/tracemap.git
cd TraceMap

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
python app.py
```
Then open http://127.0.0.1:5000 in your browser, enter a valid domain or IP, and click Trace.

<br>
<br>

***Will TraceMap Expand ?***

Currently an MVP. Planned expansions include:

- UDP and TCP probe modes: beyond ICMP, matching real-world traceroute behaviour
- ASN path visualization: group hops by owning organization to see which networks handle your traffic
- Exportable route reports: save trace results as JSON or CSV for offline analysis
- API rate limiting: protect the `/trace` endpoint from rapid repeat requests
- IPQuery response caching: reduce redundant API calls for IPs seen across multiple traces
- Public deployment: host TraceMap as a web accessible tool, removing the need for local installation

<br>
<br>

***Why Is It Named TraceMap ?***

The name points directly at the core function, mapping the traceroute results on an interactive map.

<br>
<br>

***Why Did I Build This ?***

The idea came while playing around with tracert for an article I was working on. One thing struck me, what if I could visualize the hops on a map? That curiosity became TraceMap, a tool that takes traceroute results and plots them geographically on an interactive satellite map.

<br>
<hr>
<br>

## :telephone_receiver: Contact
Have questions, feedback, or suggestions? Feel free to reach out:
-  [![Gmail](https://img.shields.io/badge/gmail-girishatindra@gmail.com-white?style=social&logo=gmail)](mailto:girishatindra@gmail.com)
