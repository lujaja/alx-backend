// import redis
import redis from 'redis'

// Create redis client
const client = redis.createClient();

client.on('connect', () => {
    console.log('Redis client connected to the server');
});

client.on('error', (err) => {
    console,error(`Redis client not connected to the server: ${err}`);
})

// Define the hash data
const hashKey = 'HolbertonSchools';
const hashData = {
  Portland: 50,
  Seattle: 80,
  'New York': 20,
  Bogota: 20,
  Cali: 40,
  Paris: 2
};

Object.keys(hashData).forEach((key) => {
    client.hset(hashKey, key, hashData[key], redis.print);
});

client.hgetall(hashKey, (err, reply) => {
    if (err) {
        console.error(err);
    } else {
        console.log(reply);
    }

    client.quit();
});