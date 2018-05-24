'use strict';

const net = require('net');
const onData = require('./onData');
const onDown = require('./onDown');
const { sleep } = require('./utils');

const socket = net.connect( async () =>
{
    try
    {
        console.log('server connected at', socket.remoteAddress);

        socket.on('data', data => onData(data) );
        socket.on('error', error => console.log(error.code) );
        socket.on('end', (data) => { console.log('Socket end event'); process.exit(0) } );
    
        while(true)
        {
            const data = await onDown();
            socket.write(data);
            await sleep(5000);
        }
    }
    catch(err)
    {
        console.log(err);
    }
});