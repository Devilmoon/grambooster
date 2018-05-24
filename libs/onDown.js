'use strict';

const fetch = require('node-fetch');

const myInstagram = "https://www.instagram.com/liberato1926/";
const who = "liberato1926";

let lastPic;

const onDown = async () =>
{
    try
    {
        const res = await fetch(myInstagram);
        const html = await res.text();
        const what = /\"display_url\":\"(.+?\.jpg)/.exec(html);
        if(lastPic != what)
        {
            lastPic = what;
            return { who, what };
        }
    }
    catch(err)
    {
        console.log(err);
    }
}

module.exports = onDown;
