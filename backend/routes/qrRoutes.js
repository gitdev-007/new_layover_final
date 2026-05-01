import { Router } from 'express';
import multer from 'multer';
import { processQR, verifyQR } from '../services/qrService.js';

const router = Router();

// Configure multer with memory storage
const storage = multer.memoryStorage();
const upload = multer({ storage });

// GET /test - Test route to verify QR router is working
router.get('/test', (req, res) => {
  res.json({ success: true, message: 'QR route working' });
});

// POST /scan - QR scan endpoint with file upload
router.post('/scan', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ 
        success: false, 
        error: 'Image file is required' 
      });
    }

    // Convert buffer to base64 for QR processing
    const imageData = `data:${req.file.mimetype};base64,${req.file.buffer.toString('base64')}`;
    
    const result = await processQR(imageData);
    res.json({ 
      success: true, 
      message: 'File received and processed successfully',
      data: result 
    });
  } catch (error) {
    console.error('QR scan error:', error);
    res.status(500).json({ 
      success: false, 
      error: error.message || 'Failed to process QR code' 
    });
  }
});

// GET /process - Test route (for debugging)
router.get('/process', (req, res) => {
  res.json({ 
    success: true, 
    message: 'QR process endpoint ready (POST to scan image)',
    method: 'POST',
    body: { imageData: 'base64-encoded-image' }
  });
});

// POST /process - Main QR processing endpoint
router.post('/process', async (req, res) => {
  try {
    const { imageData } = req.body;
    
    if (!imageData) {
      return res.status(400).json({ error: 'Image data is required' });
    }
    
    const result = await processQR(imageData);
    res.json(result);
  } catch (error) {
    console.error('QR processing error:', error);
    res.status(500).json({ error: 'Failed to process QR code' });
  }
});

// POST /api/qr/verify - Verify QR data
router.post('/verify', async (req, res) => {
  try {
    const { qrData } = req.body;
    
    if (!qrData) {
      return res.status(400).json({ error: 'QR data is required' });
    }
    
    const result = await verifyQR(qrData);
    res.json(result);
  } catch (error) {
    console.error('QR verification error:', error);
    res.status(500).json({ error: 'Failed to verify QR code' });
  }
});

export default router;
