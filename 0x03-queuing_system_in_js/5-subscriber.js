// Import Redis
import redis from 'redis';

// Create redis client
const client = redis.createClient();

// On Connect
client.on('connect', () => {
    console.log('Redis client connected to the server');

    // Subscribe to theHolberton school channel
    client.subscribe('holberton school channel')
});

// on Error
client.on('error', (err) => {
    console.error(`Redis client not connected to the server: ${err}`);
})

client.on('message', (channel, message) => {
    console.log(`${message}`);

    if (message === 'KILL_SERVER') {
        client.unsubscribe();
        client.quit();
    }
})
