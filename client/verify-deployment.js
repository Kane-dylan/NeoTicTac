#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🔍 Pre-Deployment Verification for Tic-Tac-Toe\n');

let allGood = true;

// Check Client Configuration
console.log('📱 Checking Client Configuration...');

// Check if .env exists
const clientEnvPath = path.join(__dirname, '.env');
if (fs.existsSync(clientEnvPath)) {
  console.log('✅ Client .env file exists');
  const envContent = fs.readFileSync(clientEnvPath, 'utf8');
  if (envContent.includes('VITE_API_URL') && envContent.includes('VITE_SOCKET_URL')) {
    console.log('✅ Required environment variables found');
  } else {
    console.log('❌ Missing required environment variables in .env');
    allGood = false;
  }
} else {
  console.log('❌ Client .env file missing');
  allGood = false;
}

// Check package.json
const packagePath = path.join(__dirname, 'package.json');
if (fs.existsSync(packagePath)) {
  console.log('✅ package.json exists');
  const packageContent = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
  if (packageContent.scripts && packageContent.scripts.build) {
    console.log('✅ Build script configured');
  } else {
    console.log('❌ Build script missing');
    allGood = false;
  }
} else {
  console.log('❌ package.json missing');
  allGood = false;
}

// Check vercel.json
const vercelPath = path.join(__dirname, 'vercel.json');
if (fs.existsSync(vercelPath)) {
  console.log('✅ vercel.json exists');
  const vercelContent = JSON.parse(fs.readFileSync(vercelPath, 'utf8'));
  if (!vercelContent.functions) {
    console.log('✅ No incorrect functions configuration');
  } else {
    console.log('❌ Incorrect functions configuration found');
    allGood = false;
  }
} else {
  console.log('❌ vercel.json missing');
  allGood = false;
}

// Check Server Configuration
console.log('\n🖥️  Checking Server Configuration...');

const serverPath = path.join(__dirname, '..', 'server');

// Check if server directory exists
if (fs.existsSync(serverPath)) {
  console.log('✅ Server directory exists');
  
  // Check wsgi.py
  const wsgiPath = path.join(serverPath, 'wsgi.py');
  if (fs.existsSync(wsgiPath)) {
    console.log('✅ wsgi.py exists');
  } else {
    console.log('❌ wsgi.py missing');
    allGood = false;
  }
  
  // Check railway.json
  const railwayPath = path.join(serverPath, 'railway.json');
  if (fs.existsSync(railwayPath)) {
    console.log('✅ railway.json exists');
  } else {
    console.log('❌ railway.json missing');
    allGood = false;
  }
  
  // Check Procfile
  const procfilePath = path.join(serverPath, 'Procfile');
  if (fs.existsSync(procfilePath)) {
    console.log('✅ Procfile exists');
  } else {
    console.log('❌ Procfile missing');
    allGood = false;
  }
  
  // Check requirements.txt
  const reqPath = path.join(serverPath, 'requirements.txt');
  if (fs.existsSync(reqPath)) {
    console.log('✅ requirements.txt exists');
  } else {
    console.log('❌ requirements.txt missing');
    allGood = false;
  }
  
} else {
  console.log('❌ Server directory not found');
  allGood = false;
}

console.log('\n📋 Verification Results:');
if (allGood) {
  console.log('🎉 All checks passed! Ready for deployment.');
  console.log('\n📝 Next steps:');
  console.log('1. Deploy server to Railway: cd ../server && railway up');
  console.log('2. Update client .env with Railway URL');
  console.log('3. Deploy client to Vercel: npm run deploy');
} else {
  console.log('❌ Some issues found. Please fix them before deploying.');
  console.log('\n📖 See DEPLOYMENT_GUIDE.md for detailed instructions.');
}

console.log('\n🔗 Useful links:');
console.log('- Railway Dashboard: https://railway.app/dashboard');
console.log('- Vercel Dashboard: https://vercel.com/dashboard');
