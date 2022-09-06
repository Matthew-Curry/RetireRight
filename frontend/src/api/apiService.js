import auth from '../cognito/auth';
import router from '../router/router'

const BASE_URL = 'https://msgyw11a6d.execute-api.us-east-2.amazonaws.com'

function getUpdatedHeaders() {
    return {
        'Authorization': auth.auth.getSignInUserSession().getIdToken().jwtToken
    }
}

export default {
    userError: 'Unable to get user data. Please try again later.',

    getUser() {
        const headers = getUpdatedHeaders();
        return fetch(BASE_URL + '/test/users/', { headers: headers })
            .then(res => {
                if (res.ok) {
                    return res.json();
                } else if (res.status === 403) {
                    // auth expired, redirect to sign in
                    router.push('/login');
                    throw new Error('User was logged out, but authentication flow has been retriggered. Please try again');
                } else {
                    return this.userError;
                }
            })
            .then(data => {
                return data;
            })
            .catch((err) => {
                if (err.message != this.userError) {
                    return err.message;
                }
                return this.userError;
            });
    }
}
