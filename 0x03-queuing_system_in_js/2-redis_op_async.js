// import redis
import redis from 'redis';
import { promisify } from 'util';

// Creat redis client
const client = redis.createClient();

client.on('connect', () => {
    console.log('Redis client connected to the server');
});

client.on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err}`);
});

// Function to set key-value in redis server
const setAsync = promisify(client.set).bind(client);
const setNewSchool = async (schoolName, value) => {
    try {
        const reply = await setAsync(schoolName, value);
        console.log(`Reply: ${reply}`);
    } catch (err) {
        console.error('Error setting key:', err);
    }
}

// promisify client.get and clinet.set method
const getAsync = promisify(client.get).bind(client);

// Function to get value of key in redis server
const displaySchoolValue = async (schoolName) => {
    try {
        const value = await getAsync(schoolName);
        console.log(`${value}`);
    } catch (err) {
        console.error('Error getting key:', err);
    }
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
