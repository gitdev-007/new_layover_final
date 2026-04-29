import React, { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import AuthModal from './AuthModal'

const PlanLayoverButton = ({ className = '', children = 'Plan Layover' }) => {
  const { isAuthenticated, loading } = useAuth()
  const [showAuthModal, setShowAuthModal] = useState(false)

  const handlePlanLayoverClick = () => {
    // Clean conditional logic
    if (!isAuthenticated) {
      // User is NOT logged in → open auth modal
      setShowAuthModal(true)
    } else {
      // User is logged in → redirect to main app page
      window.location.href = '/plan.html'
    }
  }

  const handleCloseAuthModal = () => {
    setShowAuthModal(false)
  }

  // Disable button while checking auth state
  const isDisabled = loading

  return (
    <>
      <button
        onClick={handlePlanLayoverClick}
        disabled={isDisabled}
        className={`bg-primary-container text-on-primary-container px-6 py-2.5 rounded-full font-label-md active:scale-95 duration-200 disabled:opacity-50 disabled:cursor-not-allowed ${className}`}
      >
        {loading ? (
          <span className="flex items-center gap-2">
            <span className="material-symbols-outlined animate-spin text-sm">refresh</span>
            Checking...
          </span>
        ) : (
          children
        )}
      </button>

      <AuthModal 
        isOpen={showAuthModal} 
        onClose={handleCloseAuthModal}
      />
    </>
  )
}

export default PlanLayoverButton
