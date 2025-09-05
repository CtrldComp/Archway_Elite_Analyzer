"""
Core WiFi Scanner Module for Archway WiFi Analyzer
Inspired by Sparrow-WiFi, AtEar, and other elite WiFi analysis tools
"""

import subprocess
import re
import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import netifaces
import psutil
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11ProbeReq, Dot11ProbeResp, Dot11Auth, Dot11Deauth
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WiFiInterface:
    """Manages WiFi interface operations"""
    
    def __init__(self, interface: str):
        self.interface = interface
        self.original_mode = None
        self.monitor_mode = False
        
    def get_available_interfaces(self) -> List[str]:
        """Get list of available wireless interfaces"""
        interfaces = []
        try:
            # Get all network interfaces
            all_interfaces = netifaces.interfaces()
            
            for iface in all_interfaces:
                # Check if it's a wireless interface
                if self.is_wireless_interface(iface):
                    interfaces.append(iface)
                    
        except Exception as e:
            logger.error(f"Error getting interfaces: {e}")
            
        return interfaces
    
    def is_wireless_interface(self, interface: str) -> bool:
        """Check if interface is wireless"""
        try:
            # Check if wireless extensions are available
            result = subprocess.run(['iwconfig', interface], 
                                  capture_output=True, text=True, timeout=5)
            return 'IEEE 802.11' in result.stdout or 'ESSID' in result.stdout
        except:
            return False
    
    def get_interface_info(self) -> Dict:
        """Get detailed interface information"""
        info = {
            'interface': self.interface,
            'exists': False,
            'wireless': False,
            'monitor_capable': False,
            'current_mode': 'unknown',
            'mac_address': None,
            'driver': None,
            'chipset': None
        }
        
        try:
            # Check if interface exists
            if self.interface in netifaces.interfaces():
                info['exists'] = True
                
                # Get MAC address
                addrs = netifaces.ifaddresses(self.interface)
                if netifaces.AF_LINK in addrs:
                    info['mac_address'] = addrs[netifaces.AF_LINK][0]['addr']
                
                # Check if wireless
                if self.is_wireless_interface(self.interface):
                    info['wireless'] = True
                    
                    # Get current mode
                    result = subprocess.run(['iwconfig', self.interface], 
                                          capture_output=True, text=True, timeout=5)
                    if 'Mode:Monitor' in result.stdout:
                        info['current_mode'] = 'monitor'
                        self.monitor_mode = True
                    elif 'Mode:Managed' in result.stdout:
                        info['current_mode'] = 'managed'
                    
                    # Check monitor capability
                    result = subprocess.run(['iw', self.interface, 'info'], 
                                          capture_output=True, text=True, timeout=5)
                    if 'monitor' in result.stdout.lower():
                        info['monitor_capable'] = True
                        
        except Exception as e:
            logger.error(f"Error getting interface info: {e}")
            
        return info
    
    def enable_monitor_mode(self) -> bool:
        """Enable monitor mode on the interface"""
        try:
            if self.monitor_mode:
                logger.info(f"Interface {self.interface} already in monitor mode")
                return True
                
            logger.info(f"Enabling monitor mode on {self.interface}")
            
            # Store original mode
            info = self.get_interface_info()
            self.original_mode = info.get('current_mode', 'managed')
            
            # Bring interface down
            subprocess.run(['sudo', 'ip', 'link', 'set', self.interface, 'down'], 
                         check=True, timeout=10)
            
            # Set monitor mode
            subprocess.run(['sudo', 'iw', self.interface, 'set', 'type', 'monitor'], 
                         check=True, timeout=10)
            
            # Bring interface up
            subprocess.run(['sudo', 'ip', 'link', 'set', self.interface, 'up'], 
                         check=True, timeout=10)
            
            # Verify monitor mode
            time.sleep(2)
            info = self.get_interface_info()
            if info['current_mode'] == 'monitor':
                self.monitor_mode = True
                logger.info(f"Monitor mode enabled on {self.interface}")
                return True
            else:
                logger.error(f"Failed to enable monitor mode on {self.interface}")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Error enabling monitor mode: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error enabling monitor mode: {e}")
            return False
    
    def disable_monitor_mode(self) -> bool:
        """Disable monitor mode and restore original mode"""
        try:
            if not self.monitor_mode:
                logger.info(f"Interface {self.interface} not in monitor mode")
                return True
                
            logger.info(f"Disabling monitor mode on {self.interface}")
            
            # Bring interface down
            subprocess.run(['sudo', 'ip', 'link', 'set', self.interface, 'down'], 
                         check=True, timeout=10)
            
            # Set managed mode (or original mode)
            target_mode = self.original_mode if self.original_mode else 'managed'
            subprocess.run(['sudo', 'iw', self.interface, 'set', 'type', target_mode], 
                         check=True, timeout=10)
            
            # Bring interface up
            subprocess.run(['sudo', 'ip', 'link', 'set', self.interface, 'up'], 
                         check=True, timeout=10)
            
            self.monitor_mode = False
            logger.info(f"Monitor mode disabled on {self.interface}")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error disabling monitor mode: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error disabling monitor mode: {e}")
            return False

class WiFiScanner:
    """Main WiFi scanner class with elite features"""
    
    def __init__(self, interface: str):
        self.interface = interface
        self.wifi_interface = WiFiInterface(interface)
        self.scanning = False
        self.scan_thread = None
        self.networks = {}
        self.clients = {}
        self.packets_captured = 0
        self.scan_start_time = None
        self.channels_2_4ghz = list(range(1, 15))  # Channels 1-14
        self.channels_5ghz = [36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 149, 153, 157, 161, 165]
        self.current_channel = 1
        self.channel_hop_interval = 0.5  # seconds
        self.vendor_db = self.load_vendor_database()
        
    def load_vendor_database(self) -> Dict[str, str]:
        """Load MAC address vendor database"""
        # This would typically load from a file like manuf.txt
        # For now, return a basic database
        return {
            '00:11:22': 'Cisco Systems',
            '00:1B:63': 'Apple Inc.',
            '00:26:BB': 'Apple Inc.',
            '28:CF:E9': 'Apple Inc.',
            '00:50:56': 'VMware Inc.',
            '08:00:27': 'Oracle VirtualBox',
            '00:0C:29': 'VMware Inc.',
            '00:1C:42': 'Parallels Inc.',
        }
    
    def get_vendor(self, mac_address: str) -> str:
        """Get vendor from MAC address"""
        if not mac_address or len(mac_address) < 8:
            return 'Unknown'
            
        oui = mac_address[:8].upper()
        return self.vendor_db.get(oui, 'Unknown')
    
    def parse_iwlist_scan(self) -> List[Dict]:
        """Parse iwlist scan output for basic WiFi scanning"""
        networks = []
        
        try:
            # Run iwlist scan
            result = subprocess.run(['sudo', 'iwlist', self.interface, 'scan'], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                logger.error(f"iwlist scan failed: {result.stderr}")
                return networks
            
            # Parse the output
            current_network = {}
            
            for line in result.stdout.split('\n'):
                line = line.strip()
                
                if 'Cell' in line and 'Address:' in line:
                    # Save previous network
                    if current_network:
                        networks.append(current_network)
                    
                    # Start new network
                    bssid_match = re.search(r'Address: ([0-9A-Fa-f:]{17})', line)
                    current_network = {
                        'bssid': bssid_match.group(1) if bssid_match else 'Unknown',
                        'ssid': '',
                        'channel': 0,
                        'frequency': 0.0,
                        'signal_strength': -100,
                        'quality': 0,
                        'encryption': 'Open',
                        'mode': 'Master',
                        'vendor': 'Unknown'
                    }
                
                elif 'ESSID:' in line:
                    ssid_match = re.search(r'ESSID:"([^"]*)"', line)
                    if ssid_match:
                        current_network['ssid'] = ssid_match.group(1)
                
                elif 'Channel:' in line:
                    channel_match = re.search(r'Channel:(\d+)', line)
                    if channel_match:
                        current_network['channel'] = int(channel_match.group(1))
                
                elif 'Frequency:' in line:
                    freq_match = re.search(r'Frequency:([0-9.]+)', line)
                    if freq_match:
                        current_network['frequency'] = float(freq_match.group(1)) * 1000  # Convert to MHz
                
                elif 'Signal level=' in line:
                    signal_match = re.search(r'Signal level=(-?\d+)', line)
                    if signal_match:
                        current_network['signal_strength'] = int(signal_match.group(1))
                
                elif 'Quality=' in line:
                    quality_match = re.search(r'Quality=(\d+)/(\d+)', line)
                    if quality_match:
                        quality = int(quality_match.group(1))
                        max_quality = int(quality_match.group(2))
                        current_network['quality'] = int((quality / max_quality) * 100)
                
                elif 'Encryption key:' in line:
                    if 'on' in line:
                        current_network['encryption'] = 'WEP'
                    else:
                        current_network['encryption'] = 'Open'
                
                elif 'IE: IEEE 802.11i/WPA2' in line:
                    current_network['encryption'] = 'WPA2'
                
                elif 'IE: WPA Version' in line:
                    current_network['encryption'] = 'WPA'
            
            # Add last network
            if current_network:
                networks.append(current_network)
            
            # Add vendor information
            for network in networks:
                network['vendor'] = self.get_vendor(network['bssid'])
            
        except subprocess.TimeoutExpired:
            logger.error("iwlist scan timed out")
        except Exception as e:
            logger.error(f"Error parsing iwlist scan: {e}")
        
        return networks
    
    def packet_handler(self, packet):
        """Handle captured packets for advanced analysis"""
        try:
            self.packets_captured += 1
            
            if packet.haslayer(Dot11):
                self.process_dot11_packet(packet)
                
        except Exception as e:
            logger.error(f"Error processing packet: {e}")
    
    def process_dot11_packet(self, packet):
        """Process 802.11 packets for detailed analysis"""
        try:
            dot11 = packet[Dot11]
            
            # Extract basic information
            timestamp = datetime.now()
            
            # Process beacon frames (Access Points)
            if packet.haslayer(Dot11Beacon):
                self.process_beacon_frame(packet, timestamp)
            
            # Process probe requests (Clients)
            elif packet.haslayer(Dot11ProbeReq):
                self.process_probe_request(packet, timestamp)
            
            # Process probe responses
            elif packet.haslayer(Dot11ProbeResp):
                self.process_probe_response(packet, timestamp)
            
            # Process authentication frames
            elif packet.haslayer(Dot11Auth):
                self.process_auth_frame(packet, timestamp)
            
            # Process deauthentication frames
            elif packet.haslayer(Dot11Deauth):
                self.process_deauth_frame(packet, timestamp)
                
        except Exception as e:
            logger.error(f"Error processing 802.11 packet: {e}")
    
    def process_beacon_frame(self, packet, timestamp):
        """Process beacon frames to identify access points"""
        try:
            dot11 = packet[Dot11]
            beacon = packet[Dot11Beacon]
            
            bssid = dot11.addr3
            if not bssid:
                return
            
            # Extract SSID
            ssid = ''
            if packet.info:
                ssid = packet.info.decode('utf-8', errors='ignore')
            
            # Get signal strength
            signal_strength = -100
            if hasattr(packet, 'dBm_AntSignal'):
                signal_strength = packet.dBm_AntSignal
            
            # Get channel from frequency
            channel = 0
            if hasattr(packet, 'Channel'):
                channel = packet.Channel
            
            # Update or create network entry
            if bssid not in self.networks:
                self.networks[bssid] = {
                    'bssid': bssid,
                    'ssid': ssid,
                    'channel': channel,
                    'signal_strength': signal_strength,
                    'encryption': 'Open',
                    'vendor': self.get_vendor(bssid),
                    'first_seen': timestamp,
                    'last_seen': timestamp,
                    'beacon_count': 1,
                    'clients': set()
                }
            else:
                # Update existing network
                network = self.networks[bssid]
                network['last_seen'] = timestamp
                network['beacon_count'] += 1
                network['signal_strength'] = signal_strength
                if ssid and not network['ssid']:
                    network['ssid'] = ssid
                    
        except Exception as e:
            logger.error(f"Error processing beacon frame: {e}")
    
    def process_probe_request(self, packet, timestamp):
        """Process probe requests to identify clients"""
        try:
            dot11 = packet[Dot11]
            
            client_mac = dot11.addr2
            if not client_mac:
                return
            
            # Extract probed SSID
            probed_ssid = ''
            if packet.info:
                probed_ssid = packet.info.decode('utf-8', errors='ignore')
            
            # Get signal strength
            signal_strength = -100
            if hasattr(packet, 'dBm_AntSignal'):
                signal_strength = packet.dBm_AntSignal
            
            # Update or create client entry
            if client_mac not in self.clients:
                self.clients[client_mac] = {
                    'mac_address': client_mac,
                    'vendor': self.get_vendor(client_mac),
                    'signal_strength': signal_strength,
                    'first_seen': timestamp,
                    'last_seen': timestamp,
                    'probed_ssids': set(),
                    'associated_bssid': None
                }
            
            client = self.clients[client_mac]
            client['last_seen'] = timestamp
            client['signal_strength'] = signal_strength
            
            if probed_ssid:
                client['probed_ssids'].add(probed_ssid)
                
        except Exception as e:
            logger.error(f"Error processing probe request: {e}")
    
    def process_probe_response(self, packet, timestamp):
        """Process probe responses"""
        # Similar to beacon processing but for probe responses
        pass
    
    def process_auth_frame(self, packet, timestamp):
        """Process authentication frames"""
        # Track authentication attempts
        pass
    
    def process_deauth_frame(self, packet, timestamp):
        """Process deauthentication frames"""
        # Track deauth attacks
        pass
    
    def start_monitor_scan(self, channels: List[int] = None) -> bool:
        """Start monitor mode scanning with packet capture"""
        try:
            if self.scanning:
                logger.warning("Scan already in progress")
                return False
            
            # Enable monitor mode
            if not self.wifi_interface.enable_monitor_mode():
                logger.error("Failed to enable monitor mode")
                return False
            
            # Set channels to scan
            if channels is None:
                channels = self.channels_2_4ghz + self.channels_5ghz
            
            self.scanning = True
            self.scan_start_time = datetime.now()
            self.packets_captured = 0
            self.networks.clear()
            self.clients.clear()
            
            # Start scanning thread
            self.scan_thread = threading.Thread(
                target=self._monitor_scan_worker, 
                args=(channels,)
            )
            self.scan_thread.daemon = True
            self.scan_thread.start()
            
            logger.info(f"Started monitor mode scan on {self.interface}")
            return True
            
        except Exception as e:
            logger.error(f"Error starting monitor scan: {e}")
            return False
    
    def _monitor_scan_worker(self, channels: List[int]):
        """Worker thread for monitor mode scanning"""
        try:
            channel_index = 0
            
            while self.scanning:
                # Change channel
                if channels:
                    channel = channels[channel_index % len(channels)]
                    self.set_channel(channel)
                    channel_index += 1
                
                # Capture packets for a short time
                try:
                    sniff(iface=self.interface, 
                          prn=self.packet_handler, 
                          timeout=self.channel_hop_interval,
                          store=0)
                except Exception as e:
                    logger.error(f"Error during packet capture: {e}")
                    time.sleep(0.1)
                    
        except Exception as e:
            logger.error(f"Error in monitor scan worker: {e}")
        finally:
            logger.info("Monitor scan worker stopped")
    
    def set_channel(self, channel: int) -> bool:
        """Set the channel for monitoring"""
        try:
            subprocess.run(['sudo', 'iw', self.interface, 'set', 'channel', str(channel)], 
                         check=True, timeout=5)
            self.current_channel = channel
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error setting channel {channel}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error setting channel {channel}: {e}")
            return False
    
    def start_basic_scan(self) -> List[Dict]:
        """Start basic WiFi scan using iwlist"""
        try:
            logger.info(f"Starting basic scan on {self.interface}")
            networks = self.parse_iwlist_scan()
            logger.info(f"Found {len(networks)} networks")
            return networks
        except Exception as e:
            logger.error(f"Error in basic scan: {e}")
            return []
    
    def stop_scan(self):
        """Stop the current scan"""
        try:
            if not self.scanning:
                logger.info("No scan in progress")
                return
            
            logger.info("Stopping scan...")
            self.scanning = False
            
            # Wait for scan thread to finish
            if self.scan_thread and self.scan_thread.is_alive():
                self.scan_thread.join(timeout=5)
            
            # Disable monitor mode
            self.wifi_interface.disable_monitor_mode()
            
            logger.info("Scan stopped")
            
        except Exception as e:
            logger.error(f"Error stopping scan: {e}")
    
    def get_scan_results(self) -> Dict:
        """Get current scan results"""
        return {
            'networks': {bssid: {
                **network,
                'clients': list(network['clients']),
                'probed_ssids': list(network.get('probed_ssids', set())),
                'first_seen': network['first_seen'].isoformat(),
                'last_seen': network['last_seen'].isoformat()
            } for bssid, network in self.networks.items()},
            'clients': {mac: {
                **client,
                'probed_ssids': list(client['probed_ssids']),
                'first_seen': client['first_seen'].isoformat(),
                'last_seen': client['last_seen'].isoformat()
            } for mac, client in self.clients.items()},
            'scan_info': {
                'interface': self.interface,
                'scanning': self.scanning,
                'packets_captured': self.packets_captured,
                'networks_found': len(self.networks),
                'clients_found': len(self.clients),
                'current_channel': self.current_channel,
                'scan_start_time': self.scan_start_time.isoformat() if self.scan_start_time else None
            }
        }
    
    def __del__(self):
        """Cleanup when scanner is destroyed"""
        try:
            self.stop_scan()
        except:
            pass

