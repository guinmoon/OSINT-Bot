const fs = require('fs');
const path = require('path');
var okapi = require('./okapi');
const random = require('random');

function run(login, password) {
    var auth = await okapi.get_auth(login, password);
}