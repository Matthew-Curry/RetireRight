/* eslint-disable */
import { CognitoAuth, StorageHelper } from 'amazon-cognito-auth-js';
import { router } from '../router';
import userInfoStore from './user-info-store';

const CLIENT_ID = process.env.VUE_APP_COGNITO_CLIENT_ID;
const APP_DOMAIN = process.env.VUE_APP_COGNITO_DOMAIN;
const REDIRECT_URI = process.env.VUE_APP_COGNITO_REDIRECT_URI;
const USER_POOL_ID = process.env.VUE_APP_COGNITO_USERPOOL_ID;
const USER_POOL_WEB_CLIENT_ID = process.env.VUE_APP_COGNITO_USERPOOL_WEB_CLIENT_ID;
const REDIRECT_URI_SIGNOUT = process.env.VUE_APP_COGNITO_REDIRECT_URI_SIGNOUT;

var authData = {
    ClientId: CLIENT_ID,
    AppWebDomain: APP_DOMAIN,
    TokenScopesArray: ['openid', 'email'],
    RedirectUriSignIn: REDIRECT_URI,
    RedirectUriSignOut: REDIRECT_URI_SIGNOUT,
    UserPoolId: USER_POOL_ID,
    userPoolWebClientId: USER_POOL_WEB_CLIENT_ID
}

var auth = new CognitoAuth(authData);

auth.userhandler = {
    onSuccess: function () {
        userInfoStore.setLoggedIn(true);
        router.push('/')
    },

    onFailure: function (err) {
        userInfoStore.setLoggedOut();
        router.go({
            path: '/error',
            query: {
                message: 'Login failed due to ' + err
            }
        });
    }
};

function getUserInfo() {
    var jwtToken = auth.getSignInUserSession().getAccessToken().jwtToken;
    const USERINFO_URL = 'http://' + auth.getAppWebDomain() + '/oauth2/userInfo';
    var requestData = {
        headers: {
            'Authorization': 'Bearer ' + jwtToken,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }

    return fetch(USERINFO_URL, requestData).then(res => res.json())

}

function getUserInfoStorageKey() {
    var keyPrefix = 'CognitoIdentityServiceProvider.' + auth.getClientId();
    var tokenUserName = auth.signInUserSession.getAccessToken().getUsername();
    var userInfoKey = keyPrefix + '.' + tokenUserName + '.userInfo';

    return userInfoKey;
}

var storageHelper = new StorageHelper();
var storage = storageHelper.getStorage();

export default {
    auth: auth,
    login() {
        auth.getSession();
    },
    logout() {
        if (auth.isUserSignedIn()) {
            var userInfoKey = this.getUserInfoStorageKey();
            auth.signOut();

            storage.removeItem(userInfoKey);
        }
    },
    getUserInfoStorageKey,
    getUserInfo
}
