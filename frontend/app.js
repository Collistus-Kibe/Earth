// --- FIREBASE CONFIGURATION ---
const firebaseConfig = {
    apiKey: "AIzaSyDX__F_8Y-E4IKXU1deMDloDDwQEfVcHcM",
    authDomain: "earth-aaa66.firebaseapp.com",
    projectId: "earth-aaa66",
    storageBucket: "earth-aaa66.firebasestorage.app",
    messagingSenderId: "619303358483",
    appId: "1:619303358483:web:039af3c04f766224552fe6",
    measurementId: "G-5H870QG1KJ"
};

// --- INIT FIREBASE ---
let app, auth, provider;

try {
    if (!firebase.apps.length) {
        app = firebase.initializeApp(firebaseConfig);
    } else {
        app = firebase.app();
    }
    auth = firebase.auth();
    provider = new firebase.auth.GoogleAuthProvider();
    console.log("🔥 Firebase Initialized.");
} catch(e) {
    console.error("Firebase Init Error:", e);
}

export { auth, provider };

// --- ROBUST AUTH LISTENER ---
export const whenAuthReady = new Promise((resolve) => {
    // Wait for DOM to be fully loaded first
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => listenForAuth(resolve));
    } else {
        listenForAuth(resolve);
    }
});

function listenForAuth(resolve) {
    auth.onAuthStateChanged((user) => {
        const loginOverlay = document.getElementById('login-overlay');
        const appContent = document.getElementById('app-content');
        const userDisplay = document.getElementById('user-email-display');

        // CRITICAL FIX: Do not crash if elements are missing
        if (!loginOverlay || !appContent) {
            console.warn("⚠️ DOM elements not ready. Retrying in 100ms...");
            setTimeout(() => listenForAuth(resolve), 100);
            return;
        }

        if (user) {
            console.log("✅ User logged in:", user.email);
            // Safe Class Toggling
            loginOverlay.classList.add('hidden');
            appContent.classList.remove('hidden');
            
            // Safe Text Update
            if(userDisplay) userDisplay.textContent = user.email;
            
            resolve(user);
        } else {
            console.log("❌ No user logged in.");
            loginOverlay.classList.remove('hidden');
            appContent.classList.add('hidden');
            resolve(null);
        }
    });
}

// --- LOGIN BUTTON LOGIC ---
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('btn-login-google');
    if (btn) {
        // Clone button to remove old listeners (prevents double-popup)
        const newBtn = btn.cloneNode(true);
        if(btn.parentNode) btn.parentNode.replaceChild(newBtn, btn);
        
        newBtn.addEventListener('click', () => {
            auth.signInWithPopup(provider).catch((error) => {
                console.error("Login Error:", error);
                alert("Login Error: " + error.message);
            });
        });
    }
});