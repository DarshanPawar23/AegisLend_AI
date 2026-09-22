import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCB2si0efDYe-N20dsP8PDNg8P13EfWvoQ",
  authDomain: "aegislend-ai.firebaseapp.com",
  projectId: "aegislend-ai",
  storageBucket: "aegislend-ai.firebasestorage.app",
  messagingSenderId: "1009997330597",
  appId: "1:1009997330597:web:4983c72a9b5c6ad3c0f54c",
  measurementId: "G-GK4YFF5KPM"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);