        function tracemap(){
            return {
                hops: [],
                map: null,  
                ttl_marker: {},
                loading: false,
                tracing: false,
                traced: false,
                error: null,
                query: null,

                async run(){
                    this.error = null;
                    this.loading = true;
                    this.tracing = true;
                    this.traced = false;
                    const ip = this.query
                    try {
                        const response = await fetch(`/trace`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ip})
                        });
                        const res = await response.json();
                        if (!response.ok){
                            this.error = res.error
                            return;
                        }
                        this.hops = res;
                        this.traced = true;
                        this.$nextTick(() => this.renderMap(res));
                    } catch (error) {
                        this.error = "connection failed — check your network";
                    } finally {
                        this.loading = false;
                        this.tracing = false;
                    }
                },

                renderMap(data){  
                    var latlongs = [];
                    if (this.map){
                        this.map.remove();
                        this.map = null;
                    }
                    this.map = L.map('map').setView([20, 0], 2);
                    this.ttl_marker = {};
                    const mapLink = '<a href="http://www.esri.com/">Esri</a>';
                    const wholink = 'i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community';
                    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                            attribution: '&copy; '+mapLink+', '+wholink,
                            maxZoom: 19,
                    }).addTo(this.map);    
                    data.forEach(hop => {
                            if (hop.latitude && hop.longitude) {
                                latlongs.push([hop.latitude, hop.longitude]);
                                const marker = L.marker([hop.latitude, hop.longitude]).addTo(this.map)
                                .bindPopup(`TTL: ${hop.ttl}<br>IP: ${hop.ip}<br>City: ${hop.city}<br>State: ${hop.state}<br>Country: ${hop.country}<br>ISP: ${hop.isp}`)
                                this.ttl_marker[hop.ttl] = marker; 
                            }
                    });
                    if (latlongs.length > 1) {
                        const polyline = L.polyline(latlongs, { color: 'red', dashArray: [4, 1, 2] }).addTo(this.map);
                        this.map.fitBounds(polyline.getBounds());
                    } 
                    else if (latlongs.length === 1) {
                        this.map.setView(latlongs[0], 6);
                    }  
                      setTimeout(() => {
                            this.map.invalidateSize();
                        }, 100);                     
                },
                
                focusHop(hop){
                    const marker = this.ttl_marker[hop]
                    if(marker){
                        this.map.setView(marker.getLatLng(), 6);
                        marker.openPopup();
                }
             }
        }
    }