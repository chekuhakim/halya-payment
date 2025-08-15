import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { ArrowLeft, DollarSign, Calendar, FileText, TrendingUp } from 'lucide-react'

export default function PaymentHistory({ resident, onBack }) {
  const [payments, setPayments] = useState([])
  const [loading, setLoading] = useState(false)
  const [summary, setSummary] = useState(null)

  useEffect(() => {
    if (!resident) return

    async function fetchPayments() {
      setLoading(true)
      
      // Fetch payments for this resident
      const { data: paymentsData, error: paymentsError } = await supabase
        .from('payments')
        .select('*')
        .eq('resident_id', resident.resident_id)
        .order('year', { ascending: false })
        .order('description')
      
      if (paymentsError) {
        console.error('Error fetching payments:', paymentsError)
        setLoading(false)
        return
      }

      setPayments(paymentsData)

      // Calculate summary
      const totalAmount = paymentsData.reduce((sum, payment) => sum + parseFloat(payment.amount), 0)
      const totalPayments = paymentsData.length
      const avgAmount = totalPayments > 0 ? totalAmount / totalPayments : 0

      setSummary({
        totalAmount,
        totalPayments,
        avgAmount
      })

      setLoading(false)
    }

    fetchPayments()
  }, [resident])

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-MY', {
      style: 'currency',
      currency: 'MYR'
    }).format(amount)
  }

  const getPaymentTypeColor = (description) => {
    if (description.includes('Membership')) return 'bg-blue-100 text-blue-800'
    if (description.includes('Annual')) return 'bg-green-100 text-green-800'
    if (description.includes('Guard')) return 'bg-purple-100 text-purple-800'
    if (description.includes('Excess')) return 'bg-orange-100 text-orange-800'
    return 'bg-gray-100 text-gray-800'
  }

  if (!resident) return null

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-blue-600 hover:text-blue-800 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            Back to Selection
          </button>
        </div>

        {/* Resident Info */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 mb-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-2">
            {resident.resident_name}
          </h2>
          <div className="flex items-center gap-4 text-gray-600">
            <span className="flex items-center gap-1">
              <FileText className="w-4 h-4" />
              {resident.resident_id}
            </span>
            <span className="flex items-center gap-1">
              <Calendar className="w-4 h-4" />
              Alley {resident.alley}, House {resident.house_number}
            </span>
          </div>
        </div>

        {/* Summary Cards */}
        {summary && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <DollarSign className="w-5 h-5 text-green-600" />
                <span className="text-sm font-medium text-green-700">Total Paid</span>
              </div>
              <div className="text-2xl font-bold text-green-800">
                {formatCurrency(summary.totalAmount)}
              </div>
            </div>
            
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <FileText className="w-5 h-5 text-blue-600" />
                <span className="text-sm font-medium text-blue-700">Total Payments</span>
              </div>
              <div className="text-2xl font-bold text-blue-800">
                {summary.totalPayments}
              </div>
            </div>
            
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="w-5 h-5 text-purple-600" />
                <span className="text-sm font-medium text-purple-700">Average Payment</span>
              </div>
              <div className="text-2xl font-bold text-purple-800">
                {formatCurrency(summary.avgAmount)}
              </div>
            </div>
          </div>
        )}

        {/* Payments List */}
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Payment History</h3>
          
          {loading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-2 text-gray-600">Loading payments...</p>
            </div>
          ) : payments.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <DollarSign className="w-12 h-12 mx-auto mb-4 text-gray-300" />
              <p>No payments found for this resident</p>
            </div>
          ) : (
            <div className="space-y-3">
              {payments.map((payment) => (
                <div
                  key={payment.id}
                  className="border border-gray-200 rounded-lg p-4 hover:border-gray-300 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPaymentTypeColor(payment.description)}`}>
                          {payment.description}
                        </span>
                        {payment.year && (
                          <span className="text-sm text-gray-500">
                            {payment.year}
                          </span>
                        )}
                      </div>
                      <div className="text-sm text-gray-600">
                        {payment.sheet_name}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold text-green-600">
                        {formatCurrency(payment.amount)}
                      </div>
                      {payment.payment_date && (
                        <div className="text-sm text-gray-500">
                          {new Date(payment.payment_date).toLocaleDateString()}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}


