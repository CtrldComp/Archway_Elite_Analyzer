import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { useTheme } from '@/components/theme-provider'
import { 
  Wifi, 
  BarChart3, 
  Users, 
  Radio, 
  History, 
  Settings, 
  ChevronLeft, 
  ChevronRight,
  Activity,
  Shield,
  Zap
} from 'lucide-react'

const navigation = [
  { name: 'Dashboard', href: '/', icon: BarChart3 },
  { name: 'Networks', href: '/networks', icon: Wifi },
  { name: 'Spectrum', href: '/spectrum', icon: Radio },
  { name: 'Clients', href: '/clients', icon: Users },
  { name: 'History', href: '/history', icon: History },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export default function Sidebar({ open, setOpen, scanStatus }) {
  const location = useLocation()
  const { theme } = useTheme()
  
  // Determine which logo to use based on theme
  const getLogoSrc = () => {
    if (theme === 'dark') {
      return '/archway-logo-light.png' // Use light logo for dark theme
    } else if (theme === 'light') {
      return '/archway-logo-dark.png' // Use dark logo for light theme
    } else {
      // System theme - detect based on system preference
      const isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches
      return isDarkMode ? '/archway-logo-light.png' : '/archway-logo-dark.png'
    }
  }

  return (
    <div className={cn(
      "fixed left-0 top-0 z-40 h-screen bg-card border-r border-border transition-all duration-300",
      open ? "w-64" : "w-16"
    )}>
      <div className="flex h-full flex-col">
        {/* Header */}
        <div className="flex h-16 items-center justify-between px-4 border-b border-border">
          {open && (
            <div className="flex items-center space-x-2">
              <img 
                src={getLogoSrc()} 
                alt="Archway Elite Analyzer" 
                className="w-8 h-8 object-contain"
              />
              <div>
                <h1 className="text-lg font-bold text-foreground">Archway</h1>
                <p className="text-xs text-muted-foreground">Elite Analyzer</p>
                <p className="text-xs text-muted-foreground opacity-75">by EVMG Technologies</p>
              </div>
            </div>
          )}
          
          {!open && (
            <div className="flex items-center justify-center w-full">
              <img 
                src={getLogoSrc()} 
                alt="Archway Elite Analyzer" 
                className="w-8 h-8 object-contain"
              />
            </div>
          )}
          
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setOpen(!open)}
            className="h-8 w-8 p-0"
          >
            {open ? (
              <ChevronLeft className="h-4 w-4" />
            ) : (
              <ChevronRight className="h-4 w-4" />
            )}
          </Button>
        </div>

        {/* Scan Status */}
        {open && (
          <div className="p-4 border-b border-border">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-foreground">Scan Status</span>
              {scanStatus.scanning && (
                <div className="flex items-center space-x-1">
                  <Activity className="w-3 h-3 text-green-500 animate-pulse" />
                  <span className="text-xs text-green-500">Active</span>
                </div>
              )}
            </div>
            
            <div className="grid grid-cols-2 gap-2">
              <div className="bg-muted rounded-lg p-2">
                <div className="text-xs text-muted-foreground">Networks</div>
                <div className="text-lg font-bold text-foreground">
                  {scanStatus.networks_count || 0}
                </div>
              </div>
              <div className="bg-muted rounded-lg p-2">
                <div className="text-xs text-muted-foreground">Clients</div>
                <div className="text-lg font-bold text-foreground">
                  {scanStatus.clients_count || 0}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Navigation */}
        <nav className="flex-1 px-2 py-4 space-y-1">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href
            const Icon = item.icon
            
            return (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  "flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors",
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:text-foreground hover:bg-muted"
                )}
              >
                <Icon className={cn("flex-shrink-0", open ? "mr-3 h-5 w-5" : "h-5 w-5")} />
                {open && (
                  <span className="truncate">{item.name}</span>
                )}
                
                {/* Show badges for certain items */}
                {open && item.name === 'Networks' && scanStatus.networks_count > 0 && (
                  <Badge variant="secondary" className="ml-auto">
                    {scanStatus.networks_count}
                  </Badge>
                )}
                {open && item.name === 'Clients' && scanStatus.clients_count > 0 && (
                  <Badge variant="secondary" className="ml-auto">
                    {scanStatus.clients_count}
                  </Badge>
                )}
              </Link>
            )
          })}
        </nav>

        {/* Footer */}
        {open && (
          <div className="p-4 border-t border-border">
            <div className="flex items-center space-x-2 text-xs text-muted-foreground">
              <Zap className="w-3 h-3" />
              <span>Elite Network Analysis</span>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

