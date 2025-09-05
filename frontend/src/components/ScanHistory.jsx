import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { History, Clock, Wifi, Users } from 'lucide-react'

export default function ScanHistory() {
  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Scan History</h1>
          <p className="text-muted-foreground">Previous WiFi scanning sessions</p>
        </div>
        
        <Badge variant="outline" className="px-3 py-1">
          <History className="w-3 h-3 mr-1" />
          0 sessions
        </Badge>
      </div>

      {/* History List */}
      <Card>
        <CardHeader>
          <CardTitle>Scan Sessions</CardTitle>
          <CardDescription>Historical record of WiFi scanning activities</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-96 flex items-center justify-center">
            <div className="text-center text-muted-foreground">
              <History className="w-16 h-16 mx-auto mb-4 opacity-50" />
              <p className="text-lg font-medium">No Scan History</p>
              <p>Start your first WiFi scan to see history here</p>
              <p className="text-sm mt-2">All scan sessions will be recorded and available for review</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

