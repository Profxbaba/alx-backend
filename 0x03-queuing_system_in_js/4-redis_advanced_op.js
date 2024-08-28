import redis from 'redis';

// Create Redis client
const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

// Store the hash in Redis
const key = 'HolbertonSchools';
const values = {
  Portland: 50,
  Seattle: 80,
  'New York': 20,
  Bogota: 20,
  Cali: 40,
  Paris: 2
};

// Use hset to store each key-value pair in the hash
for (const [field, value] of Object.entries(values)) {
  client.hset(key, field, value, redis.print);
}

// Retrieve and display the stored hash
client.hgetall(key, (err, result) => {
  if (err) {
    console.error(`Error retrieving hash: ${err}`);
  } else {
    console.log(result);
  }

  // Close the Redis connection
  client.quit();
});
