// Supabase Auth Client
// Initialize with your Supabase credentials

const SUPABASE_URL = 'https://your-project.supabase.co';
const SUPABASE_ANON_KEY = 'your-anon-key';

let supabaseClient = null;

// Initialize Supabase client
function initSupabase() {
  if (!supabaseClient && window.supabase) {
    supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
  }
  return supabaseClient;
}

// Sign Up
async function signUp(email, password) {
  const client = initSupabase();
  if (!client) throw new Error('Supabase not loaded');
  
  const { data, error } = await client.auth.signUp({
    email,
    password
  });
  
  if (error) throw error;
  return data;
}

// Login
async function login(email, password) {
  const client = initSupabase();
  if (!client) throw new Error('Supabase not loaded');
  
  const { data, error } = await client.auth.signInWithPassword({
    email,
    password
  });
  
  if (error) throw error;
  return data;
}

// Logout
async function logout() {
  const client = initSupabase();
  if (!client) throw new Error('Supabase not loaded');
  
  const { error } = await client.auth.signOut();
  if (error) throw error;
  
  localStorage.removeItem('user');
  window.location.href = 'auth.html';
}

// Get current session
async function getSession() {
  const client = initSupabase();
  if (!client) return null;
  
  const { data: { session } } = await client.auth.getSession();
  return session;
}

// Check if user is logged in
async function isLoggedIn() {
  const session = await getSession();
  return !!session;
}

// Listen to auth state changes
function onAuthStateChange(callback) {
  const client = initSupabase();
  if (!client) return;
  
  client.auth.onAuthStateChange((event, session) => {
    callback(event, session);
  });
}

// Export functions
window.auth = {
  signUp,
  login,
  logout,
  getSession,
  isLoggedIn,
  onAuthStateChange,
  initSupabase
};
