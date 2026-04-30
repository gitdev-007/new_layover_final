/**
 * IATA Airline Designator Codes
 * Comprehensive list of 2-3 letter airline codes
 */
const VALID_AIRLINES = new Set([
  // Indian Airlines
  'AI', // Air India
  '6E', // IndiGo
  'UK', // Vistara
  'G8', // Go First
  'SG', // SpiceJet
  'I5', // Air India Express
  'QP', // Akasa Air
  '2T', // TruJet
  '9I', // Alliance Air
  'H1', // Hindustan Aeronautics
  
  // International - Asia
  'SQ', // Singapore Airlines
  'CX', // Cathay Pacific
  'MH', // Malaysia Airlines
  'TG', // Thai Airways
  'KE', // Korean Air
  'JL', // Japan Airlines
  'NH', // All Nippon Airways
  'EY', // Etihad
  'QR', // Qatar Airways
  'EK', // Emirates
  
  // International - Europe
  'BA', // British Airways
  'LH', // Lufthansa
  'AF', // Air France
  'KL', // KLM
  'LX', // Swiss
  'VS', // Virgin Atlantic
  
  // International - Americas
  'AA', // American Airlines
  'UA', // United Airlines
  'DL', // Delta
  'AC', // Air Canada
]);

/**
 * Extract value from QR data by key
 * @param {string} qrData - QR data string
 * @param {string} key - Key to search for
 * @returns {string|null} Extracted value or null
 */
function extractValue(qrData, key) {
  const regex = new RegExp(`${key}[\\s]*:[\\s]*([^|\\s;]+)`, 'i');
  const match = qrData.match(regex);
  return match ? match[1].trim() : null;
}

/**
 * Validate PNR format (6 alphanumeric characters)
 * @param {string} pnr - PNR code
 * @returns {boolean} True if valid PNR format
 */
export function validatePNR(pnr) {
  if (!pnr || typeof pnr !== 'string') {
    return false;
  }
  // PNR should be exactly 6 alphanumeric characters
  return /^[A-Z0-9]{6}$/i.test(pnr.trim());
}

/**
 * Validate Flight format (2 letters + 1-4 digits)
 * @param {string} flight - Flight number
 * @returns {boolean} True if valid flight format
 */
export function validateFlight(flight) {
  if (!flight || typeof flight !== 'string') {
    return false;
  }
  const trimmed = flight.trim().toUpperCase();
  // Flight should be 2 letters followed by 1-4 digits
  return /^[A-Z]{2}\d{1,4}$/.test(trimmed);
}

/**
 * Extract airline code from flight number
 * @param {string} flight - Flight number
 * @returns {string|null} 2-letter airline code
 */
export function extractAirlineCode(flight) {
  if (!flight || typeof flight !== 'string') {
    return null;
  }
  const trimmed = flight.trim().toUpperCase();
  // Extract first 2 letters if flight format is valid
  if (/^[A-Z]{2}\d{1,4}$/.test(trimmed)) {
    return trimmed.substring(0, 2);
  }
  return null;
}

/**
 * Validate airline code against known airlines
 * @param {string} airlineCode - 2-letter airline code
 * @returns {boolean} True if valid airline
 */
export function validateAirlineCode(airlineCode) {
  if (!airlineCode || typeof airlineCode !== 'string') {
    return false;
  }
  return VALID_AIRLINES.has(airlineCode.toUpperCase());
}

/**
 * Validate seat number format
 * Format: 1-3 digits + 1 letter (e.g., 12A, 5F, 123K)
 * @param {string} seat - Seat number
 * @returns {boolean} True if valid seat format
 */
export function validateSeat(seat) {
  if (!seat || typeof seat !== 'string') {
    return false;
  }
  const trimmed = seat.trim().toUpperCase();
  // Valid seat: 1-3 digits followed by A-Z (max 999 rows, columns A-K typical)
  return /^\d{1,3}[A-K]$/.test(trimmed);
}

/**
 * Validate date format and realism
 * Accepts: DDMMM or YYYY-MM-DD formats
 * Date must be within 1 year of current date
 * @param {string} dateStr - Date string
 * @returns {{valid: boolean, error: string|null, formatted: string|null}}
 */
export function validateDate(dateStr) {
  if (!dateStr || typeof dateStr !== 'string') {
    return { valid: false, error: 'No date provided', formatted: null };
  }
  
  const trimmed = dateStr.trim();
  const now = new Date();
  const currentYear = now.getFullYear();
  let parsedDate = null;
  
  // Format 1: DDMMM (e.g., 24MAY)
  const ddmmmMatch = trimmed.match(/^(\d{2})([A-Z]{3})$/i);
  if (ddmmmMatch) {
    const day = parseInt(ddmmmMatch[1], 10);
    const monthStr = ddmmmMatch[2].toUpperCase();
    const months = {
      'JAN': 0, 'FEB': 1, 'MAR': 2, 'APR': 3, 'MAY': 4, 'JUN': 5,
      'JUL': 6, 'AUG': 7, 'SEP': 8, 'OCT': 9, 'NOV': 10, 'DEC': 11
    };
    
    const month = months[monthStr];
    if (month === undefined) {
      return { valid: false, error: `Invalid month: ${monthStr}`, formatted: null };
    }
    if (day < 1 || day > 31) {
      return { valid: false, error: `Invalid day: ${day}`, formatted: null };
    }
    
    // Assume current year, but handle year boundary
    let year = currentYear;
    parsedDate = new Date(year, month, day);
    
    // If date is more than 6 months in past, assume next year
    const sixMonthsAgo = new Date(now);
    sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6);
    if (parsedDate < sixMonthsAgo) {
      year++;
      parsedDate = new Date(year, month, day);
    }
  }
  
  // Format 2: YYYY-MM-DD
  else if (/^\d{4}-\d{2}-\d{2}$/.test(trimmed)) {
    parsedDate = new Date(trimmed);
    if (isNaN(parsedDate.getTime())) {
      return { valid: false, error: 'Invalid date format', formatted: null };
    }
  }
  
  // Format 3: DD/MM/YYYY or DD-MM-YYYY
  else if (/^\d{2}[\/\-]\d{2}[\/\-]\d{4}$/.test(trimmed)) {
    const sep = trimmed.includes('/') ? '/' : '-';
    const parts = trimmed.split(sep);
    const day = parseInt(parts[0], 10);
    const month = parseInt(parts[1], 10) - 1;
    const year = parseInt(parts[2], 10);
    parsedDate = new Date(year, month, day);
    if (isNaN(parsedDate.getTime())) {
      return { valid: false, error: 'Invalid date values', formatted: null };
    }
  }
  
  // No valid format found
  else {
    return { valid: false, error: 'Unrecognized date format. Expected: DDMMM or YYYY-MM-DD', formatted: null };
  }
  
  // Check date is realistic (within 1 year from now, not in past more than 1 day)
  const oneYearFromNow = new Date(now);
  oneYearFromNow.setFullYear(oneYearFromNow.getFullYear() + 1);
  
  const yesterday = new Date(now);
  yesterday.setDate(yesterday.getDate() - 1);
  yesterday.setHours(0, 0, 0, 0);
  
  if (parsedDate < yesterday) {
    return { valid: false, error: 'Date is in the past', formatted: null };
  }
  
  if (parsedDate > oneYearFromNow) {
    return { valid: false, error: 'Date is more than 1 year in the future', formatted: null };
  }
  
  // Format as DD-MMM-YYYY
  const formatted = parsedDate.toLocaleDateString('en-US', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  }).toUpperCase().replace(/ /g, '-');
  
  return { valid: true, error: null, formatted };
}

/**
 * Full QR data validation
 * @param {string} qrData - Decoded QR string
 * @returns {Object} Validation result with isValid flag and extracted data
 */
/**
 * Comprehensive QR data validation
 * Validates: PNR, Flight, Airline, Seat, Date
 * @param {string} qrData - Decoded QR string
 * @param {Object} extractedInfo - Optional pre-parsed data
 * @returns {Object} Validation result with isValid flag and detailed errors
 */
export function validateQR(qrData, extractedInfo = null) {
  if (!qrData || typeof qrData !== 'string') {
    return {
      isValid: false,
      pnr: null,
      flight: null,
      airline: null,
      seat: null,
      date: null,
      errors: ['No QR data provided']
    };
  }

  const errors = [];
  const normalizedData = qrData.toUpperCase();

  // Extract values (from data or use provided extractedInfo)
  let pnr, flight, airline, seat, date;
  
  if (extractedInfo) {
    // Handle both BCBP and standard parser formats
    pnr = extractedInfo.pnr || extractedInfo.pnrCode || null;
    flight = extractedInfo.flightNumber || extractedInfo.flight || null;
    airline = extractedInfo.airlineCode || extractedInfo.airline || null;
    seat = extractedInfo.seat || null;
    date = extractedInfo.date || null;
  } else {
    pnr = extractValue(normalizedData, 'PNR');
    flight = extractValue(normalizedData, 'FLIGHT');
    seat = extractValue(normalizedData, 'SEAT');
    date = extractValue(normalizedData, 'DATE');
    airline = flight ? extractAirlineCode(flight) : null;
  }

  // Validate PNR format
  if (!pnr) {
    errors.push('PNR not found');
  } else if (!validatePNR(pnr)) {
    errors.push(`Invalid PNR format: ${pnr} (should be 6 alphanumeric characters)`);
  }

  // Validate Flight format
  if (!flight) {
    errors.push('Flight number not found');
  } else if (!validateFlight(flight)) {
    errors.push(`Invalid flight format: ${flight} (should be 2 letters + 1-4 digits)`);
  }

  // Validate airline code
  if (airline) {
    if (!validateAirlineCode(airline)) {
      errors.push(`Unknown airline code: ${airline} (not in IATA registry)`);
    }
  } else if (flight) {
    errors.push('Could not extract airline code from flight number');
  }

  // Validate seat if provided
  if (seat && !validateSeat(seat)) {
    errors.push(`Invalid seat format: ${seat} (expected: 1-3 digits + A-K, e.g., 12A)`);
  }

  // Validate date if provided
  if (date) {
    const dateValidation = validateDate(date);
    if (!dateValidation.valid) {
      errors.push(`Invalid date: ${dateValidation.error}`);
    }
  }

  const isValid = errors.length === 0 && pnr && flight && airline && validateAirlineCode(airline);

  return {
    isValid,
    pnr: pnr || null,
    flight: flight || null,
    airline: airline || null,
    seat: seat || null,
    date: date || null,
    errors: errors.length > 0 ? errors : null
  };
}

export default { 
  validateQR, 
  validatePNR, 
  validateFlight, 
  extractAirlineCode, 
  validateAirlineCode,
  validateSeat,
  validateDate 
};
