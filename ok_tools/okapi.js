const request = require('request');

var get_auth = async function(login, password) {
    var options = {
        'method': 'POST',
        'url': 'https://api.ok.ru/api/batch/executeV2',
        'headers': {
            'User-Agent': 'OKAndroid/20.4.20 b614 (Android 7.0; en_US; Android Custom Phone Build/vbox86p-userdebug 7.0 NRD90M 391 test-keys; xhdpi 320dpi 720x1184)',
            'Accept': 'application/json',
            'Transfer-Encoding': 'chunked',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        form: {
            'application_key': 'CBAFJIICABABABABA',
            'auth.login': '',
            'methods': `[\n    {\n        "auth.login": {\n            "params": {\n                "client": "android_8_20.4.20",\n                "deviceId": "INSTALL_ID=030b17c2-f51d-4641-b860-c9230a751ec5;ANDROID_ID=84949fde69b77119;",\n                "gen_token": true,\n                "password": "${password}",\n                "user_name": "${login}",\n                "verification_supported": true,\n                "verification_supported_v": "3"\n            }\n        }\n    }\n]`
        }
    };
    return new Promise((resolve, reject) => {
        request(options, function(error, response) {
            if (error) throw new Error(error);
            resolve(JSON.parse(response.body));
        });
    });
}

var get_friends = async function(uid, session_key) {
    var options = {
        'method': 'GET',
        'url': `https://api.ok.ru/api/friends/get?application_key=CBAFJIICABABABABA&client=android_8_16.9.27&fid=${uid}&session_key=${session_key}`,
        'headers': {
            'Accept': 'application/json',
            'User-Agent': 'OKAndroid/16.9.27 b231 (Android 7.0; en_US; Android Custom Build/vbox86p-userdebug; xhdpi 320dpi 720x1184)',
            'Host': 'api.ok.ru',
            'Connection': 'Keep-Alive',
            'Cookie': 'bci=-3218965118927310717; _statid=b877bcdf-b9bd-40d6-9715-53452ec7df84'
        }
    };
    return new Promise((resolve, reject) => {
        request(options, function(error, response) {
            if (error) throw new Error(error);
            resolve(JSON.parse(response.body));
        });
    });
}

var get_users_info = async function(uids, session_key) {
    var uid_str = '';
    if (uids != undefined) {
        for (var i = 0; i < uids.length; i++) {
            uid_str += uids[i];
            if (i < uids.length - 1)
                uid_str += '%2C';
        }
    }
    var options = {
        'method': 'GET',
        'url': `https://api.ok.ru/api/users/getInfo?application_key=CBAFJIICABABABABA&client=android_8_16.9.27&emptyPictures=false&fields=last_name%2Cname%2Cfirst_name%2Cpic190x190%2Conline%2Clast_online_ms%2Cpic190x190%2Cpic_full%2Cshow_lock%2Cbirthday%2Cgender%2Ccan_vcall%2Cprivate%2Ccan_vmail&session_key=${session_key}&uids=${uid_str}`,
        'headers': {
            'Accept': 'application/json',
            'User-Agent': 'OKAndroid/16.9.27 b231 (Android 7.0; en_US; Android Custom Build/vbox86p-userdebug; xhdpi 320dpi 720x1184)',
            'Host': 'api.ok.ru',
            'Connection': 'Keep-Alive',
            'Cookie': 'bci=-3218965118927310717; _statid=b877bcdf-b9bd-40d6-9715-53452ec7df84'
        }
    };
    return new Promise((resolve, reject) => {
        request(options, function(error, response) {
            if (error) throw new Error(error);
            resolve(JSON.parse(response.body));
        });
    });
}



var get_accounts_by_phones = async function(query, session_key) {
    //{"credentials":[{"firstName":"Adriana","lastName":"Poetter","phone":" 992938808418","hasAvatar":false,"hasRingtone":false,"isFavorite":false}]}
    var options = {
        'method': 'POST',
        'url': 'https://api.ok.ru/api/search/byContactsBook',
        'headers': {
            'User-Agent': 'OKAndroid/20.4.20 b614 (Android 7.0; en_US; Android Custom Phone Build/vbox86p-userdebug 7.0 NRD90M 391 test-keys; xhdpi 320dpi 720x1184)',
            'Accept': 'application/json',
            'Transfer-Encoding': 'chunked',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        form: {
            '__screen': 'friends,feed_main',
            'application_key': 'CBAFJIICABABABABA',
            'fields': 'user.url_profile,user.age,user.last_name,user.pic600x600,user.pic128x128,user.gender,user.location,user.uid,user.first_name,user.online,birthday',
            'session_key': `${session_key}`,
            'query': `${query}`
        }
    };
    return new Promise((resolve, reject) => {
        request(options, function(error, response) {
            if (error) throw new Error(error);
            resolve(JSON.parse(response.body));
        });
    });
}

var get_photo_urls = async function(session_key, uid, max_count) {
    var options = {
        'method': 'POST',
        'url': 'https://api.ok.ru/api/batch/executeV2',
        'headers': {
            'User-Agent': 'OKAndroid/20.4.20 b614 (Android 7.0; en_US; Android Custom Phone Build/vbox86p-userdebug 7.0 NRD90M 391 test-keys; xhdpi 320dpi 720x1184)',
            'Accept': 'application/json',
            'Transfer-Encoding': 'chunked',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        form: {
            'application_key': 'CBAFJIICABABABABA',
            'session_key': session_key,
            'methods': `[{"photos.getPhotos":{"params":{"aid":"stream","count":${max_count},"detectTotalCount":"true","fid":"${uid}","fields":"photo.pic_max"}}}]`
        }
    };
    return new Promise((resolve, reject) => {
        request(options, function(error, response) {
            if (error) throw new Error(error);
            resolve(JSON.parse(response.body));
        });
    });
}

var get_users_status = async function(session_key, uids) {
    var uids_str = '';
    for (var i = 0; i < uids.length; i++) {
        uids_str += uids[i];
        if (i < uids.length - 1)
            uids_str += ',';
    }
    var options = {
        'method': 'POST',
        'url': 'https://api.ok.ru/api/batch/executeV2',
        'headers': {
            'User-Agent': 'OKAndroid/20.4.20 b614 (Android 7.0; en_US; Android Custom Phone Build/vbox86p-userdebug 7.0 NRD90M 391 test-keys; xhdpi 320dpi 720x1184)',
            'Accept': 'application/json',
            'Transfer-Encoding': 'chunked',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        form: {
            'application_key': 'CBAFJIICABABABABA',
            'session_key': session_key,
            'methods': `[{"users.getInfo": {"params": {"fields": "name,last_online","uids": "${uids_str}"}}}]`
        }
    };
    return new Promise((resolve, reject) => {
        request(options, function(error, response) {
            if (error) throw new Error(error);
            resolve(JSON.parse(response.body));
        });
    });
}


var get_recovery_phone = async function(profile_url_id) {
    var options = {
        'method': 'POST',
        'url': 'https://ok.ru/dk',
        'headers': {
            'authority': 'ok.ru',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'strd': 'false',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'tkn': 'undefined',
            'origin': 'https://ok.ru',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://ok.ru/',
            'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,ru;q=0.7',
            'cookie': 'viewport=1057; _lastSmsForCodeTime_password=; bci=-3218965118927310717; _statid=b877bcdf-b9bd-40d6-9715-53452ec7df84; JSESSIONID=98be89eea4f1e4db160c664be815496f2946e88abf1c5cef.bef3488'
        },
        body: "st.recoveryData=" + profile_url_id + "&st.ccode=&st.recoveryMethod=Link&st.registrationAction=ValidateLink&st.cmd=anonymPasswordRecoveryNew&cmd=AnonymPasswordRecoveryNew&gwt.requested=da69c7ebT1598879267705"

    };
    return new Promise((resolve, reject) => {
        request(options, function(error, response) {
            if (error) throw new Error(error);
            var JSESSIONID = "JSESSIONID=98be89eea4f1e4db160c664be815496f2946e88abf1c5cef.bef3488";
            if (response.headers["set-cookie"] != undefined) {
                response.headers["set-cookie"].forEach(cookie => {
                    if (cookie.indexOf("JSESSIONID") >= 0) {
                        JSESSIONID = cookie;
                    }
                });
            }
            var options = {
                'method': 'GET',
                'url': 'https://ok.ru/dk?st.cmd=anonymPasswordRecoveryNew&st.registrationAction=ChooseCodeDestination&st.recoveryMethod=Link',
                'headers': {
                    'authority': 'ok.ru',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'referer': 'https://ok.ru/',
                    'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,ru;q=0.7',
                    'cookie': `viewport=1057; _lastSmsForCodeTime_password=; bci=-3218965118927310717; _statid=b877bcdf-b9bd-40d6-9715-53452ec7df84; ${JSESSIONID}`
                }
            };
            request(options, function(error, response) {
                if (error) throw new Error(error);
                var body = response.body;
                var phrase = "<div>Via SMS +";
                var phrase2 = "****";
                var phrase_ind = body.indexOf(phrase);
                if (phrase_ind < 0) {
                    resolve(false);
                }
                var body_part1 = body.substring(phrase_ind + phrase.length)
                var phrase2_ind = body_part1.indexOf(phrase2);
                if (phrase2_ind < 0) {
                    resolve(false);
                }
                var number = body_part1.substring(0, phrase2_ind);
                resolve(number);
            });
        });
    });
}



exports.get_auth = get_auth;
exports.get_users_info = get_users_info;
exports.get_friends = get_friends;
exports.get_accounts_by_phones = get_accounts_by_phones;
exports.get_photo_urls = get_photo_urls;
exports.get_users_status = get_users_status;
exports.get_recovery_phone = get_recovery_phone;