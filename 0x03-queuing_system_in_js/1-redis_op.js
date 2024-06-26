// import redis
import redis from 'redis';

//create a redis client
const client = redis.createClient();

client.on('connect', () => {
    console.log('Redis client connected to the server');
});

client.on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err}`);
})


// Function to set key-value in redis server
const setNewSchool = (schoolName, value) => {
    client.set(schoolName, value, redis.print);
}

// Function to display value of key in redis server
const displaySchoolValue = (schoolName) => {
    client.get(schoolName, (err, reply) => {
        if (err) {
            console.log(err);
        } else {
            console.log(reply);
        }
        
    });
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
