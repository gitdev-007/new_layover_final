import { Router } from 'express';
import multer from 'multer';
import AWS from 'aws-sdk';
import supabaseClient from '../supabaseClient.js';
import { scanQR } from '../services/qrScanner.js';
import { validateQR } from '../services/validation.js';
import { parseQRData } from '../services/parser.js';
import { detectFraud } from '../services/fraudDetection.js';
import { decodeBCBP } from '../services/bcbpDecoder.js';

const router = Router();

// Configure AWS S3
const s3 = new AWS.S3({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  region: process.env.AWS_REGION,
});

/**
 * Background QR processing function
 * Processes uploaded QR files asynchronously
 * @param {string} id - Upload ID
 */
async function processQRInBackground(id) {
  try {
    console.log(`[Background] Starting processing for upload ${id}`);
    
    // Fetch the upload record
    const { data: upload, error: fetchError } = await supabaseClient
      .from('qr_uploads')
      .select('*')
      .eq('id', id)
      .single();

    if (fetchError || !upload) {
      console.error(`[Background] Upload ${id} not found`);
      return;
    }

    // Update status to processing
    await supabaseClient
      .from('qr_uploads')
      .update({ status: 'processing' })
      .eq('id', id);

    // Download file from S3
    const s3Key = upload.file_url.split('/').pop();
    const s3Params = {
      Bucket: process.env.AWS_BUCKET_NAME,
      Key: s3Key,
    };
    
    const s3Object = await s3.getObject(s3Params).promise();
    const buffer = s3Object.Body;

    // Scan QR code
    const qrData = await scanQR(buffer);

    // Check for duplicate QR data
    const { data: existingUploads, error: duplicateError } = await supabaseClient
      .from('qr_uploads')
      .select('id')
      .eq('qr_data', qrData)
      .neq('id', id)
      .limit(1);

    const isDuplicate = existingUploads && existingUploads.length > 0;

    // Check if QR data matches BCBP format (starts with M or S followed by digit)
    const isBCBPFormat = /^[MS]\d/.test(qrData);
    
    // Parse QR data using appropriate parser
    let extractedInfo;
    if (isBCBPFormat) {
      console.log(`[Background] Detected BCBP format for upload ${id}`);
      extractedInfo = decodeBCBP(qrData);
    } else {
      console.log(`[Background] Using standard parser for upload ${id}`);
      extractedInfo = parseQRData(qrData);
    }
    
    const validationResult = validateQR(qrData);
    const isValid = validationResult.isValid;

    // Detect fraud
    const fraudResult = await detectFraud(qrData, extractedInfo);

    // Determine status
    let status = isValid ? 'verified' : 'failed';
    if (isDuplicate) {
      status = 'duplicate';
    }
    if (fraudResult.isFraud) {
      status = 'fraud';
    }

    // Update DB with results
    // Handle both BCBP (airlineCode) and standard parser (airline) formats
    const airlineCode = extractedInfo.airlineCode || extractedInfo.airline || null;
    
    await supabaseClient
      .from('qr_uploads')
      .update({
        qr_data: qrData,
        is_valid: isValid,
        status: status,
        is_duplicate: isDuplicate,
        is_fraud: fraudResult.isFraud,
        fraud_reason: fraudResult.reason,
        extracted_info: extractedInfo,
        airline: airlineCode
      })
      .eq('id', id);

    console.log(`[Background] Completed processing for upload ${id}. Status: ${status}, Fraud: ${fraudResult.isFraud}`);

  } catch (error) {
    console.error(`[Background] Error processing upload ${id}:`, error);
    
    // Update status to failed
    await supabaseClient
      .from('qr_uploads')
      .update({
        status: 'failed',
        qr_data: error.message
      })
      .eq('id', id);
  }
}

// Simple in-memory rate limiter (requests per IP)
const rateLimits = new Map();
const RATE_LIMIT_WINDOW = 60 * 1000; // 1 minute
const RATE_LIMIT_MAX = 10; // max 10 requests per minute

function rateLimit(req, res, next) {
  const ip = req.ip || req.connection.remoteAddress || 'unknown';
  const now = Date.now();

  for (const [key, entry] of rateLimits.entries()) {
    if (now - entry.timestamp > RATE_LIMIT_WINDOW) {
      rateLimits.delete(key);
    }
  }

  const ipData = rateLimits.get(ip);

  if (ipData) {
    if (now - ipData.timestamp > RATE_LIMIT_WINDOW) {
      rateLimits.set(ip, { count: 1, timestamp: now });
    } else if (ipData.count >= RATE_LIMIT_MAX) {
      return res.status(429).json({
        success: false,
        error: 'Rate limit exceeded'
      });
    } else {
      rateLimits.set(ip, {
        count: ipData.count + 1,
        timestamp: ipData.timestamp
      });
    }
  } else {
    rateLimits.set(ip, { count: 1, timestamp: now });
  }

  next();
}

// Configure multer with memory storage
const upload = multer({
  storage: multer.memoryStorage(),
});

// GET /my-uploads - Get user's uploads
router.get('/my-uploads', async (req, res) => {
  try {
    // Get user from JWT token
    const authHeader = req.headers.authorization;
    
    if (!authHeader) {
      return res.status(401).json({
        success: false,
        error: 'Authentication required'
      });
    }

    const token = authHeader.replace('Bearer ', '');
    const { data: { user }, error: authError } = await supabaseClient.auth.getUser(token);

    if (authError || !user) {
      return res.status(401).json({
        success: false,
        error: 'Invalid or expired token'
      });
    }

    // Fetch user's uploads
    const { data: uploads, error } = await supabaseClient
      .from('qr_uploads')
      .select('*')
      .eq('user_id', user.id)
      .order('created_at', { ascending: false });

    if (error) {
      throw new Error(`Failed to fetch uploads: ${error.message}`);
    }

    res.json({
      success: true,
      data: uploads || []
    });

  } catch (error) {
    console.error('Fetch uploads error:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to fetch uploads'
    });
  }
});

export const uploadQR = async (req, res) => {
  try {
    console.log("FILE RECEIVED:", req.file);

    if (!req.file) {
      return res.status(400).json({ message: "No file uploaded" });
    }

    const params = {
      Bucket: process.env.AWS_BUCKET_NAME,
      Key: Date.now() + "-" + req.file.originalname,
      Body: req.file.buffer,
      ContentType: req.file.mimetype,
    };

    const uploadResult = await s3.upload(params).promise();

    return res.status(200).json({
      success: true,
      url: uploadResult.Location,
    });

  } catch (error) {
    console.error("UPLOAD ERROR FULL:", error);
    return res.status(500).json({
      message: error.message || "Upload failed",
    });
  }
};

// POST /upload-qr - Upload QR file to S3
router.post('/upload-qr', rateLimit, upload.single('file'), uploadQR);

// Export cleanup function for testing/development
export function cleanupRateLimits() {
  rateLimits.clear();
}

export default router;
