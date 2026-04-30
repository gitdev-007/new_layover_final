import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import qrRoutes from './routes/qrRoutes.js';
import uploadRoutes from './routes/uploadRoutes.js';
import processRoutes from './routes/processRoutes.js';
import confirmationRoutes from './routes/confirmationRoutes.js';
import adminRoutes from './routes/adminRoutes.js';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;
const FRONTEND_URL = process.env.FRONTEND_URL || 'http://localhost:3000';

// CORS configuration
const corsOptions = {
  origin: FRONTEND_URL,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true
};

// Middleware
app.use(cors(corsOptions));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Root test route
app.get('/', (req, res) => {
  res.send('Backend is running');
});

// Routes
app.use('/api/qr', qrRoutes);
app.use('/api', uploadRoutes);
app.use('/api', processRoutes);
app.use('/api', confirmationRoutes);
app.use('/api/admin', adminRoutes);

// Log all registered routes for debugging
console.log('\n📋 Registered Routes:');
console.log('====================');
console.log('GET  /                    - Root test');
console.log('GET  /api/qr/test         - QR route test');
console.log('POST /api/qr/scan         - QR scan endpoint');
console.log('POST /api/upload-qr      - Upload QR file');
console.log('GET  /api/qr-status/:id   - Check QR status');
console.log('GET  /api/process-qr/:id  - Process QR (legacy)');
console.log('GET  /health              - Health check');
console.log('====================\n');

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ success: false, message: 'Endpoint not found' });
});

// Global error handler middleware
app.use((err, req, res, next) => {
  // Log error details to console
  console.error('Error:', err.message);
  console.error('Stack:', err.stack);
  
  // Determine status code
  const statusCode = err.statusCode || err.status || 500;
  
  // Return structured error response
  res.status(statusCode).json({
    success: false,
    message: err.message || 'Internal server error'
  });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
});
