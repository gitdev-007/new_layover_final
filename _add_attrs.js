const fs = require('fs');
const path = 'c:\\Users\\Dev Tinker\\Desktop\\layoverX_dummy\\hotel.html';
let html = fs.readFileSync(path, 'utf8');

// Find all hotel-item divs and add data attributes before the closing >
html = html.replace(
  /<div class="hotel-item([^"]*)"([^>]*)>/g,
  '<div class="hotel-item$1"$2 data-duration="2" data-price="1200" data-distance="3" data-amenities="wifi">'
);

fs.writeFileSync(path, html);
console.log('Done');
