"""
WiFi Network Data Model for Archway WiFi Analyzer
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class WiFiNetwork(db.Model):
    """Model for storing WiFi network information"""
    __tablename__ = 'wifi_networks'
    
    id = db.Column(db.Integer, primary_key=True)
    ssid = db.Column(db.String(255), nullable=False)
    bssid = db.Column(db.String(17), nullable=False, unique=True)  # MAC address format
    channel = db.Column(db.Integer, nullable=False)
    frequency = db.Column(db.Float, nullable=False)  # in MHz
    signal_strength = db.Column(db.Integer, nullable=False)  # in dBm
    quality = db.Column(db.Integer, default=0)
    encryption = db.Column(db.String(50), default='Open')
    cipher = db.Column(db.String(50), default='None')
    authentication = db.Column(db.String(50), default='None')
    mode = db.Column(db.String(20), default='Master')  # Master, Ad-Hoc, etc.
    vendor = db.Column(db.String(100), default='Unknown')
    first_seen = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    beacon_interval = db.Column(db.Integer, default=100)
    privacy = db.Column(db.Boolean, default=False)
    wps = db.Column(db.Boolean, default=False)
    client_count = db.Column(db.Integer, default=0)
    data_packets = db.Column(db.Integer, default=0)
    data_bytes = db.Column(db.BigInteger, default=0)
    
    # Relationship to clients
    clients = db.relationship('WiFiClient', backref='network', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert network to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'ssid': self.ssid,
            'bssid': self.bssid,
            'channel': self.channel,
            'frequency': self.frequency,
            'signal_strength': self.signal_strength,
            'quality': self.quality,
            'encryption': self.encryption,
            'cipher': self.cipher,
            'authentication': self.authentication,
            'mode': self.mode,
            'vendor': self.vendor,
            'first_seen': self.first_seen.isoformat() if self.first_seen else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'beacon_interval': self.beacon_interval,
            'privacy': self.privacy,
            'wps': self.wps,
            'client_count': self.client_count,
            'data_packets': self.data_packets,
            'data_bytes': self.data_bytes
        }

class WiFiClient(db.Model):
    """Model for storing WiFi client information"""
    __tablename__ = 'wifi_clients'
    
    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.String(17), nullable=False, unique=True)
    network_id = db.Column(db.Integer, db.ForeignKey('wifi_networks.id'), nullable=True)
    vendor = db.Column(db.String(100), default='Unknown')
    signal_strength = db.Column(db.Integer, default=0)
    first_seen = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    data_packets = db.Column(db.Integer, default=0)
    data_bytes = db.Column(db.BigInteger, default=0)
    probed_ssids = db.Column(db.Text, default='[]')  # JSON array of probed SSIDs
    
    def get_probed_ssids(self):
        """Get list of probed SSIDs"""
        try:
            return json.loads(self.probed_ssids)
        except:
            return []
    
    def add_probed_ssid(self, ssid):
        """Add a probed SSID to the list"""
        probed = self.get_probed_ssids()
        if ssid not in probed:
            probed.append(ssid)
            self.probed_ssids = json.dumps(probed)
    
    def to_dict(self):
        """Convert client to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'mac_address': self.mac_address,
            'network_id': self.network_id,
            'vendor': self.vendor,
            'signal_strength': self.signal_strength,
            'first_seen': self.first_seen.isoformat() if self.first_seen else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'data_packets': self.data_packets,
            'data_bytes': self.data_bytes,
            'probed_ssids': self.get_probed_ssids()
        }

class ScanSession(db.Model):
    """Model for storing scan session information"""
    __tablename__ = 'scan_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    interface = db.Column(db.String(20), nullable=False)
    scan_type = db.Column(db.String(50), default='passive')  # passive, active, monitor
    channels_scanned = db.Column(db.Text, default='[]')  # JSON array of channels
    networks_found = db.Column(db.Integer, default=0)
    clients_found = db.Column(db.Integer, default=0)
    packets_captured = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='running')  # running, completed, error
    
    def get_channels_scanned(self):
        """Get list of scanned channels"""
        try:
            return json.loads(self.channels_scanned)
        except:
            return []
    
    def set_channels_scanned(self, channels):
        """Set the list of scanned channels"""
        self.channels_scanned = json.dumps(channels)
    
    def to_dict(self):
        """Convert scan session to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'interface': self.interface,
            'scan_type': self.scan_type,
            'channels_scanned': self.get_channels_scanned(),
            'networks_found': self.networks_found,
            'clients_found': self.clients_found,
            'packets_captured': self.packets_captured,
            'status': self.status
        }

class SpectrumData(db.Model):
    """Model for storing spectrum analysis data"""
    __tablename__ = 'spectrum_data'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    frequency = db.Column(db.Float, nullable=False)  # in MHz
    power_level = db.Column(db.Float, nullable=False)  # in dBm
    bandwidth = db.Column(db.Float, default=1.0)  # in MHz
    scan_session_id = db.Column(db.Integer, db.ForeignKey('scan_sessions.id'), nullable=True)
    
    def to_dict(self):
        """Convert spectrum data to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'frequency': self.frequency,
            'power_level': self.power_level,
            'bandwidth': self.bandwidth,
            'scan_session_id': self.scan_session_id
        }

