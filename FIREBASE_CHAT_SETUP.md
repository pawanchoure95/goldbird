# Firebase Premium Chat Setup (Shaadi-Style Real-Time)

## 1. Create Firebase project
1. Open Firebase Console and create/select project.
2. Enable `Authentication` -> `Sign-in method` -> enable `Custom`.
3. Enable `Cloud Firestore` in production mode.

## 2. Add Web App credentials
1. In Firebase project settings, create a web app.
2. Copy these values into `.env`:

```env
FIREBASE_CHAT_ENABLED=True
FIREBASE_API_KEY=your_api_key
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
FIREBASE_MEASUREMENT_ID=your_measurement_id
FIREBASE_SERVICE_ACCOUNT_PATH=D:\path\to\firebase-service-account.json
```

## 3. Service account (for secure custom token auth)
1. Firebase Console -> Project Settings -> Service Accounts.
2. Generate private key JSON.
3. Save file outside public folders.
4. Set `FIREBASE_SERVICE_ACCOUNT_PATH` to that JSON path.

## 4. Install dependencies
```bash
pip install -r requirements.txt
```

## 5. Firestore security rules (required)
Use these rules to ensure only room participants can read/write chat:

```text
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    function isSignedIn() {
      return request.auth != null;
    }

    function inParticipants(roomId) {
      return isSignedIn()
        && request.auth.uid in get(/databases/$(database)/documents/chatRooms/$(roomId)).data.participants;
    }

    match /chatRooms/{roomId} {
      allow read: if inParticipants(roomId);
      allow create: if isSignedIn()
        && request.resource.data.participants is list
        && request.auth.uid in request.resource.data.participants;
      allow update: if inParticipants(roomId);

      match /messages/{messageId} {
        allow read: if inParticipants(roomId);
        allow create: if inParticipants(roomId)
          && request.resource.data.senderUid == request.auth.uid
          && request.resource.data.text is string
          && request.resource.data.text.size() > 0
          && request.resource.data.text.size() <= 500;
      }
    }

    match /presence/{uid} {
      allow read: if isSignedIn();
      allow write: if isSignedIn() && request.auth.uid == uid;
    }
  }
}
```

## 6. How match-based chat access works in this code
- Room ID format: `minUserId_maxUserId` (example: `3_17`).
- A user can chat only if both users liked each other.
- Django routes enforce match access:
  - `/accounts/chat/`
  - `/accounts/chat/<username>/`
- Firebase token endpoint (authenticated): `/accounts/chat-api/token/`

## 7. Production checklist
1. Set strong `SECRET_KEY` and `DEBUG=False`.
2. Restrict `ALLOWED_HOSTS` to real domains.
3. Use HTTPS only.
4. Keep Firebase service-account JSON private.
5. Monitor Firestore usage and add quotas/alerts.
