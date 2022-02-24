const fs = require('fs');
const path = require('path');
var okapi = require('./okapi');
const random = require('random');

var Target_Phone = '';
var command_args = process.argv.slice(2);
var Auths = {};
var Current_Auth_LP = {}
var current_auth_id = 0;
var only_json_out = false;
var names = fs.readFileSync('names.txt').toString().split("\n");
var families = fs.readFileSync('families.txt').toString().split("\n");
var Config = {
    auth: {}
}

function isEmptyObject(obj) {
    return !Object.keys(obj).length;
}

function msleep(n) {
    Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, n);
}

function sleep(n) {
    msleep(n * 1000);
}

var get_new_auth_by_id = async function() {
    Current_Auth_LP.Login = Auths[current_auth_id].Login;
    Current_Auth_LP.Password = Auths[current_auth_id].Password;
    Config.auth = await okapi.get_auth(Current_Auth_LP.Login, Current_Auth_LP.Password);
    if (Config.auth.error_msg != undefined)
        return false;
    Config.auth = Config.auth[0].ok;
    if (!only_json_out)
        console.log(`***************\nGetted new auth ${Auths[current_auth_id].Login}: ${Config.auth.session_key}\n**********\n`)
}

var do_query = async function(query, parrent_id) {
    var Accs_returned = false;
    while (!Accs_returned) {
        var Accs = await okapi.get_accounts_by_phones(query, Config.auth.session_key);
        //****LIMITS****
        if (Accs != undefined && Accs.error_code != undefined) {
            // sleep.sleep(Config.cur_long_delay);
            if ((current_auth_id + 1) < Auths.length) {
                current_auth_id++;
                await get_new_auth_by_id();
                success_count = 0;
            } else {
                current_auth_id = 0;
                if (!only_json_out)
                    console.log(`sleep ${3600} for LIMIT_REACHED reason\n`);
                sleep(3600);
            }
        } else {
            Accs_returned = true;
        }
    }
    var users_count = 0;
    if (Accs.users != undefined)
        users_count = Accs.users.length;
    if (!only_json_out)
        console.log(`SUCCESS [RESP]Accs(${users_count})\n********************\n`);
    if (Accs == undefined || isEmptyObject(Accs) || users_count == 0) {
        return false;
    }
    return Accs;
}

var run = async function() {
    // console.log(command_args)
    if (command_args[1] == "true")
        only_json_out = true
    var authsPath = path.join(__dirname, "auths.json");
    if (fs.existsSync(authsPath)) {
        Auths = JSON.parse(fs.readFileSync(authsPath, "utf8"));
    }
    if (Auths.auths == undefined || Auths.auths.length < 1) {
        if (!only_json_out)
            console.log("Auths not found!");
        return;
    }
    if (command_args.length >= 1) {
        Target_Phone = command_args[0];
    } else {
        if (!only_json_out)
            console.log("Invalid argument");
        return;
    }
    Auths = Auths.auths;
    await get_new_auth_by_id();
    var query = { credentials: [] };
    var name = names[random.int(0, names.length)]
    var family = families[random.int(0, families.length)]
    var number = Target_Phone;
    var credential = {
        "firstName": name,
        "lastName": family,
        "phone": number,
        "hasAvatar": false,
        "hasRingtone": false,
        "isFavorite": false
    }
    query.credentials.push(credential);
    var result = await do_query(JSON.stringify(query), 0);
    console.log(JSON.stringify(result));
}

run();