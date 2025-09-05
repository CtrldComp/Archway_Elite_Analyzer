"""
Sample WiFi network data for demonstration purposes
"""

from datetime import datetime, timedelta
import random

def generate_sample_networks():
    """Generate realistic sample WiFi network data"""
    
    # Common SSID patterns
    ssids = [
        "HomeNetwork_5G", "NETGEAR_2.4G", "Linksys_Guest", "TP-Link_AC1750",
        "ATT_WiFi_5G", "Verizon_Home", "Xfinity_2.4G", "Spectrum_5G",
        "ASUS_AX6000", "Nighthawk_Pro", "Office_WiFi", "Conference_Room",
        "Guest_Network", "IoT_Devices", "Smart_Home", "Gaming_Network",
        "Free_WiFi", "Public_Access", "Starbucks_WiFi", "Hotel_Guest"
    ]
    
    # Vendor OUI mappings
    vendors = {
        "Apple": ["00:1B:63", "00:23:DF", "00:25:00"],
        "Cisco": ["00:0A:41", "00:0B:46", "00:0C:85"],
        "Netgear": ["00:09:5B", "00:0F:B5", "00:14:6C"],
        "Linksys": ["00:06:25", "00:0C:41", "00:12:17"],
        "TP-Link": ["00:27:19", "14:CC:20", "50:C7:BF"],
        "ASUS": ["00:1F:C6", "00:22:15", "00:26:18"],
        "D-Link": ["00:05:5D", "00:0F:3D", "00:15:E9"],
        "Ubiquiti": ["00:15:6D", "04:18:D6", "24:A4:3C"],
        "Aruba": ["00:0B:86", "00:1A:1E", "00:24:6C"],
        "Ruckus": ["00:24:A8", "2C:5A:0F", "58:93:96"]
    }
    
    # Encryption types with realistic distribution
    encryption_types = ["WPA3", "WPA2", "WPA", "WEP", "Open"]
    encryption_weights = [0.15, 0.65, 0.10, 0.05, 0.05]  # WPA2 most common
    
    # Channel distribution (2.4GHz and 5GHz)
    channels_24ghz = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    channels_5ghz = [36, 40, 44, 48, 149, 153, 157, 161, 165]
    
    networks = []
    base_time = datetime.now()
    
    for i in range(50):  # Generate 50 sample networks
        # Select vendor and generate MAC
        vendor_name = random.choice(list(vendors.keys()))
        oui = random.choice(vendors[vendor_name])
        mac_suffix = ":".join([f"{random.randint(0, 255):02X}" for _ in range(3)])
        bssid = f"{oui}:{mac_suffix}"
        
        # Select SSID (some hidden)
        ssid = random.choice(ssids) if random.random() > 0.1 else None
        
        # Select channel and frequency
        if random.random() > 0.3:  # 70% 5GHz, 30% 2.4GHz
            channel = random.choice(channels_5ghz)
            frequency = 5000 + (channel * 5)
        else:
            channel = random.choice(channels_24ghz)
            frequency = 2412 + ((channel - 1) * 5)
        
        # Generate signal strength (closer networks stronger)
        distance_factor = random.uniform(0.1, 1.0)
        base_signal = -30 if distance_factor < 0.2 else -50 if distance_factor < 0.5 else -70
        signal_strength = base_signal + random.randint(-15, 5)
        
        # Select encryption
        encryption = random.choices(encryption_types, weights=encryption_weights)[0]
        
        # Generate timestamps
        first_seen = base_time - timedelta(hours=random.randint(1, 72))
        last_seen = base_time - timedelta(minutes=random.randint(0, 30))
        
        # Calculate quality based on signal strength
        quality = max(0, min(100, 100 + signal_strength + 30))
        
        # Generate client count
        client_count = random.randint(0, 15) if encryption != "Open" else random.randint(0, 25)
        
        network = {
            "id": i + 1,
            "ssid": ssid,
            "bssid": bssid,
            "signal_strength": signal_strength,
            "channel": channel,
            "frequency": frequency,
            "encryption": encryption,
            "cipher": "CCMP" if encryption in ["WPA2", "WPA3"] else "TKIP" if encryption == "WPA" else "WEP" if encryption == "WEP" else "None",
            "authentication": "PSK" if encryption in ["WPA", "WPA2", "WPA3"] else "Open",
            "vendor": vendor_name,
            "mode": "Infrastructure",
            "quality": quality,
            "client_count": client_count,
            "first_seen": first_seen.isoformat(),
            "last_seen": last_seen.isoformat(),
            "beacon_interval": random.choice([100, 102, 104]),
            "capabilities": ["ESS"] + (["Privacy"] if encryption != "Open" else []),
            "country_code": "US",
            "max_rate": random.choice([54, 150, 300, 600, 1200, 2400]) # Mbps
        }
        
        networks.append(network)
    
    return networks

def generate_sample_clients():
    """Generate sample client data"""
    
    device_types = {
        "Smartphone": ["Apple", "Samsung", "Google", "OnePlus", "Xiaomi"],
        "Laptop": ["Dell", "HP", "Lenovo", "Apple", "ASUS"],
        "Tablet": ["Apple", "Samsung", "Microsoft", "Amazon"],
        "IoT": ["Ring", "Nest", "Philips", "Amazon", "Sonos"],
        "Gaming": ["Sony", "Microsoft", "Nintendo", "Valve"],
        "Smart TV": ["Samsung", "LG", "Sony", "TCL", "Roku"]
    }
    
    clients = []
    base_time = datetime.now()
    
    for i in range(30):  # Generate 30 sample clients
        device_type = random.choice(list(device_types.keys()))
        manufacturer = random.choice(device_types[device_type])
        
        # Generate MAC address
        oui_map = {
            "Apple": "00:1B:63",
            "Samsung": "00:12:FB", 
            "Google": "00:1A:11",
            "Dell": "00:14:22",
            "HP": "00:1F:29"
        }
        
        oui = oui_map.get(manufacturer, "00:50:56")  # Default OUI
        mac_suffix = ":".join([f"{random.randint(0, 255):02X}" for _ in range(3)])
        mac_address = f"{oui}:{mac_suffix}"
        
        # Generate signal strength
        signal_strength = random.randint(-80, -30)
        
        # Generate timestamps
        first_seen = base_time - timedelta(hours=random.randint(1, 24))
        last_seen = base_time - timedelta(minutes=random.randint(0, 10))
        
        # Associated network (random from 1-50)
        network_id = random.randint(1, 50)
        
        client = {
            "id": i + 1,
            "mac_address": mac_address,
            "vendor": manufacturer,
            "device_type": device_type,
            "signal_strength": signal_strength,
            "network_id": network_id,
            "first_seen": first_seen.isoformat(),
            "last_seen": last_seen.isoformat(),
            "data_transferred": random.randint(1024, 1024*1024*100),  # Bytes
            "packets_sent": random.randint(100, 10000),
            "packets_received": random.randint(150, 15000),
            "connection_duration": random.randint(300, 86400),  # Seconds
            "capabilities": ["WPA2"] if random.random() > 0.1 else ["Open"]
        }
        
        clients.append(client)
    
    return clients

