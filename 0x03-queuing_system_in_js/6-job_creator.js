// Import Kue
import kue from 'kue';

// Create queue
const queue = kue.createQueue();

const jobData = {
    phoneNumber: '4153518780',
    message: 'This is the code to verify your account'
}

// creat a job
const job = queue.create(
    'push_notification_code',
    jobData
).save((err) => {
    if (!err) {
        console.log(`Notification job created: ${job.id}`);
    } else {
        console.error(`Notification job failed`);
    }
})
