import { useState } from 'react'
import ResidentSelector from './components/ResidentSelector'
import PaymentHistory from './components/PaymentHistory'
import { Building2, DollarSign } from 'lucide-react'

function App() {
  const [selectedResident, setSelectedResident] = useState(null)

  const handleResidentSelect = (resident) => {
    setSelectedResident(resident)
  }

  const handleBackToSelection = () => {
    setSelectedResident(null)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <Building2 className="w-8 h-8 text-blue-600" />
                <DollarSign className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Halya Payment System</h1>
                <p className="text-sm text-gray-500">Security Guard Fee Collection</p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500">Total Residents: 147</div>
              <div className="text-sm text-gray-500">Total Payments: 1,540</div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="py-8">
        {selectedResident ? (
          <PaymentHistory 
            resident={selectedResident} 
            onBack={handleBackToSelection} 
          />
        ) : (
          <ResidentSelector onResidentSelect={handleResidentSelect} />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="text-center text-sm text-gray-500">
            <p>© 2025 Halya Payment System. All rights reserved.</p>
            <p className="mt-1">Powered by Supabase & React</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App


