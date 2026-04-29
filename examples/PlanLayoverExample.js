import React from 'react'
import { AuthProvider } from '../context/AuthContext'
import PlanLayoverButton from '../components/PlanLayoverButton'

// Example of how to use PlanLayoverButton in your app
const AppExample = () => {
  return (
    <AuthProvider>
      <div className="min-h-screen bg-surface text-white p-8">
        <h1 className="text-3xl font-bold mb-8">LayoverX</h1>
        
        {/* Navigation example */}
        <nav className="flex items-center gap-6 mb-12">
          <a href="#" className="text-secondary hover:text-white">Home</a>
          <a href="#" className="text-secondary hover:text-white">About</a>
          
          {/* Plan Layover button with conditional auth logic */}
          <PlanLayoverButton />
        </nav>

        {/* Hero section example */}
        <section className="text-center">
          <h2 className="text-4xl font-bold mb-4">Your Layover. Your Experience.</h2>
          <p className="text-secondary/80 mb-8">Explore curated airport-near experiences</p>
          
          {/* Another instance with custom styling */}
          <PlanLayoverButton 
            className="px-8 py-4 text-lg"
            children="Start Planning"
          />
        </section>
      </div>
    </AuthProvider>
  )
}

export default AppExample
