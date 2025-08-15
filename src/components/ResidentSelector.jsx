import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { Search, Home, MapPin } from 'lucide-react'

export default function ResidentSelector({ onResidentSelect }) {
  const [alleys, setAlleys] = useState([])
  const [selectedAlley, setSelectedAlley] = useState('')
  const [residents, setResidents] = useState([])
  const [loading, setLoading] = useState(false)

  // Fetch unique alleys
  useEffect(() => {
    async function fetchAlleys() {
      const { data, error } = await supabase
        .from('residents')
        .select('alley')
        .order('alley')
      
      if (error) {
        console.error('Error fetching alleys:', error)
        return
      }

      const uniqueAlleys = [...new Set(data.map(r => r.alley))].filter(Boolean)
      setAlleys(uniqueAlleys)
    }

    fetchAlleys()
  }, [])

  // Fetch residents when alley is selected
  useEffect(() => {
    if (!selectedAlley) {
      setResidents([])
      return
    }

    async function fetchResidents() {
      setLoading(true)
      const { data, error } = await supabase
        .from('residents')
        .select('*')
        .eq('alley', selectedAlley)
        .order('house_number')
      
      if (error) {
        console.error('Error fetching residents:', error)
        setLoading(false)
        return
      }

      setResidents(data)
      setLoading(false)
    }

    fetchResidents()
  }, [selectedAlley])

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
          <MapPin className="w-6 h-6 text-blue-600" />
          Select Resident
        </h2>

        {/* Alley Selection */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Choose Alley:
          </label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {alleys.map((alley) => (
              <button
                key={alley}
                onClick={() => setSelectedAlley(alley)}
                className={`p-3 rounded-lg border-2 transition-colors ${
                  selectedAlley === alley
                    ? 'border-blue-500 bg-blue-50 text-blue-700'
                    : 'border-gray-200 hover:border-gray-300 text-gray-700'
                }`}
              >
                <div className="font-semibold">Alley {alley}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Residents List */}
        {selectedAlley && (
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <Home className="w-5 h-5 text-green-600" />
              Houses in Alley {selectedAlley}
            </h3>
            
            {loading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-2 text-gray-600">Loading residents...</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {residents.map((resident) => (
                  <button
                    key={resident.resident_id}
                    onClick={() => onResidentSelect(resident)}
                    className="p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors text-left"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-bold text-blue-600">
                        {resident.resident_id}
                      </span>
                      <span className="text-sm text-gray-500">
                        House {resident.house_number}
                      </span>
                    </div>
                    <div className="text-sm text-gray-700 line-clamp-2">
                      {resident.resident_name}
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        )}

        {!selectedAlley && (
          <div className="text-center py-12 text-gray-500">
            <Search className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>Select an alley to view residents</p>
          </div>
        )}
      </div>
    </div>
  )
}


