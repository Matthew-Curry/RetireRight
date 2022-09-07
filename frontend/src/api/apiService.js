import auth from '../cognito/auth';
import { router } from '../router/router'

const BASE_URL = 'https://msgyw11a6d.execute-api.us-east-2.amazonaws.com'
const USER_URL = BASE_URL + '/test/users/'
//const SCENARIO_URL = USER_URL + '/scenarios/'

function getUpdatedHeaders() {
    return {
        'Authorization': auth.auth.getSignInUserSession().getIdToken().jwtToken
    }
}

// reads response data, throws errors as needed
function processLogic(res, errMsg) {
    if (res.ok) {
        return res.json();
    } else if (res.status === 403) {
        // auth expired, redirect to sign in
        router.push('/login');
        throw new Error('User was logged out, but authentication flow has been retriggered. Please try again');
    } else {
        throw new Error(errMsg);
    }
}

// function to run after recieving a response from fetch wrapper to get the data
function processResponse(resPair) {
    const [res, errMsg] = resPair

    return processLogic(res, errMsg).then(data => {
        return data;
    })

}

// wraps the fetch API so the application error message can be tied to the API call
// should a general error be raised
function fetchWrapper(url, options, errMsg) {
    return new Promise((resolve, reject) => {
        fetch(url, options)
        .then((res) => {
            resolve([res, errMsg])
        })
        .catch((err) => {
            reject(err)
        })
    })
}

export default {
    userGetError: 'Unable to get user data. Please try again later.',
    userPatchError: 'Unable to update the user data. Please try again later',

    getUser() {
        const headers = getUpdatedHeaders();
        const options = { headers: headers }

        return fetchWrapper(USER_URL, options, this.userGetError)
            .then(processResponse)
            .catch((err) => {
                return err.message
            })
    },

    patchUser(patchValues) {
        let headers = getUpdatedHeaders();
        headers['Content-Type'] = 'application/json';
        const options = {
            headers: headers,
            method: 'PATCH',
            body: JSON.stringify(patchValues)
        }

        return fetchWrapper(USER_URL, options, this.userPatchError)
        .then(processResponse)
        .catch((err) => {
            return err.message
        })
    }
}
