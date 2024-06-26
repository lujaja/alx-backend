import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', () => {
  let queue;

  beforeEach(() => {
    queue = kue.createQueue();
    queue.testMode.enter(); // Enter test mode
  });

  afterEach(() => {
    queue.testMode.clear(); // Clear the queue
    queue.testMode.exit(); // Exit test mode
  });

  it('should display an error message if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs('not an array', queue)).to.throw('Jobs is not an array');
  });

  it('should create two new jobs to the queue', () => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
      { phoneNumber: '4153518781', message: 'This is the code 4562 to verify your account' }
    ];

    createPushNotificationsJobs(jobs, queue);

    expect(queue.testMode.jobs.length).to.equal(2);

    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[0].data).to.eql(jobs[0]);

    expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[1].data).to.eql(jobs[1]);
  });

  it('should log correct job creation, completion, failure, and progress messages', (done) => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' }
    ];

    const log = [];
    console.log = (msg) => log.push(msg); // Capture console.log output

    createPushNotificationsJobs(jobs, queue);

    queue.testMode.jobs[0].emit('complete');
    queue.testMode.jobs[0].emit('failed', new Error('Job failed'));
    queue.testMode.jobs[0].emit('progress', 50);

    setTimeout(() => {
      expect(log).to.include(`Notification job created: #${queue.testMode.jobs[0].id}`);
      expect(log).to.include(`Notification job #${queue.testMode.jobs[0].id} completed`);
      expect(log).to.include(`Notification job #${queue.testMode.jobs[0].id} failed: Error: Job failed`);
      expect(log).to.include(`Notification job #${queue.testMode.jobs[0].id} 50% complete`);
      done();
    }, 1000);
  });
});
