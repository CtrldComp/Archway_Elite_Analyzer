import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from '@/components/ui/toaster'
import { ThemeProvider } from '@/components/theme-provider'
import Sidebar from '@/components/Sidebar'
import Dashboard from '@/components/Dashboard'
import NetworkList from '@/components/NetworkList'
import NetworkDetails from '@/components/NetworkDetails'
import SpectrumAnalyzer from '@/components/SpectrumAnalyzer'
import ClientList from '@/components/ClientList'
import ScanHistory from '@/components/ScanHistory'
import Settings from '@/components/Settings'
import './App.css'

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [currentScan, setCurrentScan] = useState(null)
  const [scanStatus, setScanStatus] = useState({ scanning: false, networks_count: 0, clients_count: 0 })

  // Poll scan status
  useEffect(() => {
    const pollScanStatus = async () => {
      try {
        const response = await fetch('/api/wifi/scan/status')
        if (response.ok) {
          const data = await response.json()
          if (data.success) {
            setScanStatus(data)
          }
        }
      } catch (error) {
        console.error('Error polling scan status:', error)
      }
    }

    const interval = setInterval(pollScanStatus, 2000) // Poll every 2 seconds
    pollScanStatus() // Initial poll

    return () => clearInterval(interval)
  }, [])

  return (
    <ThemeProvider defaultTheme="dark" storageKey="archway-theme">
      <Router>
        <div className="flex h-screen bg-background">
          <Sidebar 
            open={sidebarOpen} 
            setOpen={setSidebarOpen}
            scanStatus={scanStatus}
          />
          
          <main className={`flex-1 transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-16'}`}>
            <div className="h-full overflow-auto">
              <Routes>
                <Route 
                  path="/" 
                  element={
                    <Dashboard 
                      scanStatus={scanStatus}
                      setScanStatus={setScanStatus}
                      currentScan={currentScan}
                      setCurrentScan={setCurrentScan}
                    />
                  } 
                />
                <Route 
                  path="/networks" 
                  element={<NetworkList scanStatus={scanStatus} />} 
                />
                <Route 
                  path="/networks/:id" 
                  element={<NetworkDetails />} 
                />
                <Route 
                  path="/spectrum" 
                  element={<SpectrumAnalyzer />} 
                />
                <Route 
                  path="/clients" 
                  element={<ClientList />} 
                />
                <Route 
                  path="/history" 
                  element={<ScanHistory />} 
                />
                <Route 
                  path="/settings" 
                  element={<Settings />} 
                />
              </Routes>
            </div>
          </main>
        </div>
        
        <Toaster />
      </Router>
    </ThemeProvider>
  )
}

export default App

