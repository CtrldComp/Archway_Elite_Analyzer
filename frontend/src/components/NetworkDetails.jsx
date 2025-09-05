import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ArrowLeft, Wifi, Signal, Shield, Users, Clock, MapPin } from 'lucide-react'

export default function NetworkDetails() {
  const { id } = useParams()
  const [network, setNetwork] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadNetworkDetails()
  }, [id])

  const loadNetworkDetails = async () => {
    setLoading(true)
    try {
      const response = await fetch(`/api/wifi/networks/${id}`)
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setNetwork(data.network)
        }
      }
    } catch (error) {
      console.error('Error loading network details:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </div>
    )
  }

  if (!network) {
    return (
      <div className="p-6">
        <div className="text-center py-8">
          <Wifi className="w-12 h-12 mx-auto mb-4 opacity-50" />
          <p className="text-muted-foreground">Network not found</p>
          <Link to="/networks">
            <Button variant="outline" className="mt-4">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Networks
            </Button>
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link to="/networks">
            <Button variant="ghost" size="sm">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-foreground">
              {network.ssid || 'Hidden Network'}
            </h1>
            <p className="text-muted-foreground">{network.bssid}</p>
          </div>
        </div>
        
        <Badge variant={network.encryption === 'Open' ? 'destructive' : 'default'}>
          {network.encryption}
        </Badge>
      </div>

      {/* Network Information */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Wifi className="w-5 h-5" />
              <span>Network Information</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-muted-foreground">SSID</label>
                <p className="text-foreground">{network.ssid || 'Hidden'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">BSSID</label>
                <p className="text-foreground font-mono text-sm">{network.bssid}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Channel</label>
                <p className="text-foreground">{network.channel}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Frequency</label>
                <p className="text-foreground">{network.frequency} MHz</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Mode</label>
                <p className="text-foreground">{network.mode}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Vendor</label>
                <p className="text-foreground">{network.vendor}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Signal className="w-5 h-5" />
              <span>Signal Information</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-muted-foreground">Signal Strength</label>
                <p className="text-foreground font-mono">{network.signal_strength} dBm</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Quality</label>
                <p className="text-foreground">{network.quality}%</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">First Seen</label>
                <p className="text-foreground text-sm">
                  {new Date(network.first_seen).toLocaleString()}
                </p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">Last Seen</label>
                <p className="text-foreground text-sm">
                  {new Date(network.last_seen).toLocaleString()}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Security Information */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Shield className="w-5 h-5" />
            <span>Security Information</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="text-sm font-medium text-muted-foreground">Encryption</label>
              <p className="text-foreground">{network.encryption}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">Cipher</label>
              <p className="text-foreground">{network.cipher}</p>
            </div>
            <div>
              <label className="text-sm font-medium text-muted-foreground">Authentication</label>
              <p className="text-foreground">{network.authentication}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Connected Clients */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Users className="w-5 h-5" />
            <span>Connected Clients ({network.clients?.length || 0})</span>
          </CardTitle>
          <CardDescription>
            Devices currently connected to this network
          </CardDescription>
        </CardHeader>
        <CardContent>
          {network.clients && network.clients.length > 0 ? (
            <div className="space-y-3">
              {network.clients.map((client) => (
                <div key={client.id} className="flex items-center justify-between p-3 bg-muted rounded-lg">
                  <div>
                    <p className="font-mono text-sm">{client.mac_address}</p>
                    <p className="text-sm text-muted-foreground">{client.vendor}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium">{client.signal_strength} dBm</p>
                    <p className="text-xs text-muted-foreground">
                      {new Date(client.last_seen).toLocaleString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-muted-foreground">
              <Users className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p>No clients detected</p>
              <p className="text-sm">Start a monitor mode scan to detect connected clients</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

