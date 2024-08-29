const Queue = require('kue').createQueue();
const { expect } = require('chai');
const sinon = require('sinon');

describe('createPushNotificationsJobs', () => {
    it('should log job progress and status', function(done) {
        const jobData = {
            phoneNumber: '4153518780',
            message: 'This is the code to verify your account'
        };

        const job = Queue.create('push_notification_code_3', jobData).save((err) => {
            if (!err) console.log(`Notification job ${job.id} completed`);
        });

        job.on('progress', function(progress) {
            console.log(`Notification job ${job.id} ${progress}% complete`);
        });

        job.on('complete', function() {
            console.log(`Notification job ${job.id} completed`);
            expect(true).to.be.true;
            done();
        });

        job.on('failed', function() {
            expect(true).to.be.false;
            done();
        });
    });
});
