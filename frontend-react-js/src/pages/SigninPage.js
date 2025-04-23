import './SigninPage.css';
import React from "react";
import {ReactComponent as Logo} from '../components/svg/logo.svg';
import { Link } from "react-router-dom";
import { signIn } from 'aws-amplify/auth'
import { Amplify } from 'aws-amplify';

import { fetchAuthSession } from 'aws-amplify/auth';

// [TODO] Authenication
import Cookies from 'js-cookie'
try {
  Amplify.configure({
    Auth: {
      Cognito: {
        userPoolClientId: '5ou33i17bgh351k5bi7eff8h5u',
        userPoolId: 'us-east-1_unxV9N09n',
          username: 'true',
          email:true
         
      }

    }
  });
} catch (error) {
  console.log(error.message)
}

export default function SigninPage() {

 
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [errors, setErrors] = React.useState('');


  const onsubmit = async (event) => {
    
    setErrors('')
    event.preventDefault();
      await signIn({username:email, password:password})
        .then(user => {
          console.log(user )

        })
        .catch(err => { 
          if (err.code == 'UserNotConfirmedException') {
            window.location.href = "/confirm"
          }

        


          console.log(err)
          setErrors(err.message)
         }
        );    
        const session = await fetchAuthSession();
        localStorage.setItem("access_token",session.tokens.accessToken)
        window.location.href = "/"


    return false
  }

  const email_onchange = (event) => {
    setEmail(event.target.value);
  }
  const password_onchange = (event) => {
    setPassword(event.target.value);
  }

  let el_errors;
  if (errors){
    el_errors = <div className='errors'>{errors}</div>;
  }

  return (
    <article className="signin-article">
      <div className='signin-info'>
        <Logo className='logo' />
      </div>
      <div className='signin-wrapper'>
        <form 
          className='signin_form'
          onSubmit={onsubmit}
        >
          <h2>Sign into your Cruddur account</h2>
          <div className='fields'>
            <div className='field text_field username'>
              <label>Email</label>
              <input
                type="text"
                value={email}
                onChange={email_onchange} 
              />
            </div>
            <div className='field text_field password'>
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={password_onchange} 
              />
            </div>
          </div>
          {el_errors}
          <div className='submit'>
            <Link to="/forgot" className="forgot-link">Forgot Password?</Link>
            <button type='submit'>Sign In</button>
          </div>

        </form>
        <div className="dont-have-an-account">
          <span>
            Don't have an account?
          </span>
          <Link to="/signup">Sign up!</Link>
        </div>
      </div>

    </article>
  );
}