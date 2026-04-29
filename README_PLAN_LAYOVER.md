# Plan Layover Button Implementation

This implementation provides a "Plan Layover" button with conditional authentication logic that seamlessly integrates with the Supabase authentication system.

## Features

✅ **Conditional Logic**: 
- If user is NOT logged in → opens auth modal
- If user is logged in → redirects to main app page

✅ **Clean Implementation**: 
- Single component with clear conditional logic
- Loading states during auth checks
- Error handling and user feedback

✅ **Reusable**: 
- Can be used anywhere in the app
- Customizable styling and text
- Consistent behavior across all instances

## Components

### 1. PlanLayoverButton (`/components/PlanLayoverButton.js`)

The main component that handles the conditional logic:

```jsx
import PlanLayoverButton from './components/PlanLayoverButton'

// Basic usage
<PlanLayoverButton />

// Custom styling and text
<PlanLayoverButton 
  className="px-8 py-4 text-lg"
  children="Start Planning"
/>
```

**Props:**
- `className` (optional): Additional CSS classes for styling
- `children` (optional): Button text (defaults to "Plan Layover")

**Logic Flow:**
1. Check authentication state using `useAuth()`
2. If loading → show loading spinner
3. If NOT authenticated → open auth modal
4. If authenticated → redirect to `/plan.html`

### 2. AuthModal (`/components/AuthModal.js`)

Modal component for login/signup that appears when unauthenticated users click the button:

**Features:**
- Toggle between login and signup
- Form validation and error handling
- Success messages and auto-close
- Loading states during auth operations
- Clean, accessible UI

## Integration

### Step 1: Wrap your app with AuthProvider

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

### Step 2: Use PlanLayoverButton anywhere

```jsx
import PlanLayoverButton from './components/PlanLayoverButton'

function Navigation() {
  return (
    <nav>
      <a href="/">Home</a>
      <a href="/about">About</a>
      <PlanLayoverButton />
    </nav>
  )
}
```

## User Experience Flow

### Unauthenticated User:
1. Clicks "Plan Layover" button
2. Auth modal opens with login/signup form
3. User completes authentication
4. Modal closes and user is redirected to `/plan.html`

### Authenticated User:
1. Clicks "Plan Layover" button
2. Immediately redirected to `/plan.html`
3. No modal interruption

## Technical Details

### Authentication State Management
- Uses `useAuth()` hook from AuthContext
- Leverages `isAuthenticated` boolean for conditional logic
- Handles loading states during auth checks

### Error Handling
- Network errors during auth operations
- Invalid credentials feedback
- Form validation errors
- Unexpected error states

### Accessibility
- Semantic HTML structure
- ARIA labels and roles
- Keyboard navigation support
- Focus management in modal

## Styling

The components use Tailwind CSS classes that match your existing design system:

- **Primary button**: `bg-primary-container text-on-primary-container`
- **Modal**: `bg-surface border border-white/10 rounded-[28px]`
- **Loading states**: Animated spinners and disabled states
- **Responsive**: Works on all screen sizes

## Customization

### Button Styling
```jsx
<PlanLayoverButton 
  className="custom-button-styles"
  children="Custom Button Text"
/>
```

### Modal Customization
The AuthModal can be customized by modifying the component in `/components/AuthModal.js`:
- Colors and spacing
- Form fields and validation
- Success/error message styling
- Animation and transitions

## Dependencies

- React (for component structure)
- AuthContext (for authentication state)
- Supabase client (for auth operations)
- Tailwind CSS (for styling)

## File Structure

```
/components/
  ├── AuthModal.js          # Login/signup modal
  └── PlanLayoverButton.js  # Main button component
/context/
  └── AuthContext.js        # Authentication state management
/lib/
  └── supabaseClient.js     # Supabase client configuration
/examples/
  └── PlanLayoverExample.js # Usage example
```
