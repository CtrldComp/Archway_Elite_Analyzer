"""
Advanced WiFi Analysis Module
Implements elite-level network analysis capabilities
"""

import json
import time
import hashlib
import statistics
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Any, Optional, Tuple

class ThreatDetector:
    """Advanced threat detection for WiFi networks"""
    
    def __init__(self):
        self.suspicious_patterns = {
            'evil_twin': [],
            'deauth_attacks': [],
            'beacon_flooding': [],
            'karma_attacks': [],
            'rogue_ap': []
        }
        
    def detect_evil_twin(self, networks: List[Dict]) -> List[Dict]:
        """Detect potential evil twin attacks"""
        ssid_groups = defaultdict(list)
        
        # Group networks by SSID
        for network in networks:
            if network.get('ssid'):
                ssid_groups[network['ssid']].append(network)
        
        evil_twins = []
        for ssid, network_list in ssid_groups.items():
            if len(network_list) > 1:
                # Check for suspicious patterns
                for i, net1 in enumerate(network_list):
                    for net2 in network_list[i+1:]:
                        # Different BSSIDs but same SSID
                        if (net1['bssid'] != net2['bssid'] and 
                            abs(net1.get('signal_strength', -100) - net2.get('signal_strength', -100)) < 10):
                            
                            evil_twins.append({
                                'type': 'evil_twin',
                                'severity': 'high',
                                'ssid': ssid,
                                'networks': [net1, net2],
                                'description': f'Potential evil twin detected for {ssid}',
                                'detected_at': datetime.now().isoformat()
                            })
        
        return evil_twins
    
    def detect_rogue_ap(self, networks: List[Dict]) -> List[Dict]:
        """Detect rogue access points"""
        rogue_aps = []
        
        for network in networks:
            # Check for suspicious characteristics
            suspicious_score = 0
            reasons = []
            
            # Open network in enterprise environment
            if network.get('encryption') == 'Open':
                suspicious_score += 3
                reasons.append('Open network detected')
            
            # Unusual vendor
            vendor = network.get('vendor', '').lower()
            if any(keyword in vendor for keyword in ['unknown', 'private', 'random']):
                suspicious_score += 2
                reasons.append('Unusual vendor')
            
            # High signal strength (potentially close/rogue)
            if network.get('signal_strength', -100) > -30:
                suspicious_score += 1
                reasons.append('Unusually strong signal')
            
            # Common honeypot SSIDs
            ssid = network.get('ssid', '').lower()
            honeypot_names = ['free wifi', 'public', 'guest', 'open', 'internet']
            if any(name in ssid for name in honeypot_names):
                suspicious_score += 2
                reasons.append('Suspicious SSID pattern')
            
            if suspicious_score >= 4:
                rogue_aps.append({
                    'type': 'rogue_ap',
                    'severity': 'medium' if suspicious_score < 6 else 'high',
                    'network': network,
                    'score': suspicious_score,
                    'reasons': reasons,
                    'description': f'Potential rogue AP: {network.get("ssid", "Hidden")}',
                    'detected_at': datetime.now().isoformat()
                })
        
        return rogue_aps

class NetworkAnalytics:
    """Advanced network analytics and insights"""
    
    def __init__(self):
        self.historical_data = []
        
    def analyze_channel_utilization(self, networks: List[Dict]) -> Dict[str, Any]:
        """Analyze channel utilization and interference"""
        channel_data = defaultdict(list)
        
        for network in networks:
            channel = network.get('channel')
            if channel:
                channel_data[str(channel)].append(network)
        
        utilization = {}
        interference_map = {}
        
        for channel, nets in channel_data.items():
            utilization[channel] = len(nets)
            
            # Calculate interference score
            total_signal = sum(abs(net.get('signal_strength', -100)) for net in nets)
            interference_map[channel] = {
                'network_count': len(nets),
                'total_signal_power': total_signal,
                'interference_score': min(100, (len(nets) * 10) + (total_signal / 10))
            }
        
        # Find optimal channels
        optimal_channels = self._find_optimal_channels(interference_map)
        
        return {
            'utilization': utilization,
            'interference_map': interference_map,
            'optimal_channels': optimal_channels,
            'congestion_level': self._calculate_congestion_level(utilization)
        }
    
    def _find_optimal_channels(self, interference_map: Dict) -> List[Dict]:
        """Find optimal channels with least interference"""
        # 2.4GHz non-overlapping channels: 1, 6, 11
        # 5GHz has many more non-overlapping channels
        
        optimal = []
        sorted_channels = sorted(interference_map.items(), 
                               key=lambda x: x[1]['interference_score'])
        
        for channel, data in sorted_channels[:5]:  # Top 5 optimal channels
            optimal.append({
                'channel': int(channel),
                'interference_score': data['interference_score'],
                'network_count': data['network_count'],
                'recommendation': 'excellent' if data['interference_score'] < 20 else 
                               'good' if data['interference_score'] < 50 else 'poor'
            })
        
        return optimal
    
    def _calculate_congestion_level(self, utilization: Dict) -> str:
        """Calculate overall network congestion level"""
        if not utilization:
            return 'none'
        
        avg_networks_per_channel = statistics.mean(utilization.values())
        
        if avg_networks_per_channel < 2:
            return 'low'
        elif avg_networks_per_channel < 5:
            return 'moderate'
        elif avg_networks_per_channel < 10:
            return 'high'
        else:
            return 'severe'
    
    def analyze_security_posture(self, networks: List[Dict]) -> Dict[str, Any]:
        """Analyze overall security posture of the environment"""
        total_networks = len(networks)
        if total_networks == 0:
            return {'total_networks': 0, 'security_score': 0}
        
        encryption_counts = Counter(net.get('encryption', 'Unknown') for net in networks)
        
        # Calculate security score
        security_score = 0
        for encryption, count in encryption_counts.items():
            weight = {
                'WPA3': 100,
                'WPA2': 80,
                'WPA': 60,
                'WEP': 20,
                'Open': 0
            }.get(encryption, 50)
            
            security_score += (count / total_networks) * weight
        
        # Security recommendations
        recommendations = []
        if encryption_counts.get('Open', 0) > 0:
            recommendations.append('Secure open networks with WPA2/WPA3')
        if encryption_counts.get('WEP', 0) > 0:
            recommendations.append('Upgrade WEP networks to WPA2/WPA3')
        if encryption_counts.get('WPA', 0) > 0:
            recommendations.append('Upgrade WPA networks to WPA2/WPA3')
        
        return {
            'total_networks': total_networks,
            'encryption_distribution': dict(encryption_counts),
            'security_score': round(security_score, 1),
            'security_level': self._get_security_level(security_score),
            'recommendations': recommendations,
            'vulnerable_networks': encryption_counts.get('Open', 0) + encryption_counts.get('WEP', 0)
        }
    
    def _get_security_level(self, score: float) -> str:
        """Convert security score to level"""
        if score >= 90:
            return 'excellent'
        elif score >= 70:
            return 'good'
        elif score >= 50:
            return 'fair'
        elif score >= 30:
            return 'poor'
        else:
            return 'critical'
    
    def generate_network_fingerprint(self, network: Dict) -> str:
        """Generate unique fingerprint for network identification"""
        fingerprint_data = {
            'bssid': network.get('bssid', ''),
            'ssid': network.get('ssid', ''),
            'channel': network.get('channel', ''),
            'encryption': network.get('encryption', ''),
            'vendor': network.get('vendor', '')
        }
        
        fingerprint_str = json.dumps(fingerprint_data, sort_keys=True)
        return hashlib.sha256(fingerprint_str.encode()).hexdigest()[:16]

class SignalAnalyzer:
    """Advanced signal analysis and RF insights"""
    
    def __init__(self):
        self.signal_history = defaultdict(list)
        
    def analyze_signal_patterns(self, networks: List[Dict]) -> Dict[str, Any]:
        """Analyze signal strength patterns and variations"""
        signal_data = []
        
        for network in networks:
            signal = network.get('signal_strength')
            if signal is not None:
                signal_data.append(abs(signal))  # Convert to positive for easier analysis
        
        if not signal_data:
            return {'error': 'No signal data available'}
        
        analysis = {
            'average_signal': round(statistics.mean(signal_data), 1),
            'median_signal': round(statistics.median(signal_data), 1),
            'signal_range': {
                'min': min(signal_data),
                'max': max(signal_data)
            },
            'signal_distribution': self._categorize_signals(signal_data),
            'quality_assessment': self._assess_signal_quality(signal_data)
        }
        
        if len(signal_data) > 1:
            analysis['standard_deviation'] = round(statistics.stdev(signal_data), 1)
        
        return analysis
    
    def _categorize_signals(self, signal_data: List[float]) -> Dict[str, int]:
        """Categorize signals by strength"""
        categories = {
            'excellent': 0,  # > 50 dBm
            'good': 0,       # 30-50 dBm  
            'fair': 0,       # 50-70 dBm
            'poor': 0        # < 70 dBm
        }
        
        for signal in signal_data:
            if signal < 50:
                categories['excellent'] += 1
            elif signal < 70:
                categories['good'] += 1
            elif signal < 85:
                categories['fair'] += 1
            else:
                categories['poor'] += 1
        
        return categories
    
    def _assess_signal_quality(self, signal_data: List[float]) -> str:
        """Assess overall signal quality in the environment"""
        avg_signal = statistics.mean(signal_data)
        
        if avg_signal < 50:
            return 'excellent'
        elif avg_signal < 70:
            return 'good'
        elif avg_signal < 85:
            return 'fair'
        else:
            return 'poor'

class AdvancedWiFiAnalyzer:
    """Main advanced analyzer combining all analysis modules"""
    
    def __init__(self):
        self.threat_detector = ThreatDetector()
        self.network_analytics = NetworkAnalytics()
        self.signal_analyzer = SignalAnalyzer()
        
    def perform_comprehensive_analysis(self, networks: List[Dict]) -> Dict[str, Any]:
        """Perform comprehensive analysis of WiFi environment"""
        if not networks:
            return {'error': 'No networks to analyze'}
        
        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'total_networks': len(networks),
            'analysis_duration': 0,  # Will be calculated
            'threat_analysis': {},
            'channel_analysis': {},
            'security_analysis': {},
            'signal_analysis': {},
            'recommendations': []
        }
        
        start_time = time.time()
        
        try:
            # Threat detection
            evil_twins = self.threat_detector.detect_evil_twin(networks)
            rogue_aps = self.threat_detector.detect_rogue_ap(networks)
            
            analysis_results['threat_analysis'] = {
                'evil_twins': evil_twins,
                'rogue_aps': rogue_aps,
                'total_threats': len(evil_twins) + len(rogue_aps),
                'threat_level': self._calculate_threat_level(evil_twins, rogue_aps)
            }
            
            # Channel analysis
            analysis_results['channel_analysis'] = self.network_analytics.analyze_channel_utilization(networks)
            
            # Security analysis
            analysis_results['security_analysis'] = self.network_analytics.analyze_security_posture(networks)
            
            # Signal analysis
            analysis_results['signal_analysis'] = self.signal_analyzer.analyze_signal_patterns(networks)
            
            # Generate recommendations
            analysis_results['recommendations'] = self._generate_recommendations(analysis_results)
            
        except Exception as e:
            analysis_results['error'] = f'Analysis error: {str(e)}'
        
        analysis_results['analysis_duration'] = round(time.time() - start_time, 2)
        
        return analysis_results
    
    def _calculate_threat_level(self, evil_twins: List, rogue_aps: List) -> str:
        """Calculate overall threat level"""
        high_threats = sum(1 for threat in evil_twins + rogue_aps 
                          if threat.get('severity') == 'high')
        medium_threats = sum(1 for threat in evil_twins + rogue_aps 
                           if threat.get('severity') == 'medium')
        
        if high_threats > 0:
            return 'high'
        elif medium_threats > 2:
            return 'medium'
        elif medium_threats > 0:
            return 'low'
        else:
            return 'none'
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        # Security recommendations
        security = analysis.get('security_analysis', {})
        if security.get('vulnerable_networks', 0) > 0:
            recommendations.append(f"Secure {security['vulnerable_networks']} vulnerable networks")
        
        # Channel recommendations
        channel = analysis.get('channel_analysis', {})
        if channel.get('congestion_level') in ['high', 'severe']:
            recommendations.append("Consider using less congested channels")
            optimal = channel.get('optimal_channels', [])
            if optimal:
                best_channel = optimal[0]['channel']
                recommendations.append(f"Channel {best_channel} shows optimal performance")
        
        # Threat recommendations
        threats = analysis.get('threat_analysis', {})
        if threats.get('total_threats', 0) > 0:
            recommendations.append("Investigate detected security threats immediately")
        
        # Signal recommendations
        signal = analysis.get('signal_analysis', {})
        if signal.get('quality_assessment') == 'poor':
            recommendations.append("Consider improving AP placement for better coverage")
        
        return recommendations

