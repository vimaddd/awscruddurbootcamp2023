import './App.css';

import HomeFeedPage from './pages/HomeFeedPage';
import UserFeedPage from './pages/UserFeedPage';
import NotificationFeedPage from './pages/NotificationFeedPage';
import SignupPage from './pages/SignupPage';
import SigninPage from './pages/SigninPage';
import RecoverPage from './pages/RecoverPage';
import MessageGroupsPage from './pages/MessageGroupsPage';
import MessageGroupPage from './pages/MessageGroupPage';
import ConfirmationPage from './pages/ConfirmationPage';
import React from 'react';
import process from 'process';
import { Amplify } from 'aws-amplify';
import {
  createBrowserRouter,
  RouterProvider
} from "react-router-dom";

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
  console.log(error)
}


const router = createBrowserRouter([
  {
    path: "/",
    element: <HomeFeedPage />
  },
  {
    path: "/notifications",
    element: <NotificationFeedPage />
  },
  {
    path: "/@:handle",
    element: <UserFeedPage />
  },
  {
    path: "/messages",
    element: <MessageGroupsPage />
  },
  {
    path: "/messages/@:handle",
    element: <MessageGroupPage />
  },
  {
    path: "/signup",
    element: <SignupPage />
  },
  {
    path: "/signin",
    element: <SigninPage />
  },
  {
    path: "/confirm",
    element: <ConfirmationPage />
  },
  {
    path: "/forgot",
    element: <RecoverPage />
  }
]);

function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;