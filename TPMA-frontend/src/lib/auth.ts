/***
    localStorage based auth with RBAC support using jsrsasign 
*/

import { KJUR, b64utoutf8 } from 'jsrsasign';
import CryptoJS from 'crypto-js';
import axios from 'axios';
import { API_BASE_URL } from './config';

const ENCRYPTION_KEY = 'TPMA@M2025';

// Valid roles for RBAC
export const ROLES = {
  TRAINEE: 'trainee',
  SUPERVISOR: 'supervisor',
  ADMINISTRATOR: 'administrator',
} as const;

type Role = typeof ROLES[keyof typeof ROLES];

// Function to check if the user is logged in
export const auth_isLoggedIn = (): boolean => {
  const token = localStorage.getItem('access_token');
  return !!token;
};

// Function to clear all localStorage data
export const clearLocalStorage = (): void => {
  localStorage.clear();
};




// // Function to log out the user
// export const logout = (): void => {
//   clearLocalStorage();
// };
export const logout = (): void => {
  clearLocalStorage();
  document.cookie = "access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Lax";
  document.cookie = "user_role=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Lax";
};




// Function to encrypt data
const encryptData = (data: any): string => {
  const encrypted = CryptoJS.AES.encrypt(JSON.stringify(data), ENCRYPTION_KEY).toString();
  return encrypted;
};

// Function to decrypt data 
const decryptData = (encryptedData: string): any => {
  try {
    const decryptedBytes = CryptoJS.AES.decrypt(encryptedData, ENCRYPTION_KEY);
    const decryptedText = decryptedBytes.toString(CryptoJS.enc.Utf8);
    return decryptedText ? JSON.parse(decryptedText) : null;
  } catch (error) {
    console.error('Error decrypting data:', error);
    return null;
  }
};

// Function to save the access token in localStorage
export const setAccessToken = (token: string): void => {
  const encryptedToken = encryptData(token);
  localStorage.setItem('access_token', encryptedToken);
};

// Function to get the access token from localStorage
export const getAccessToken = (): string | null => {
  const encryptedToken = localStorage.getItem('access_token');
  return encryptedToken ? decryptData(encryptedToken) : null;
};

// Function to save the refresh token in localStorage
export const setRefreshToken = (token: string): void => {
  const encryptedToken = encryptData(token);
  localStorage.setItem('refresh_token', encryptedToken);
};

// Function to get the refresh token from localStorage
export const getRefreshToken = (): string | null => {
  const encryptedToken = localStorage.getItem('refresh_token');
  return encryptedToken ? decryptData(encryptedToken) : null;
};

// Function to save the user data in localStorage
export const setUserData = (user: any): void => {
  const encryptedUser = encryptData(user || {});
  localStorage.setItem('user', encryptedUser);
};

// Function to save the user profile data in localStorage
export const setProfileData = (profile: any): void => {
  if (profile?.permission_groups && profile?.permissions) {
    const allPermissions = [...(profile.permissions || []), ...(profile.permission_groups || []).reduce((acc: any[], group: any) => acc.concat(group.permissions || []), [])];
    const uniquePermissions = allPermissions.filter((p: any, i: number, self: any[]) => self.findIndex((sp: any) => sp.id === p.id) === i);
    localStorage.setItem('permissions', encryptData(uniquePermissions));
  }
  localStorage.setItem('profile', encryptData(profile || {}));
};

// Function to get the user data from localStorage
export const getUserData = (): any | null => {
  const encryptedUser = localStorage.getItem('user');
  return encryptedUser ? decryptData(encryptedUser) : null;
};

// Function to get the user profile data from localStorage
export const getProfileData = (): any | null => {
  const encryptedProfile = localStorage.getItem('profile');
  return encryptedProfile ? decryptData(encryptedProfile) : null;
};

// Set enrollment data for trainee
const setTraineeEnrollmentData = async (profileId: string): Promise<void> => {
  try {
    const accessToken = getAccessToken();
    const url = `${API_BASE_URL}/academy/trainees/${profileId}/enrollment/`;
    const response = await axios.get(url, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    localStorage.setItem('enrollment', encryptData(response.data));
  } catch (error) {
    console.error('Error fetching enrollment data:', error);
  }
};

// Set enrollment data for supervisor
const setSupervisorEnrollmentData = (enrollment: any): void => {
  localStorage.setItem('enrollment', encryptData(enrollment || {}));
};

// Function to get the enrollment data from localStorage
export const getEnrollmentData = (): any | null => {
  const encryptedData = localStorage.getItem('enrollment');
  return encryptedData ? decryptData(encryptedData) : null;
};


export const saveLoginResponse = (data: any): void => {
  const { access, refresh, user, profile, enrollment } = data;
  setAccessToken(access);
  setRefreshToken(refresh);
  setUserData(user);
  if (user?.role === ROLES.SUPERVISOR && enrollment) {
    setSupervisorEnrollmentData(enrollment);
  }
  if (profile) {
    setProfileData(profile);
    if (user?.role === ROLES.TRAINEE && profile.id) {
      setTraineeEnrollmentData(profile.id);
    }
  } else {
    setProfileData({});
  }
};

export const getUserRole = (): Role | null => {
  const user = getUserData();
  if (user && typeof user === 'object' && 'role' in user && Object.values(ROLES).includes(user.role)) {
    return user.role as Role;
  }
  return null;
};






// Function to get the user's ID from localStorage
export const getUserId = (): string | null => {
  const user = getUserData();
  if (user && typeof user === 'object' && 'id' in user) {
    return user.id;
  }
  return null;
};

// Function to check if logged user has a permission
export const hasPermission = (codename: string): boolean => {
  const role = getUserRole();
  if (role === ROLES.ADMINISTRATOR) return true; // Admins have all permissions
  const encryptedPermissions = localStorage.getItem('permissions');
  if (!encryptedPermissions) return false;
  const permissions = decryptData(encryptedPermissions);
  if (!permissions) return false;
  return permissions.some((p: any) => p.codename === codename);
};

// Function to save tokens in localStorage
export const saveTokens = (data: { access: string; refresh: string }): void => {
  setAccessToken(data.access);
  setRefreshToken(data.refresh);
};

// Function to check if the access token is still valid
export const checkTokenValidity = async (): Promise<boolean> => {
  const accessToken = getAccessToken();
  if (accessToken) {
    try {
      await axios.post(`${API_BASE_URL}/token/verify/`, { token: accessToken });
      return true;
    } catch (error) {
      return false;
    }
  }
  return false;
};

// Function to refresh the tokens
export const refreshTokens = async (): Promise<string | null> => {
  const refreshToken = getRefreshToken();
  if (refreshToken) {
    try {
      const response = await axios.post(`${API_BASE_URL}/token/refresh/`, { refresh: refreshToken });
      saveTokens(response.data);
      return response.data.access;
    } catch (error) {
      console.error('Error refreshing tokens:', error);
      return null;
    }
  }
  return null;
};

// Utility functions for file links
export const getFileLink = (file_id: string): string => {
  return `https://drive.google.com/uc?export=view&id=${file_id}`;
};

export const getFileLink2 = (file_id: string): string => {
  return `https://drive.google.com/file/d/${file_id}/view`;
};