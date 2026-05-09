import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import Razorpay from 'razorpay';
import crypto from 'crypto';
import qrRoutes from './routes/qrRoutes.js';
import uploadRoutes from './routes/uploadRoutes.js';
import processRoutes from './routes/processRoutes.js';
import confirmationRoutes from './routes/confirmationRoutes.js';
import adminRoutes from './routes/adminRoutes.js';

// Load environment variables
dotenv.config();

const app = express();

const razorpay = new Razorpay({
    key_id: process.env.RAZORPAY_KEY_ID,
    key_secret: process.env.RAZORPAY_KEY_SECRET,
});

// CORS configuration - Allow all origins
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

app.options('*', cors());

// Middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Root test route
app.get('/', (req, res) => {
  res.send('Backend is running');
});

// Razorpay Routes
app.post('/create-order', async (req, res) => {
    try {
        const options = {
            amount: req.body.amount * 100, // amount in smallest currency unit
            currency: "INR",
            receipt: "receipt_order_" + Date.now(),
        };
        const order = await razorpay.orders.create(options);
        res.json(order);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/verify-payment', (req, res) => {
    const { razorpay_order_id, razorpay_payment_id, razorpay_signature } = req.body;
    const sign = razorpay_order_id + "|" + razorpay_payment_id;
    const expectedSign = crypto
        .createHmac("sha256", process.env.RAZORPAY_KEY_SECRET)
        .update(sign.toString())
        .digest("hex");

    if (razorpay_signature === expectedSign) {
        res.json({ success: true });
    } else {
        res.status(400).json({ success: false, message: "Invalid signature" });
    }
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
console.log('GET  /api/qr-status       - Check QR status (query: id or url)');
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

// ================= ERROR HANDLER =================
app.use((err, req, res, next) => {
  console.error('Error:', err.message);
  console.error('Stack:', err.stack);

  const statusCode = err.statusCode || err.status || 500;

  res.status(statusCode).json({
    success: false,
    message: err.message || 'Internal server error'
  });
});

// ================= PORT CONFIG =================
const PORT = process.env.PORT || 5000;

// ================= START SERVER =================
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Health check: https://layoverbackend.onrender.com/health`);
});
