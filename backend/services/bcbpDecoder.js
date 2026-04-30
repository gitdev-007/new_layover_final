/**
 * IATA BCBP (Bar Coded Boarding Pass) Decoder
 * Decodes raw BCBP strings into structured flight data
 * Based on IATA Resolution 792
 */

/**
 * Decodes BCBP string into structured data
 * @param {string} qrData - Raw BCBP string
 * @returns {Object} Structured boarding pass data
 */
export function decodeBCBP(qrData) {
  if (!qrData || typeof qrData !== 'string') {
    return {
      passengerName: null,
      pnr: null,
      flightNumber: null,
      airlineCode: null,
      seat: null,
      date: null,
      raw: qrData,
      isValid: false
    };
  }

  try {
    const result = {
      passengerName: null,
      pnr: null,
      flightNumber: null,
      airlineCode: null,
      seat: null,
      date: null,
      raw: qrData,
      isValid: false
    };

    // BCBP typically starts with 'M' (multiple) or 'S' (single)
    // Format: M1 (Format code + Legs)
    const trimmed = qrData.trim();
    
    // Check if it's a BCBP format
    if (trimmed.startsWith('M') || trimmed.startsWith('S')) {
      result.isValid = true;
      
      // Parse based on IATA BCBP standard
      // Position 0: Format Code (M=Multi, S=Single)
      // Position 1: Number of legs (1-9)
      
      let pos = 0;
      
      // Skip format code and leg count
      pos = 2;
      
      // Passenger Name (up to 20 chars, ends with field separator or spaces)
      // Usually starts after position 2
      const nameMatch = trimmed.match(/^M?1?([^/\s]{2,20})/);
      if (nameMatch) {
        result.passengerName = formatName(nameMatch[1]);
      }
    }

    // Alternative parsing for common formats
    // Try to extract using regex patterns
    
    // Passenger Name: usually uppercase, can have / separator
    // Format: LASTNAME/FIRSTNAME or LASTNAME/FIRSTNAME MIDDLE
    const namePatterns = [
      /([A-Z]+\/[A-Z\s]+)/,  // LASTNAME/FIRSTNAME
      /NAME[:\s]+([A-Z\s\/]+)/i,  // NAME: LASTNAME/FIRSTNAME
      /PASSENGER[:\s]+([A-Z\s\/]+)/i  // PASSENGER: NAME
    ];
    
    for (const pattern of namePatterns) {
      const match = trimmed.match(pattern);
      if (match && match[1]) {
        result.passengerName = formatName(match[1].trim());
        break;
      }
    }

    // PNR/Booking Reference (6 alphanumeric)
    const pnrPatterns = [
      /PNR[:\s]+([A-Z0-9]{6})/i,
      /BOOKING[:\s]+([A-Z0-9]{6})/i,
      /REF[:\s]+([A-Z0-9]{6})/i,
      /REFERENCE[:\s]+([A-Z0-9]{6})/i,
      /\b([A-Z0-9]{6})\b/  // Standalone 6-char code
    ];
    
    for (const pattern of pnrPatterns) {
      const match = trimmed.match(pattern);
      if (match && match[1]) {
        result.pnr = match[1].toUpperCase();
        break;
      }
    }

    // Flight Number: 2 letter airline code + 1-4 digits
    const flightPatterns = [
      /FLIGHT[:\s]+([A-Z]{2,3}\d{1,4})/i,
      /FLT[:\s]+([A-Z]{2,3}\d{1,4})/i,
      /\b([A-Z]{2}\d{3,4})\b/,  // AI202, 6E1234
      /\b([A-Z]{3}\d{1,4})\b/   // AIC202
    ];
    
    for (const pattern of flightPatterns) {
      const match = trimmed.match(pattern);
      if (match && match[1]) {
        result.flightNumber = match[1].toUpperCase();
        // Extract airline code from flight number
        result.airlineCode = result.flightNumber.replace(/\d/g, '');
        break;
      }
    }

    // Seat Number: Format like 12A, 5F, etc.
    const seatPatterns = [
      /SEAT[:\s]+(\d{1,3}[A-Z])/i,
      /\b(\d{1,3}[A-Z])\b/  // Standalone seat number
    ];
    
    for (const pattern of seatPatterns) {
      const match = trimmed.match(pattern);
      if (match && match[1] && isValidSeat(match[1])) {
        result.seat = match[1].toUpperCase();
        break;
      }
    }

    // Date: Various formats
    const datePatterns = [
      /DATE[:\s]+(\d{2}[A-Z]{3})/i,  // DDMMM format
      /DATE[:\s]+(\d{2}[A-Z]{3}\d{2,4})/i,  // DDMMMYY
      /\b(\d{2}[A-Z]{3})\b/  // Standalone date
    ];
    
    for (const pattern of datePatterns) {
      const match = trimmed.match(pattern);
      if (match && match[1]) {
        result.date = parseDate(match[1]);
        break;
      }
    }

    // BCBP specific parsing if standard format
    if (result.isValid && trimmed.startsWith('M')) {
      // Deep parse BCBP structure
      parseBCBPStructure(trimmed, result);
    }

    return result;

  } catch (error) {
    console.error('BCBP decode error:', error);
    return {
      passengerName: null,
      pnr: null,
      flightNumber: null,
      airlineCode: null,
      seat: null,
      date: null,
      raw: qrData,
      isValid: false,
      error: error.message
    };
  }
}

/**
 * Parse deep BCBP structure
 */
function parseBCBPStructure(data, result) {
  try {
    // BCBP M1 format:
    // M1 - Format code + Number of legs
    // Then repeated for each leg:
    // - Passenger Name (20 chars)
    // - Electronic Ticket Indicator (1 char)
    // - Operating Carrier PNR (7 chars)
    // - Origin Airport (3 chars)
    // - Destination Airport (3 chars)
    // - Operating Carrier Designator (3 chars)
    // - Flight Number (5 chars)
    // - Date of Flight (3 chars - Julian date)
    // - Compartment Code (1 char)
    // - Seat Number (4 chars)
    // - Check-in Sequence (5 chars)
    // - Passenger Status (1 char)
    
    let pos = 2; // After M1
    
    // Passenger Name (20 chars, left-justified, space-padded)
    if (!result.passengerName && data.length > pos + 20) {
      const nameRaw = data.substring(pos, pos + 20).trim();
      if (nameRaw && nameRaw.length > 1) {
        result.passengerName = formatName(nameRaw);
      }
    }
    pos += 20;
    
    // Electronic Ticket Indicator
    pos += 1;
    
    // Operating Carrier PNR (7 chars) - This could be the PNR
    if (!result.pnr && data.length > pos + 7) {
      const pnrRaw = data.substring(pos, pos + 7).trim();
      if (pnrRaw && /^[A-Z0-9]+$/.test(pnrRaw)) {
        result.pnr = pnrRaw;
      }
    }
    pos += 7;
    
    // Origin (3) + Destination (3)
    pos += 6;
    
    // Operating Carrier Designator (3 chars)
    if (!result.airlineCode && data.length > pos + 3) {
      const airline = data.substring(pos, pos + 3).trim();
      if (airline && /^[A-Z]{2,3}$/.test(airline)) {
        result.airlineCode = airline;
      }
    }
    pos += 3;
    
    // Flight Number (5 chars)
    if (!result.flightNumber && data.length > pos + 5) {
      const flightRaw = data.substring(pos, pos + 5).trim();
      if (flightRaw && /^\d{1,4}$/.test(flightRaw)) {
        result.flightNumber = (result.airlineCode || 'XX') + flightRaw.padStart(3, '0');
      }
    }
    pos += 5;
    
    // Date of Flight (3 chars - Julian day)
    if (!result.date && data.length > pos + 3) {
      const julianDate = data.substring(pos, pos + 3);
      if (/^\d{3}$/.test(julianDate)) {
        result.date = julianToDate(julianDate);
      }
    }
    pos += 3;
    
    // Compartment Code (1)
    pos += 1;
    
    // Seat Number (4 chars)
    if (!result.seat && data.length > pos + 4) {
      const seatRaw = data.substring(pos, pos + 4).trim();
      if (seatRaw && /^\d{1,3}[A-Z]$/.test(seatRaw)) {
        result.seat = seatRaw;
      }
    }
    
  } catch (error) {
    console.error('BCBP structure parse error:', error);
  }
}

/**
 * Format passenger name
 */
function formatName(nameRaw) {
  if (!nameRaw) return null;
  
  // Replace / with space for display
  let name = nameRaw.replace(/\//g, ' ').trim();
  
  // Handle common formats
  // LASTNAME/FIRSTNAME -> FIRSTNAME LASTNAME
  const parts = name.split(' ');
  if (parts.length >= 2 && nameRaw.includes('/')) {
    // Already in correct order from replace
    return parts.map(p => p.charAt(0) + p.slice(1).toLowerCase()).join(' ');
  }
  
  return name;
}

/**
 * Check if seat number is valid
 */
function isValidSeat(seat) {
  if (!seat || seat.length < 2) return false;
  const row = seat.slice(0, -1);
  const letter = seat.slice(-1);
  return /^\d{1,3}$/.test(row) && /^[A-Z]$/.test(letter);
}

/**
 * Parse date string to readable format
 */
function parseDate(dateStr) {
  if (!dateStr || dateStr.length < 5) return null;
  
  const months = {
    'JAN': 'January', 'FEB': 'February', 'MAR': 'March',
    'APR': 'April', 'MAY': 'May', 'JUN': 'June',
    'JUL': 'July', 'AUG': 'August', 'SEP': 'September',
    'OCT': 'October', 'NOV': 'November', 'DEC': 'December'
  };
  
  const day = dateStr.substring(0, 2);
  const month = dateStr.substring(2, 5).toUpperCase();
  
  const monthName = months[month] || month;
  return `${day} ${monthName}`;
}

/**
 * Convert Julian day to date
 */
function julianToDate(julianDay) {
  const day = parseInt(julianDay, 10);
  if (isNaN(day) || day < 1 || day > 366) return null;
  
  const now = new Date();
  const year = now.getFullYear();
  const date = new Date(year, 0, day); // Jan 1 + day-1
  
  return date.toLocaleDateString('en-US', {
    day: '2-digit',
    month: 'short'
  });
}

export default { decodeBCBP };
