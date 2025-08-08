// Build script for Vercel deployment
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('Building ERHAN Visitor System for Vercel...');

// Build client
console.log('Building client...');
execSync('cd client && npm run build', { stdio: 'inherit' });

// Copy client dist to root
console.log('Copying build files...');
if (fs.existsSync('dist')) {
  fs.rmSync('dist', { recursive: true, force: true });
}
fs.cpSync('client/dist', 'dist', { recursive: true });

console.log('Build completed successfully!');