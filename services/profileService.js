// Profile service for handling user profiles
// Note: This file is designed for ES modules. For plain HTML + JavaScript,
// you should include the profile functions directly in your HTML script tags
// or load this file as a regular script (not type="module")

// For plain HTML usage, include this script after Supabase CDN:
// <script src="services/profileService.js"></script>
// Then use: profileService.getProfile(userId)

const profileService = {
  // Fetch user profile by user ID
  async getProfile(userId) {
    try {
      const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', userId)
        .single()

      if (error) {
        // If profile doesn't exist, return null
        if (error.code === 'PGRST116') {
          return { data: null, error: null }
        }
        throw error
      }

      return { data, error: null }
    } catch (error) {
      console.error('Error fetching profile:', error)
      return { data: null, error }
    }
  },

  // Create or update user profile
  async upsertProfile(profile) {
    try {
      const { data, error } = await supabase
        .from('profiles')
        .upsert(profile)
        .select()
        .single()

      if (error) throw error

      return { data, error: null }
    } catch (error) {
      console.error('Error upserting profile:', error)
      return { data: null, error }
    }
  },

  // Create profile for new user
  async createProfile(userId, userData = {}) {
    try {
      const profile = {
        id: userId,
        name: userData.name || userData.user_metadata?.name || '',
        email: userData.email || '',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        ...userData
      }

      const { data, error } = await supabase
        .from('profiles')
        .insert(profile)
        .select()
        .single()

      if (error) throw error

      return { data, error: null }
    } catch (error) {
      console.error('Error creating profile:', error)
      return { data: null, error }
    }
  },

  // Update user profile
  async updateProfile(userId, updates) {
    try {
      const { data, error } = await supabase
        .from('profiles')
        .update({
          ...updates,
          updated_at: new Date().toISOString()
        })
        .eq('id', userId)
        .select()
        .single()

      if (error) throw error

      return { data, error: null }
    } catch (error) {
      console.error('Error updating profile:', error)
      return { data: null, error }
    }
  }
}

// Make profileService available globally for plain HTML usage
if (typeof window !== 'undefined') {
  window.profileService = profileService
}
