import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Users, Smartphone, Laptop, Wifi } from 'lucide-react'

export default function ClientList() {
  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">WiFi Clients</h1>
          <p className="text-muted-foreground">Connected devices and client analysis</p>
        </div>
        
        <Badge variant="outline" className="px-3 py-1">
          <Users className="w-3 h-3 mr-1" />
          0 clients
        </Badge>
      </div>

      {/* Client List */}
      <Card>
        <CardHeader>
          <CardTitle>Discovered Clients</CardTitle>
          <CardDescription>Devices detected in the WiFi environment</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-96 flex items-center justify-center">
            <div className="text-center text-muted-foreground">
              <Users className="w-16 h-16 mx-auto mb-4 opacity-50" />
              <p className="text-lg font-medium">No Clients Detected</p>
              <p>Start a monitor mode scan to detect WiFi clients</p>
              <p className="text-sm mt-2">Client detection requires monitor mode capabilities</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

