# Authentication State Management with Supabase

This implementation provides global authentication state management using React Context and Supabase.

## Setup

1. **Wrap your app with AuthProvider** (typically in `_app.js` or `main.js`):

```jsx
import { AuthProvider } from './context/AuthContext'

function App() {
  return (
    <AuthProvider>
      <YourAppComponents />
    </AuthProvider>
  )
}
```

2. **Use the useAuth hook in any component**:

```jsx
import { useAuth } from './context/AuthContext'

function MyComponent() {
  const { user, loading, isAuthenticated, signIn, signUp, signOut } = useAuth()

  if (loading) return <div>Loading...</div>

  return (
    <div>
      {isAuthenticated ? (
        <div>Welcome, {user.email}!</div>
      ) : (
        <div>Please sign in</div>
      )}
    </div>
  )
}
```

## Available Properties and Methods

### Properties
- `user`: Current user object or null
- `session`: Current session object or null
- `loading`: Boolean indicating if auth state is loading
- `isAuthenticated`: Boolean indicating if user is logged in

### Methods
- `signIn(email, password)`: Sign in user
- `signUp(email, password)`: Sign up new user
- `signOut()`: Sign out current user

## Features

✅ **Automatic session detection** - Detects if user is logged in on app load
✅ **Session persistence** - Automatically persists and restores sessions
✅ **Real-time auth state changes** - Listens to all auth state changes
✅ **Global state management** - Access auth state anywhere in the app
✅ **Error handling** - Built-in error handling for all auth operations
✅ **Loading states** - Proper loading states during auth checks

## Usage Examples

### Protected Routes
```jsx
import { useAuth } from './context/AuthContext'
import { useRouter } from 'next/router'

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth()
  const router = useRouter()

  if (loading) return <div>Loading...</div>
  
  if (!isAuthenticated) {
    router.push('/auth')
    return null
  }

  return children
}
```

### Authentication Forms
```jsx
import { useAuth } from './context/AuthContext'

function LoginForm() {
  const { signIn } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    const { error } = await signIn(email, password)
    
    if (error) {
      console.error('Login failed:', error.message)
    } else {
      // User is now logged in (handled by AuthProvider)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button type="submit">Sign In</button>
    </form>
  )
}
```

## Environment Variables

Make sure your `.env.local` file contains:
```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```
