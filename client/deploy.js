#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🚀 Deploying Tic-Tac-Toe Client to Vercel...\n');

// Check if .env exists
const envPath = path.join(__dirname, '.env');
if (!fs.existsSync(envPath)) {
  console.error('❌ Error: .env file not found!');
  console.log('📝 Please create a .env file with your production URLs:');
  console.log('   VITE_API_URL=https://your-railway-app.railway.app/api');
  console.log('   VITE_SOCKET_URL=https://your-railway-app.railway.app');
  process.exit(1);
}

try {
  // Build the project
  console.log('📦 Building project...');
  execSync('npm run build', { stdio: 'inherit' });
  
  // Deploy to Vercel
  console.log('\n🔄 Deploying to Vercel...');
  execSync('vercel --prod', { stdio: 'inherit' });
  
  console.log('\n✅ Deployment complete!');
  console.log('🌍 Your app should now be live on Vercel');
  
} catch (error) {
  console.error('\n❌ Deployment failed:', error.message);
  process.exit(1);
}
