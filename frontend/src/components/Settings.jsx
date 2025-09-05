import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Switch } from '@/components/ui/switch'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Settings as SettingsIcon, Moon, Sun, Monitor, Wifi, Database } from 'lucide-react'
import { useTheme } from '@/components/theme-provider'

export default function Settings() {
  const { theme, setTheme } = useTheme()

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground">Settings</h1>
        <p className="text-muted-foreground">Configure Archway WiFi Analyzer</p>
      </div>

      {/* Appearance */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Monitor className="w-5 h-5" />
            <span>Appearance</span>
          </CardTitle>
          <CardDescription>Customize the look and feel of the application</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium">Theme</label>
              <p className="text-sm text-muted-foreground">Choose your preferred theme</p>
            </div>
            <Select value={theme} onValueChange={setTheme}>
              <SelectTrigger className="w-32">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="light">
                  <div className="flex items-center space-x-2">
                    <Sun className="w-4 h-4" />
                    <span>Light</span>
                  </div>
                </SelectItem>
                <SelectItem value="dark">
                  <div className="flex items-center space-x-2">
                    <Moon className="w-4 h-4" />
                    <span>Dark</span>
                  </div>
                </SelectItem>
                <SelectItem value="system">
                  <div className="flex items-center space-x-2">
                    <Monitor className="w-4 h-4" />
                    <span>System</span>
                  </div>
                </SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Scanning */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Wifi className="w-5 h-5" />
            <span>Scanning</span>
          </CardTitle>
          <CardDescription>Configure WiFi scanning behavior</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium">Auto-refresh</label>
              <p className="text-sm text-muted-foreground">Automatically refresh scan results</p>
            </div>
            <Switch />
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium">Monitor mode</label>
              <p className="text-sm text-muted-foreground">Enable advanced packet capture</p>
            </div>
            <Switch />
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium">Channel hopping</label>
              <p className="text-sm text-muted-foreground">Scan across all channels</p>
            </div>
            <Switch defaultChecked />
          </div>
        </CardContent>
      </Card>

      {/* Database */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Database className="w-5 h-5" />
            <span>Database</span>
          </CardTitle>
          <CardDescription>Manage scan data and history</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium">Store scan history</label>
              <p className="text-sm text-muted-foreground">Keep historical scan data</p>
            </div>
            <Switch defaultChecked />
          </div>
          
          <div className="flex items-center space-x-4">
            <Button variant="outline">
              Export Data
            </Button>
            <Button variant="outline">
              Clear History
            </Button>
            <Button variant="destructive">
              Reset Database
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* About */}
      <Card>
        <CardHeader>
          <CardTitle>About Archway</CardTitle>
          <CardDescription>Elite Analyzer by EVMG Technologies</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2 text-sm text-muted-foreground">
            <p><span className="font-semibold text-foreground">Developer:</span> EVMG Technologies</p>
            <p><span className="font-semibold text-foreground">Version:</span> 1.0.0</p>
            <p>Built with modern web technologies for comprehensive network analysis</p>
            <p>Features advanced scanning, spectrum analysis, and security assessment</p>
            <p className="text-xs opacity-75 mt-4">© 2025 EVMG Technologies. All rights reserved.</p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

