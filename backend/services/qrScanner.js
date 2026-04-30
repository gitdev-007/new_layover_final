import { MultiFormatReader, BarcodeFormat } from '@zxing/library';
import sharp from 'sharp';
import { PDFDocument } from 'pdf-lib';
import { pdf } from 'pdf-to-img';

/**
 * Check if buffer is a PDF file
 * @param {Buffer} buffer - File buffer
 * @returns {boolean} True if PDF
 */
function isPDF(buffer) {
  // PDF files start with %PDF-
  return buffer.slice(0, 5).toString('ascii') === '%PDF-';
}

/**
 * Convert PDF first page to image buffer
 * @param {Buffer} buffer - PDF buffer
 * @returns {Promise<Buffer>} PNG image buffer
 */
async function pdfToImage(buffer) {
  try {
    // Convert PDF buffer to images
    const pages = await pdf(buffer, {
      scale: 2.0, // Higher resolution for better QR scanning
      format: 'png'
    });
    
    // Return first page as buffer
    if (pages.length === 0) {
      throw new Error('PDF has no pages');
    }
    
    // pages[0] is already a Buffer (PNG)
    return pages[0];
  } catch (error) {
    console.error('PDF conversion error:', error);
    throw new Error('Failed to convert PDF to image');
  }
}

/**
 * Scan QR code from image or PDF buffer
 * @param {Buffer} buffer - File buffer (image or PDF)
 * @returns {Promise<string>} Decoded QR string
 */
export async function scanQR(buffer) {
  try {
    let imageBuffer = buffer;
    
    // Check if PDF and convert to image
    if (isPDF(buffer)) {
      console.log('PDF detected, converting to image...');
      imageBuffer = await pdfToImage(buffer);
    }
    
    // Convert buffer to raw image data using sharp
    const { data, info } = await sharp(imageBuffer)
      .raw()
      .ensureAlpha()
      .toBuffer({ resolveWithObject: true });

    // Create ZXing reader
    const reader = new MultiFormatReader();
    const hints = new Map();
    hints.set(3, [BarcodeFormat.QR_CODE]); // 3 = POSSIBLE_FORMATS

    // Decode the QR code
    const luminanceSource = {
      getWidth: () => info.width,
      getHeight: () => info.height,
      getRow: (y, row) => {
        for (let x = 0; x < info.width; x++) {
          const offset = (y * info.width + x) * 4;
          // Convert RGBA to luminance
          row[x] = ((data[offset] + data[offset + 1] + data[offset + 2]) / 3) & 0xFF;
        }
        return row;
      },
      getMatrix: () => {
        const matrix = new Uint8ClampedArray(info.width * info.height);
        for (let y = 0; y < info.height; y++) {
          for (let x = 0; x < info.width; x++) {
            const offset = (y * info.width + x) * 4;
            matrix[y * info.width + x] = ((data[offset] + data[offset + 1] + data[offset + 2]) / 3) & 0xFF;
          }
        }
        return matrix;
      }
    };

    const binaryBitmap = {
      getWidth: () => info.width,
      getHeight: () => info.height,
      getBlackRow: (y, row) => luminanceSource.getRow(y, row),
      getBlackMatrix: () => luminanceSource.getMatrix()
    };

    const result = reader.decode(binaryBitmap, hints);
    return result.getText();

  } catch (error) {
    console.error('QR scanning error:', error);
    if (error.message.includes('PDF')) {
      throw new Error('Failed to process PDF file');
    }
    throw new Error('No QR code found');
  }
}

export default { scanQR };
