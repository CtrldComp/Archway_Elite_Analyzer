import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useToast } from '@/hooks/use-toast'
import { 
  Wifi, 
  Users, 
  Radio, 
  Activity, 
  Play, 
  Square, 
  RefreshCw,
  Shield,
  AlertTriangle,
  TrendingUp,
  Zap
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8']

export default function Dashboard({ scanStatus, setScanStatus, currentScan, setCurrentScan }) {
  const [interfaces, setInterfaces] = useState([])
  const [selectedInterface, setSelectedInterface] = useState('')
  const [scanType, setScanType] = useState('basic')
  const [analytics, setAnalytics] = useState(null)
  const [recentNetworks, setRecentNetworks] = useState([])
  const [loading, setLoading] = useState(false)
  const { toast } = useToast()

  // Load interfaces on component mount
  useEffect(() => {
    loadInterfaces()
    loadAnalytics()
    loadRecentNetworks()
  }, [])

  const loadInterfaces = async () => {
    try {
      const response = await fetch('/api/wifi/interfaces')
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setInterfaces(data.interfaces)
          // Auto-select first wireless interface
          const wirelessInterface = data.interfaces.find(iface => iface.wireless)
          if (wirelessInterface) {
            setSelectedInterface(wirelessInterface.interface)
          }
        }
      }
    } catch (error) {
      console.error('Error loading interfaces:', error)
    }
  }

  const loadAnalytics = async () => {
    try {
      const response = await fetch('/api/wifi/analytics/summary')
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setAnalytics(data.summary)
        }
      }
    } catch (error) {
      console.error('Error loading analytics:', error)
    }
  }

  const loadRecentNetworks = async () => {
    try {
      const response = await fetch('/api/wifi/networks?per_page=5&sort_by=last_seen&order=desc')
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setRecentNetworks(data.networks)
        }
      }
    } catch (error) {
      console.error('Error loading recent networks:', error)
    }
  }

  const startScan = async () => {
    if (!selectedInterface) {
      toast({
        title: "Error",
        description: "Please select a wireless interface",
        variant: "destructive"
      })
      return
    }

    setLoading(true)
    try {
      const response = await fetch('/api/wifi/scan/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          interface: selectedInterface,
          scan_type: scanType,
          duration: 60
        })
      })

      const data = await response.json()
      if (data.success) {
        setCurrentScan(data.scan_session_id)
        toast({
          title: "Scan Started",
          description: `Started ${scanType} scan on ${selectedInterface}`,
        })
      } else {
        toast({
          title: "Scan Failed",
          description: data.error || "Failed to start scan",
          variant: "destructive"
        })
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to start scan",
        variant: "destructive"
      })
    } finally {
      setLoading(false)
    }
  }

  const stopScan = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/wifi/scan/stop', {
        method: 'POST'
      })

      const data = await response.json()
      if (data.success) {
        setCurrentScan(null)
        toast({
          title: "Scan Stopped",
          description: "WiFi scan has been stopped",
        })
      } else {
        toast({
          title: "Error",
          description: data.error || "Failed to stop scan",
          variant: "destructive"
        })
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to stop scan",
        variant: "destructive"
      })
    } finally {
      setLoading(false)
    }
  }

  // Generate sample data for charts
  const signalData = [
    { time: '10:00', signal: -45 },
    { time: '10:05', signal: -52 },
    { time: '10:10', signal: -48 },
    { time: '10:15', signal: -55 },
    { time: '10:20', signal: -50 },
    { time: '10:25', signal: -47 },
  ]

  const encryptionData = analytics ? Object.entries(analytics.encryption_distribution).map(([key, value]) => ({
    name: key,
    value: value
  })) : []

  const channelData = analytics ? Object.entries(analytics.channel_utilization).map(([key, value]) => ({
    channel: `Ch ${key}`,
    networks: value
  })) : []

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">WiFi Analysis Dashboard</h1>
          <p className="text-muted-foreground">Elite network monitoring and analysis</p>
        </div>
        
        <div className="flex items-center space-x-2">
          <Badge variant={scanStatus.scanning ? "default" : "secondary"} className="px-3 py-1">
            {scanStatus.scanning ? (
              <>
                <Activity className="w-3 h-3 mr-1 animate-pulse" />
                Scanning
              </>
            ) : (
              <>
                <Radio className="w-3 h-3 mr-1" />
                Idle
              </>
            )}
          </Badge>
        </div>
      </div>

      {/* Scan Controls */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Zap className="w-5 h-5" />
            <span>Scan Controls</span>
          </CardTitle>
          <CardDescription>
            Configure and control WiFi scanning operations
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="text-sm font-medium text-foreground mb-2 block">Interface</label>
              <Select value={selectedInterface} onValueChange={setSelectedInterface}>
                <SelectTrigger>
                  <SelectValue placeholder="Select interface" />
                </SelectTrigger>
                <SelectContent>
                  {interfaces.map((iface) => (
                    <SelectItem key={iface.interface} value={iface.interface}>
                      {iface.interface} {iface.wireless && <Badge variant="outline" className="ml-2">WiFi</Badge>}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            
            <div>
              <label className="text-sm font-medium text-foreground mb-2 block">Scan Type</label>
              <Select value={scanType} onValueChange={setScanType}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="basic">Basic Scan</SelectItem>
                  <SelectItem value="monitor">Monitor Mode</SelectItem>
                  <SelectItem value="passive">Passive Scan</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="flex items-end">
              {scanStatus.scanning ? (
                <Button 
                  onClick={stopScan} 
                  disabled={loading}
                  variant="destructive"
                  className="w-full"
                >
                  <Square className="w-4 h-4 mr-2" />
                  Stop Scan
                </Button>
              ) : (
                <Button 
                  onClick={startScan} 
                  disabled={loading || !selectedInterface}
                  className="w-full"
                >
                  <Play className="w-4 h-4 mr-2" />
                  Start Scan
                </Button>
              )}
            </div>
            
            <div className="flex items-end">
              <Button 
                onClick={() => {
                  loadAnalytics()
                  loadRecentNetworks()
                }}
                variant="outline"
                className="w-full"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Refresh
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Networks Found</CardTitle>
            <Wifi className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics?.total_networks || 0}</div>
            <p className="text-xs text-muted-foreground">
              +12% from last scan
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Clients</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics?.total_clients || 0}</div>
            <p className="text-xs text-muted-foreground">
              +5% from last scan
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Security Issues</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3</div>
            <p className="text-xs text-muted-foreground">
              Open networks detected
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Signal Quality</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">85%</div>
            <p className="text-xs text-muted-foreground">
              Average signal strength
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Signal Strength Over Time</CardTitle>
            <CardDescription>Real-time signal monitoring</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={signalData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="signal" stroke="#8884d8" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Encryption Distribution</CardTitle>
            <CardDescription>Security protocols in use</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={encryptionData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {encryptionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Channel Utilization and Recent Networks */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Channel Utilization</CardTitle>
            <CardDescription>Network distribution across channels</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={channelData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="channel" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="networks" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Recent Networks</CardTitle>
            <CardDescription>Latest discovered access points</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentNetworks.map((network) => (
                <div key={network.id} className="flex items-center justify-between p-3 bg-muted rounded-lg">
                  <div>
                    <div className="font-medium">{network.ssid || 'Hidden Network'}</div>
                    <div className="text-sm text-muted-foreground">{network.bssid}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-medium">{network.signal_strength} dBm</div>
                    <Badge variant={network.encryption === 'Open' ? 'destructive' : 'default'}>
                      {network.encryption}
                    </Badge>
                  </div>
                </div>
              ))}
              
              {recentNetworks.length === 0 && (
                <div className="text-center text-muted-foreground py-8">
                  No networks found. Start a scan to discover networks.
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

