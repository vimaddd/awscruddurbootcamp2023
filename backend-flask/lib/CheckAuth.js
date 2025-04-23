import { fetchAuthSession, getCurrentUser, fetchUserAttributes } from 'aws-amplify/auth';

const checkAuth = async (setUser) => {
  try {
    // Check if user is authenticated
    const { tokens } = await fetchAuthSession();
    if (!tokens) {
      throw new Error("No authentication tokens found");
    }

    // Get the current user's basic info
    const cognitoUser = await getCurrentUser();
    console.log('user', cognitoUser);

    // Fetch additional user attributes
    const attributes = await fetchUserAttributes();
    
    setUser({
      display_name: attributes.name || cognitoUser.username,
      handle: attributes.preferred_username || cognitoUser.username
    });

  } catch (err) {
    console.error("Authentication error:", err);
    // Optional: set user to null or handle error state
    // setUser(null);
  }
};

export default checkAuth;