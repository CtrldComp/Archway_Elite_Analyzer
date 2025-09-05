import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { 
  Wifi, 
  Search, 
  Filter, 
  ArrowUpDown, 
  Eye, 
  Shield, 
  ShieldAlert,
  Signal,
  Users,
  Clock
} from 'lucide-react'

export default function NetworkList({ scanStatus }) {
  const [networks, setNetworks] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [sortBy, setSortBy] = useState('last_seen')
  const [sortOrder, setSortOrder] = useState('desc')
  const [encryptionFilter, setEncryptionFilter] = useState('all')
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 20,
    total: 0,
    pages: 0
  })

  useEffect(() => {
    loadNetworks()
  }, [pagination.page, sortBy, sortOrder, encryptionFilter])

  const loadNetworks = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams({
        page: pagination.page.toString(),
        per_page: pagination.per_page.toString(),
        sort_by: sortBy,
        order: sortOrder
      })

      const response = await fetch(`/api/wifi/networks?${params}`)
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setNetworks(data.networks)
          setPagination(prev => ({
            ...prev,
            total: data.pagination.total,
            pages: data.pagination.pages
          }))
        }
      }
    } catch (error) {
      console.error('Error loading networks:', error)
    } finally {
      setLoading(false)
    }
  }

  const getSignalStrengthColor = (strength) => {
    if (strength >= -50) return 'text-green-500'
    if (strength >= -70) return 'text-yellow-500'
    return 'text-red-500'
  }

  const getSignalBars = (strength) => {
    if (strength >= -50) return 4
    if (strength >= -60) return 3
    if (strength >= -70) return 2
    return 1
  }

  const getEncryptionBadge = (encryption) => {
    switch (encryption) {
      case 'Open':
        return <Badge variant="destructive">Open</Badge>
      case 'WEP':
        return <Badge variant="secondary">WEP</Badge>
      case 'WPA':
        return <Badge variant="default">WPA</Badge>
      case 'WPA2':
        return <Badge variant="default">WPA2</Badge>
      case 'WPA3':
        return <Badge variant="default">WPA3</Badge>
      default:
        return <Badge variant="outline">{encryption}</Badge>
    }
  }

  const filteredNetworks = networks.filter(network => {
    const matchesSearch = network.ssid.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         network.bssid.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         network.vendor.toLowerCase().includes(searchTerm.toLowerCase())
    
    const matchesEncryption = encryptionFilter === 'all' || network.encryption === encryptionFilter
    
    return matchesSearch && matchesEncryption
  })

  const handleSort = (field) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(field)
      setSortOrder('desc')
    }
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">WiFi Networks</h1>
          <p className="text-muted-foreground">
            Discovered access points and their details
          </p>
        </div>
        
        <div className="flex items-center space-x-2">
          <Badge variant="outline" className="px-3 py-1">
            {filteredNetworks.length} networks
          </Badge>
          {scanStatus.scanning && (
            <Badge variant="default" className="px-3 py-1">
              <Signal className="w-3 h-3 mr-1 animate-pulse" />
              Scanning
            </Badge>
          )}
        </div>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Filter className="w-5 h-5" />
            <span>Filters & Search</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search networks..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            
            <Select value={encryptionFilter} onValueChange={setEncryptionFilter}>
              <SelectTrigger>
                <SelectValue placeholder="Filter by encryption" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Encryption Types</SelectItem>
                <SelectItem value="Open">Open Networks</SelectItem>
                <SelectItem value="WEP">WEP</SelectItem>
                <SelectItem value="WPA">WPA</SelectItem>
                <SelectItem value="WPA2">WPA2</SelectItem>
                <SelectItem value="WPA3">WPA3</SelectItem>
              </SelectContent>
            </Select>
            
            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger>
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="last_seen">Last Seen</SelectItem>
                <SelectItem value="signal_strength">Signal Strength</SelectItem>
                <SelectItem value="ssid">Network Name</SelectItem>
                <SelectItem value="channel">Channel</SelectItem>
                <SelectItem value="encryption">Encryption</SelectItem>
              </SelectContent>
            </Select>
            
            <Button onClick={loadNetworks} variant="outline">
              <ArrowUpDown className="w-4 h-4 mr-2" />
              Refresh
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Networks Table */}
      <Card>
        <CardHeader>
          <CardTitle>Network Details</CardTitle>
          <CardDescription>
            Comprehensive information about discovered WiFi networks
          </CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead 
                      className="cursor-pointer hover:bg-muted"
                      onClick={() => handleSort('ssid')}
                    >
                      <div className="flex items-center space-x-1">
                        <Wifi className="w-4 h-4" />
                        <span>Network Name</span>
                        <ArrowUpDown className="w-3 h-3" />
                      </div>
                    </TableHead>
                    <TableHead>BSSID</TableHead>
                    <TableHead 
                      className="cursor-pointer hover:bg-muted"
                      onClick={() => handleSort('signal_strength')}
                    >
                      <div className="flex items-center space-x-1">
                        <Signal className="w-4 h-4" />
                        <span>Signal</span>
                        <ArrowUpDown className="w-3 h-3" />
                      </div>
                    </TableHead>
                    <TableHead 
                      className="cursor-pointer hover:bg-muted"
                      onClick={() => handleSort('channel')}
                    >
                      Channel
                    </TableHead>
                    <TableHead 
                      className="cursor-pointer hover:bg-muted"
                      onClick={() => handleSort('encryption')}
                    >
                      <div className="flex items-center space-x-1">
                        <Shield className="w-4 h-4" />
                        <span>Security</span>
                        <ArrowUpDown className="w-3 h-3" />
                      </div>
                    </TableHead>
                    <TableHead>Vendor</TableHead>
                    <TableHead>
                      <div className="flex items-center space-x-1">
                        <Users className="w-4 h-4" />
                        <span>Clients</span>
                      </div>
                    </TableHead>
                    <TableHead 
                      className="cursor-pointer hover:bg-muted"
                      onClick={() => handleSort('last_seen')}
                    >
                      <div className="flex items-center space-x-1">
                        <Clock className="w-4 h-4" />
                        <span>Last Seen</span>
                        <ArrowUpDown className="w-3 h-3" />
                      </div>
                    </TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredNetworks.map((network) => (
                    <TableRow key={network.id} className="hover:bg-muted/50">
                      <TableCell>
                        <div>
                          <div className="font-medium">
                            {network.ssid || <span className="text-muted-foreground italic">Hidden Network</span>}
                          </div>
                          {network.encryption === 'Open' && (
                            <div className="flex items-center space-x-1 text-red-500 text-xs">
                              <ShieldAlert className="w-3 h-3" />
                              <span>Unsecured</span>
                            </div>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <code className="text-xs bg-muted px-2 py-1 rounded">
                          {network.bssid}
                        </code>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center space-x-2">
                          <div className="flex space-x-1">
                            {[...Array(4)].map((_, i) => (
                              <div
                                key={i}
                                className={`w-1 h-3 rounded-full ${
                                  i < getSignalBars(network.signal_strength)
                                    ? getSignalStrengthColor(network.signal_strength)
                                    : 'bg-muted'
                                }`}
                                style={{
                                  backgroundColor: i < getSignalBars(network.signal_strength) 
                                    ? 'currentColor' 
                                    : undefined
                                }}
                              />
                            ))}
                          </div>
                          <span className={`text-sm font-mono ${getSignalStrengthColor(network.signal_strength)}`}>
                            {network.signal_strength} dBm
                          </span>
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline">
                          {network.channel}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        {getEncryptionBadge(network.encryption)}
                      </TableCell>
                      <TableCell>
                        <span className="text-sm text-muted-foreground">
                          {network.vendor}
                        </span>
                      </TableCell>
                      <TableCell>
                        <Badge variant="secondary">
                          {network.client_count}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <span className="text-sm text-muted-foreground">
                          {new Date(network.last_seen).toLocaleString()}
                        </span>
                      </TableCell>
                      <TableCell>
                        <Link to={`/networks/${network.id}`}>
                          <Button variant="ghost" size="sm">
                            <Eye className="w-4 h-4" />
                          </Button>
                        </Link>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
              
              {filteredNetworks.length === 0 && (
                <div className="text-center py-8 text-muted-foreground">
                  {networks.length === 0 ? (
                    <div>
                      <Wifi className="w-12 h-12 mx-auto mb-4 opacity-50" />
                      <p>No networks discovered yet.</p>
                      <p className="text-sm">Start a scan to discover WiFi networks.</p>
                    </div>
                  ) : (
                    <div>
                      <Search className="w-12 h-12 mx-auto mb-4 opacity-50" />
                      <p>No networks match your search criteria.</p>
                      <p className="text-sm">Try adjusting your filters or search terms.</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Pagination */}
      {pagination.pages > 1 && (
        <div className="flex items-center justify-between">
          <div className="text-sm text-muted-foreground">
            Showing {((pagination.page - 1) * pagination.per_page) + 1} to{' '}
            {Math.min(pagination.page * pagination.per_page, pagination.total)} of{' '}
            {pagination.total} networks
          </div>
          
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setPagination(prev => ({ ...prev, page: prev.page - 1 }))}
              disabled={pagination.page <= 1}
            >
              Previous
            </Button>
            
            <div className="flex items-center space-x-1">
              {[...Array(Math.min(5, pagination.pages))].map((_, i) => {
                const page = i + 1
                return (
                  <Button
                    key={page}
                    variant={pagination.page === page ? "default" : "outline"}
                    size="sm"
                    onClick={() => setPagination(prev => ({ ...prev, page }))}
                  >
                    {page}
                  </Button>
                )
              })}
            </div>
            
            <Button
              variant="outline"
              size="sm"
              onClick={() => setPagination(prev => ({ ...prev, page: prev.page + 1 }))}
              disabled={pagination.page >= pagination.pages}
            >
              Next
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}

