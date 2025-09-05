"""
WiFi API Routes for Archway WiFi Analyzer
Provides RESTful API endpoints for WiFi scanning and analysis
"""

from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
import threading
import time
from datetime import datetime
from src.core.wifi_scanner import WiFiScanner, WiFiInterface
from src.models.wifi_network import WiFiNetwork, WiFiClient, ScanSession, SpectrumData, db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
wifi_bp = Blueprint('wifi', __name__)

# Global scanner instance
scanner = None
scanner_lock = threading.Lock()

@wifi_bp.route('/interfaces', methods=['GET'])
@cross_origin()
def get_interfaces():
    """Get available WiFi interfaces"""
    try:
        wifi_interface = WiFiInterface('')
        interfaces = wifi_interface.get_available_interfaces()
        
        interface_info = []
        for iface in interfaces:
            wifi_iface = WiFiInterface(iface)
            info = wifi_iface.get_interface_info()
            interface_info.append(info)
        
        return jsonify({
            'success': True,
            'interfaces': interface_info
        })
        
    except Exception as e:
        logger.error(f"Error getting interfaces: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@wifi_bp.route('/interface/<interface_name>/info', methods=['GET'])
@cross_origin()
def get_interface_info(interface_name):
    """Get detailed information about a specific interface"""
    try:
        wifi_interface = WiFiInterface(interface_name)
        info = wifi_interface.get_interface_info()
        
        return jsonify({
            'success': True,
            'interface_info': info
        })
        
    except Exception as e:
        logger.error(f"Error getting interface info: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@wifi_bp.route('/scan/start', methods=['POST'])
@cross_origin()
def start_scan():
    """Start WiFi scanning"""
    global scanner
    
    try:
        data = request.get_json() or {}
        interface = data.get('interface', 'wlan0')
        scan_type = data.get('scan_type', 'basic')  # basic, monitor, passive
        channels = data.get('channels', None)
        duration = data.get('duration', 30)  # seconds
        
        with scanner_lock:
            if scanner and scanner.scanning:
                return jsonify({
                    'success': False,
                    'error': 'Scan already in progress'
                }), 400
            
            # Create new scanner instance
            scanner = WiFiScanner(interface)
            
            # Create scan session record
            scan_session = ScanSession(
                interface=interface,
                scan_type=scan_type,
                status='running'
            )
            
            if channels:
                scan_session.set_channels_scanned(channels)
            
            db.session.add(scan_session)
            db.session.commit()
            
            # Start appropriate scan type
            if scan_type == 'basic':
                # Start basic scan in background thread
                def basic_scan_worker():
                    try:
                        networks = scanner.start_basic_scan()
                        
                        # Store results in database
                        for network_data in networks:
                            network = WiFiNetwork.query.filter_by(bssid=network_data['bssid']).first()
                            
                            if not network:
                                network = WiFiNetwork(
                                    ssid=network_data.get('ssid', ''),
                                    bssid=network_data['bssid'],
                                    channel=network_data.get('channel', 0),
                                    frequency=network_data.get('frequency', 0.0),
                                    signal_strength=network_data.get('signal_strength', -100),
                                    quality=network_data.get('quality', 0),
                                    encryption=network_data.get('encryption', 'Open'),
                                    mode=network_data.get('mode', 'Master'),
                                    vendor=network_data.get('vendor', 'Unknown')
                                )
                                db.session.add(network)
                            else:
                                # Update existing network
                                network.last_seen = datetime.utcnow()
                                network.signal_strength = network_data.get('signal_strength', network.signal_strength)
                                network.quality = network_data.get('quality', network.quality)
                        
                        # Update scan session
                        scan_session.status = 'completed'
                        scan_session.end_time = datetime.utcnow()
                        scan_session.networks_found = len(networks)
                        
                        db.session.commit()
                        
                    except Exception as e:
                        logger.error(f"Error in basic scan worker: {e}")
                        scan_session.status = 'error'
                        db.session.commit()
                
                thread = threading.Thread(target=basic_scan_worker)
                thread.daemon = True
                thread.start()
                
            elif scan_type == 'monitor':
                # Start monitor mode scan
                success = scanner.start_monitor_scan(channels)
                if not success:
                    scan_session.status = 'error'
                    db.session.commit()
                    return jsonify({
                        'success': False,
                        'error': 'Failed to start monitor mode scan'
                    }), 500
                
                # Schedule scan stop after duration
                def stop_scan_after_duration():
                    time.sleep(duration)
                    if scanner:
                        scanner.stop_scan()
                        scan_session.status = 'completed'
                        scan_session.end_time = datetime.utcnow()
                        db.session.commit()
                
                thread = threading.Thread(target=stop_scan_after_duration)
                thread.daemon = True
                thread.start()
            
            return jsonify({
                'success': True,
                'scan_session_id': scan_session.id,
                'message': f'Started {scan_type} scan on {interface}'
            })
            
    except Exception as e:
        logger.error(f"Error starting scan: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@wifi_bp.route('/scan/stop', methods=['POST'])
@cross_origin()
def stop_scan():
    """Stop current WiFi scan"""
    global scanner
    
    try:
        with scanner_lock:
            if not scanner or not scanner.scanning:
                return jsonify({
                    'success': False,
                    'error': 'No scan in progress'
                }), 400
            
            scanner.stop_scan()
            
            return jsonify({
                'success': True,
                'message': 'Scan stopped'
            })
            
    except Exception as e:
        logger.error(f"Error stopping scan: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@wifi_bp.route('/scan/status', methods=['GET'])
@cross_origin()
def get_scan_status():
    """Get current scan status"""
    global scanner
    
    try:
        with scanner_lock:
            if not scanner:
                return jsonify({
                    'success': True,
                    'scanning': False,
                    'message': 'No scanner initialized'
                })
            
            results = scanner.get_scan_results()
            
            return jsonify({
                'success': True,
                'scanning': scanner.scanning,
                'scan_info': results['scan_info'],
                'networks_count': len(results['networks']),
                'clients_count': len(results['clients'])
            })
            
    except Exception as e:
        logger.error(f"Error getting scan status: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@wifi_bp.route('/scan/results', methods=['GET'])
@cross_origin()
def get_scan_results():
    """Get current scan results"""
    global scanner
    
    try:
        with scanner_lock:
            if not scanner:
                return jsonify({
                    'success': False,
                    'error': 'No scanner initialized'
                }), 400
            
            results = scanner.get_scan_results()
            
            return jsonify({
                'success': True,
                'results': results
            })
            
    except Exception as e:
        logger.error(f"Error getting scan results: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@wifi_bp.route('/networks', methods=['GET'])
@cross_origin()
def get_networks():
    """Get all discovered networks from database"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        sort_by = request.args.get('sort_by', 'last_seen')
        order = request.args.get('order', 'desc')
        
        # Build query
        query = WiFiNetwork.query
        
        # Apply sorting
        if hasattr(WiFiNetwork, sort_by):
            if order == 'desc':
                query = query.order_by(getattr(WiFiNetwork, sort_by).desc())
            else:
                query = query.order_by(getattr(WiFiNetwork, sort_by).asc())
        
        # Paginate
        networks = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'networks': [network.to_dict() for network in networks.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': networks.total,
                'pages': networks.pages,
                'has_next': networks.has_next,
                'has_prev': networks.has_prev
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting networks: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@wifi_bp.route('/networks/<int:network_id>', methods=['GET'])
@cross_origin()
def get_network_details(network_id):
    """Get detailed information about a specific network"""
    try:
        network = WiFiNetwork.query.get_or_404(network_id)
        
        # Get associated clients
        clients = [client.to_dict() for client in network.clients]
        
        network_data = network.to_dict()
        network_data['clients'] = clients
        
        return jsonify({
            'success': True,
            'network': network_data
        })
        
    except Exception as e:
        logger.error(f"Error getting network details: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@wifi_bp.route('/clients', methods=['GET'])
@cross_origin()
def get_clients():
    """Get all discovered clients from database"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        clients = WiFiClient.query.order_by(WiFiClient.last_seen.desc()).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'clients': [client.to_dict() for client in clients.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': clients.total,
                'pages': clients.pages,
                'has_next': clients.has_next,
                'has_prev': clients.has_prev
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting clients: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@wifi_bp.route('/scan/sessions', methods=['GET'])
@cross_origin()
def get_scan_sessions():
    """Get scan session history"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        sessions = ScanSession.query.order_by(ScanSession.start_time.desc()).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'sessions': [session.to_dict() for session in sessions.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': sessions.total,
                'pages': sessions.pages,
                'has_next': sessions.has_next,
                'has_prev': sessions.has_prev
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting scan sessions: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@wifi_bp.route('/spectrum/start', methods=['POST'])
@cross_origin()
def start_spectrum_analysis():
    """Start spectrum analysis (placeholder for future SDR integration)"""
    try:
        data = request.get_json() or {}
        interface = data.get('interface', 'wlan0')
        frequency_range = data.get('frequency_range', '2.4GHz')  # 2.4GHz, 5GHz, both
        
        # This would integrate with SDR hardware like HackRF or Ubertooth
        # For now, return a placeholder response
        
        return jsonify({
            'success': True,
            'message': 'Spectrum analysis started (placeholder)',
            'note': 'SDR integration required for full spectrum analysis'
        })
        
    except Exception as e:
        logger.error(f"Error starting spectrum analysis: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@wifi_bp.route('/analytics/summary', methods=['GET'])
@cross_origin()
def get_analytics_summary():
    """Get analytics summary of WiFi environment"""
    try:
        # Get network statistics
        total_networks = WiFiNetwork.query.count()
        total_clients = WiFiClient.query.count()
        
        # Get encryption statistics
        encryption_stats = db.session.query(
            WiFiNetwork.encryption, 
            db.func.count(WiFiNetwork.id)
        ).group_by(WiFiNetwork.encryption).all()
        
        # Get channel utilization
        channel_stats = db.session.query(
            WiFiNetwork.channel, 
            db.func.count(WiFiNetwork.id)
        ).group_by(WiFiNetwork.channel).all()
        
        # Get vendor statistics
        vendor_stats = db.session.query(
            WiFiNetwork.vendor, 
            db.func.count(WiFiNetwork.id)
        ).group_by(WiFiNetwork.vendor).limit(10).all()
        
        return jsonify({
            'success': True,
            'summary': {
                'total_networks': total_networks,
                'total_clients': total_clients,
                'encryption_distribution': dict(encryption_stats),
                'channel_utilization': dict(channel_stats),
                'top_vendors': dict(vendor_stats)
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting analytics summary: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@wifi_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'service': 'Archway WiFi Analyzer API',
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })



# Advanced Analysis Endpoints
from src.core.advanced_analyzer import AdvancedWiFiAnalyzer
from src.data.sample_networks import generate_sample_networks, generate_sample_clients

# Initialize advanced analyzer
advanced_analyzer = AdvancedWiFiAnalyzer()

# Load sample data for demonstration
sample_networks = generate_sample_networks()
sample_clients = generate_sample_clients()

@wifi_bp.route('/analytics/advanced', methods=['GET'])
@cross_origin()
def get_advanced_analytics():
    """Get comprehensive advanced analytics"""
    try:
        # Get networks from database or use sample data
        networks_query = WiFiNetwork.query.all()
        
        if networks_query:
            networks = [network.to_dict() for network in networks_query]
        else:
            # Use sample data for demonstration
            networks = sample_networks
        
        if not networks:
            return jsonify({
                'success': False,
                'error': 'No network data available for analysis'
            }), 400
        
        analysis = advanced_analyzer.perform_comprehensive_analysis(networks)
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        logger.error(f"Advanced analytics error: {e}")
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500

@wifi_bp.route('/analytics/threats', methods=['GET'])
@cross_origin()
def get_threat_analysis():
    """Get threat detection results"""
    try:
        # Get networks from database or use sample data
        networks_query = WiFiNetwork.query.all()
        
        if networks_query:
            networks = [network.to_dict() for network in networks_query]
        else:
            networks = sample_networks
        
        if not networks:
            return jsonify({
                'success': True,
                'threats': {
                    'evil_twins': [],
                    'rogue_aps': [],
                    'total_threats': 0
                }
            })
        
        evil_twins = advanced_analyzer.threat_detector.detect_evil_twin(networks)
        rogue_aps = advanced_analyzer.threat_detector.detect_rogue_ap(networks)
        
        return jsonify({
            'success': True,
            'threats': {
                'evil_twins': evil_twins,
                'rogue_aps': rogue_aps,
                'total_threats': len(evil_twins) + len(rogue_aps),
                'last_updated': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Threat analysis error: {e}")
        return jsonify({
            'success': False,
            'error': f'Threat analysis failed: {str(e)}'
        }), 500

@wifi_bp.route('/analytics/channels', methods=['GET'])
@cross_origin()
def get_channel_analysis():
    """Get channel utilization and interference analysis"""
    try:
        # Get networks from database or use sample data
        networks_query = WiFiNetwork.query.all()
        
        if networks_query:
            networks = [network.to_dict() for network in networks_query]
        else:
            networks = sample_networks
        
        if not networks:
            return jsonify({
                'success': True,
                'channel_analysis': {
                    'utilization': {},
                    'interference_map': {},
                    'optimal_channels': []
                }
            })
        
        analysis = advanced_analyzer.network_analytics.analyze_channel_utilization(networks)
        return jsonify({
            'success': True,
            'channel_analysis': analysis
        })
        
    except Exception as e:
        logger.error(f"Channel analysis error: {e}")
        return jsonify({
            'success': False,
            'error': f'Channel analysis failed: {str(e)}'
        }), 500

@wifi_bp.route('/analytics/security', methods=['GET'])
@cross_origin()
def get_security_analysis():
    """Get security posture analysis"""
    try:
        # Get networks from database or use sample data
        networks_query = WiFiNetwork.query.all()
        
        if networks_query:
            networks = [network.to_dict() for network in networks_query]
        else:
            networks = sample_networks
        
        if not networks:
            return jsonify({
                'success': True,
                'security_analysis': {
                    'total_networks': 0,
                    'security_score': 0,
                    'vulnerable_networks': 0
                }
            })
        
        analysis = advanced_analyzer.network_analytics.analyze_security_posture(networks)
        return jsonify({
            'success': True,
            'security_analysis': analysis
        })
        
    except Exception as e:
        logger.error(f"Security analysis error: {e}")
        return jsonify({
            'success': False,
            'error': f'Security analysis failed: {str(e)}'
        }), 500

@wifi_bp.route('/demo/populate', methods=['POST'])
@cross_origin()
def populate_demo_data():
    """Populate database with sample data for demonstration"""
    try:
        # Clear existing data
        WiFiClient.query.delete()
        WiFiNetwork.query.delete()
        db.session.commit()
        
        # Add sample networks
        for network_data in sample_networks:
            network = WiFiNetwork(
                ssid=network_data.get('ssid', ''),
                bssid=network_data['bssid'],
                channel=network_data.get('channel', 0),
                frequency=network_data.get('frequency', 0.0),
                signal_strength=network_data.get('signal_strength', -100),
                quality=network_data.get('quality', 0),
                encryption=network_data.get('encryption', 'Open'),
                mode=network_data.get('mode', 'Master'),
                vendor=network_data.get('vendor', 'Unknown')
            )
            db.session.add(network)
        
        # Add sample clients
        for client_data in sample_clients:
            client = WiFiClient(
                mac_address=client_data['mac_address'],
                vendor=client_data.get('vendor', 'Unknown'),
                signal_strength=client_data.get('signal_strength', -100),
                network_id=client_data.get('network_id', 1)
            )
            db.session.add(client)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Populated {len(sample_networks)} networks and {len(sample_clients)} clients'
        })
        
    except Exception as e:
        logger.error(f"Error populating demo data: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

