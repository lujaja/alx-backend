// Import Redis
import redis from 'redis';

// Create redis client
const client = redis.createClient();

// On Connect
client.on('connect', () => {
    console.log('Redis client connected to the server');
});

// On Error
client.on('error', (err) => {
    console.error(`Redis client not connected to the server: ${err}`);
});

// Function to publish a message after a specified delay
const publishMessage = (message, time) => {
    setTimeout(() => {
        console.log(`About to send ${message}`);
        client.publish('holberton school channel', message);
    }, time);
};

publishMessage("Holberton Student #1 starts course", 100);
publishMessage("Holberton Student #2 starts course", 200);
publishMessage("KILL_SERVER", 300);
publishMessage("Holberton Student #3 starts course", 400);
