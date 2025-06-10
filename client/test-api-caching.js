// Test script to verify API caching is working
const { getGameDetails } = require("./src/services/api.js");

async function testCaching() {
  console.log("Testing API caching mechanism...");

  const gameId = 14;

  console.log("\n1. First call to getGameDetails...");
  const start1 = Date.now();
  try {
    await getGameDetails(gameId);
    console.log(`First call took: ${Date.now() - start1}ms`);
  } catch (error) {
    console.log(`First call failed: ${error.message}`);
  }

  console.log("\n2. Second call immediately after (should use cache)...");
  const start2 = Date.now();
  try {
    await getGameDetails(gameId);
    console.log(`Second call took: ${Date.now() - start2}ms`);
  } catch (error) {
    console.log(`Second call failed: ${error.message}`);
  }

  console.log(
    "\n3. Waiting 3 seconds and trying again (cache should expire)..."
  );
  setTimeout(async () => {
    const start3 = Date.now();
    try {
      await getGameDetails(gameId);
      console.log(`Third call took: ${Date.now() - start3}ms`);
    } catch (error) {
      console.log(`Third call failed: ${error.message}`);
    }
  }, 3000);
}

testCaching();
