import { Router } from 'express';
import multer from 'multer';
import sharp from 'sharp';
import { MultiFormatReader, BarcodeFormat, DecodeHintType, RGBLuminanceSource, BinaryBitmap, HybridBinarizer } from '@zxing/library';
import { v4 as uuidv4 } from 'uuid'; // Assuming uuid is available in the project

const router = Router();

// Configure multer with memory storage
const storage = multer.memoryStorage();
const upload = multer({ storage });

// Helper to simulate rate limiting
const recentRequests = new Set();
const rateLimit = (ip) => {
    if (recentRequests.has(ip)) return false;
    recentRequests.add(ip);
    setTimeout(() => recentRequests.delete(ip), 5000); // 5s window
    return true;
};

// ... (existing helper scanQRFromBuffer) ...

// Group QR Processing Endpoint
router.post('/group-scan', async (req, res) => {
    const ip = req.ip;
    if (!rateLimit(ip)) return res.status(429).json({ success: false, error: 'Too many requests' });

    const { passenger_count, qr_codes } = req.body;

    if (!passenger_count || !Array.isArray(qr_codes) || qr_codes.length !== passenger_count) {
        return res.status(400).json({ success: false, error: 'Invalid passenger count or QR codes mismatch' });
    }

    const booking_id = uuidv4();
    const results = [];
    let validCount = 0;

    for (let i = 0; i < qr_codes.length; i++) {
        // Base64 to Buffer
        const buffer = Buffer.from(qr_codes[i].split(',')[1], 'base64');
        const qrResult = await scanQRFromBuffer(buffer);

        if (qrResult) {
            validCount++;
            results.push({ index: i + 1, status: 'valid', data: qrResult.text });
        } else {
            results.push({ index: i + 1, status: 'invalid' });
        }
    }

    res.json({
        booking_id,
        total_passengers: passenger_count,
        valid_passengers: validCount,
        invalid_passengers: passenger_count - validCount,
        passengers: results
    });
});

// ... (keep existing endpoints) ...


// Helper function to scan QR code from image buffer
async function scanQRFromBuffer(buffer) {
  try {
    // Convert image to raw RGBA pixels using sharp
    const { data, info } = await sharp(buffer)
      .raw()
      .ensureAlpha()
      .resize(800, 800, { fit: 'inside', withoutEnlargement: false })
      .toBuffer({ resolveWithObject: true });

    const { width, height } = info;
    
    // Convert RGBA to luminance (grayscale)
    const luminances = new Uint8ClampedArray(width * height);
    for (let i = 0; i < width * height; i++) {
      const r = data[i * 4];
      const g = data[i * 4 + 1];
      const b = data[i * 4 + 2];
      // Standard luminance formula
      luminances[i] = Math.round(0.299 * r + 0.587 * g + 0.114 * b);
    }

    // Create luminance source and binary bitmap for ZXing
    const luminanceSource = new RGBLuminanceSource(luminances, width, height);
    const binaryBitmap = new BinaryBitmap(new HybridBinarizer(luminanceSource));

    // Configure hints for QR code detection
    const hints = new Map();
    hints.set(DecodeHintType.POSSIBLE_FORMATS, [BarcodeFormat.QR_CODE]);
    hints.set(DecodeHintType.TRY_HARDER, true);

    // Create reader and decode
    const reader = new MultiFormatReader();
    reader.setHints(hints);
    
    const result = reader.decode(binaryBitmap);
    
    return {
      text: result.getText(),
      format: result.getBarcodeFormat().toString(),
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    console.error('QR Scan Error:', error);
    return null;
  }
}

// GET /test - Test route to verify QR router is working
router.get('/test', (req, res) => {
  res.json({ success: true, message: 'QR route working' });
});

// GET /qr-status - Poll for QR processing status
router.get('/qr-status', async (req, res) => {
  try {
    const { id } = req.query;

    if (!id) {
      return res.status(400).json({
        success: false,
        message: "ID is required"
      });
    }

    return res.json({
      success: true,
      status: "processing",
      progress: 65,
      id
    });

  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Server error"
    });
  }
});

// POST /scan - QR scan endpoint with real QR code detection
router.post('/scan', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ 
        success: false, 
        error: 'Image file is required' 
      });
    }

    console.log(`📸 Processing file: ${req.file.originalname}, Size: ${req.file.size} bytes, Type: ${req.file.mimetype}`);

    // Scan QR code from the uploaded image buffer
    const qrResult = await scanQRFromBuffer(req.file.buffer);
    
    if (!qrResult) {
      return res.status(400).json({
        success: false,
        error: 'No QR code found in the image'
      });
    }

    // Detect type based on content patterns
    let type = 'UNKNOWN';
    const rawText = qrResult.text;
    
    if (rawText.startsWith('M1') && rawText.includes('E')) {
      type = 'IATA_BCBP'; // IATA Bar Coded Boarding Pass
    } else if (rawText.includes('://')) {
      type = 'URL';
    } else if (/^[A-Z0-9]{6}$/.test(rawText)) {
      type = 'PNR_CODE';
    } else if (rawText.includes('BEGIN:VCARD')) {
      type = 'VCARD';
    } else if (rawText.includes('WIFI:')) {
      type = 'WIFI';
    }

    console.log(`✅ QR Code detected: ${type}`);
    
    res.json({ 
      success: true, 
      message: 'QR code scanned successfully',
      data: {
        raw: qrResult.text,
        type: type,
        format: qrResult.format,
        timestamp: qrResult.timestamp
      }
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
