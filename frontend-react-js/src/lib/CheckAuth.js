import { fetchAuthSession, getCurrentUser } from 'aws-amplify/auth';

const checkAuth = async (setUser) => {
  try {
    // Fetch the auth session (verifies the user is authenticated)
    const { tokens } = await fetchAuthSession();
    
    if (!tokens) {
      throw new Error("No tokens found - user not authenticated");
    }

    // Get the current user's attributes
    const cognito_user = await getCurrentUser();
    console.log('user', cognito_user);

    setUser({
      display_name: cognito_user.signInDetails?.loginId || 'Unknown',
      handle: cognito_user.username
    });
    
  } catch (err) {
    console.log('Auth error:', err);
  }
};

export default checkAuth;