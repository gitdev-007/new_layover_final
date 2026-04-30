import { Router } from 'express';
import { processQR, verifyQR } from '../services/qrService.js';

const router = Router();

// POST /api/qr/process - Process QR code
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
