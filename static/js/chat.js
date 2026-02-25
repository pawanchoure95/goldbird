(function () {
  const bootstrapNode = document.getElementById("chat-bootstrap");
  if (!bootstrapNode) return;

  const data = JSON.parse(bootstrapNode.textContent || "{}");
  const firebaseEnabled = !!data.firebaseEnabled;
  const selectedUser = data.selectedUser;
  const currentUser = data.currentUser || {};
  const matches = data.matches || [];

  const messageList = document.getElementById("messageList");
  const typingIndicator = document.getElementById("typingIndicator");
  const form = document.getElementById("chatForm");
  const input = document.getElementById("messageInput");
  const activeStatus = document.getElementById("activeStatus");

  if (!firebaseEnabled) {
    showSystemMessage(
      "Chat is configured in UI but Firebase is not enabled on server. Follow setup steps to activate real-time chat."
    );
    if (form) form.style.display = "none";
    return;
  }

  if (!selectedUser || !messageList || !form || !input) return;

  const allowedRoomIds = new Set(matches.map((m) => m.roomId));
  const roomId = selectedUser.roomId;

  if (!allowedRoomIds.has(roomId)) {
    showSystemMessage("Unauthorized room access blocked.");
    form.style.display = "none";
    return;
  }

  if (!window.firebase) {
    showSystemMessage("Firebase SDK failed to load.");
    form.style.display = "none";
    return;
  }

  const app = firebase.apps.length ? firebase.app() : firebase.initializeApp(data.firebaseConfig || {});
  const auth = firebase.auth(app);
  const db = firebase.firestore(app);

  const roomRef = db.collection("chatRooms").doc(roomId);
  const messagesRef = roomRef.collection("messages");
  const myPresenceRef = db.collection("presence").doc(String(currentUser.uid));
  const partnerPresenceRef = db.collection("presence").doc(String(selectedUser.id));

  let typingTimer = null;
  let isTyping = false;

  authenticate()
    .then(() => Promise.all([ensureRoomMetadata(), setPresence(true), subscribePresence(), subscribeMessages()]))
    .catch((err) => {
      showSystemMessage(`Failed to start chat: ${err.message || "Unknown error"}`);
      form.style.display = "none";
    });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = sanitize(input.value);
    if (!text) return;

    try {
      await messagesRef.add({
        text: text,
        senderUid: String(currentUser.uid),
        senderUsername: currentUser.username,
        senderName: currentUser.fullName || currentUser.username,
        senderProfilePicture: currentUser.profilePicture || "",
        createdAt: firebase.firestore.FieldValue.serverTimestamp(),
      });

      await roomRef.set(
        {
          participants: [String(currentUser.uid), String(selectedUser.id)].sort(),
          participantUsernames: [currentUser.username, selectedUser.username].sort(),
          updatedAt: firebase.firestore.FieldValue.serverTimestamp(),
          lastMessage: text.slice(0, 200),
        },
        { merge: true }
      );

      input.value = "";
      setTyping(false);
      input.focus();
    } catch (err) {
      showSystemMessage("Message send failed. Try again.");
    }
  });

  input.addEventListener("input", () => {
    const clean = sanitize(input.value);
    if (clean.length > 0) {
      setTyping(true);
      clearTimeout(typingTimer);
      typingTimer = setTimeout(() => setTyping(false), 1200);
    } else {
      setTyping(false);
    }
  });

  window.addEventListener("beforeunload", () => {
    setTyping(false);
    setPresence(false);
  });

  function authenticate() {
    return fetch(data.tokenEndpoint, {
      method: "GET",
      credentials: "same-origin",
      headers: { "X-Requested-With": "XMLHttpRequest" },
    })
      .then((res) => res.json())
      .then((payload) => {
        if (!payload.ok || !payload.token) {
          throw new Error(payload.message || "Firebase token unavailable.");
        }
        return auth.signInWithCustomToken(payload.token);
      });
  }

  function ensureRoomMetadata() {
    return roomRef.set(
      {
        participants: [String(currentUser.uid), String(selectedUser.id)].sort(),
        participantUsernames: [currentUser.username, selectedUser.username].sort(),
        updatedAt: firebase.firestore.FieldValue.serverTimestamp(),
      },
      { merge: true }
    );
  }

  function subscribeMessages() {
    return messagesRef
      .orderBy("createdAt", "asc")
      .limitToLast(120)
      .onSnapshot((snapshot) => {
        const shouldStickToBottom = isNearBottom();
        messageList.innerHTML = "";
        snapshot.forEach((doc) => renderMessage(doc.data()));
        if (shouldStickToBottom) scrollToBottom();
      });
  }

  function subscribePresence() {
    partnerPresenceRef.onSnapshot((doc) => {
      const info = doc.exists ? doc.data() : {};
      const isOnline = !!info.online;
      const inRoomTyping = info.typingRoomId === roomId;
      if (activeStatus) activeStatus.textContent = isOnline ? "Online" : "Offline";
      if (typingIndicator) {
        typingIndicator.classList.toggle("active", !!inRoomTyping);
        typingIndicator.textContent = inRoomTyping ? `${selectedUser.fullName} is typing...` : "";
      }
      const presenceBadge = document.getElementById(`presence-${selectedUser.id}`);
      if (presenceBadge) presenceBadge.textContent = isOnline ? "Online" : "Offline";
    });
  }

  function setPresence(online) {
    return myPresenceRef.set(
      {
        online: !!online,
        lastSeen: firebase.firestore.FieldValue.serverTimestamp(),
        typingRoomId: isTyping ? roomId : "",
      },
      { merge: true }
    );
  }

  function setTyping(state) {
    isTyping = !!state;
    myPresenceRef.set(
      {
        typingRoomId: isTyping ? roomId : "",
        lastSeen: firebase.firestore.FieldValue.serverTimestamp(),
      },
      { merge: true }
    );
  }

  function sanitize(value) {
    return (value || "")
      .replace(/[<>]/g, "")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, 500);
  }

  function renderMessage(msg) {
    const isSelf = String(msg.senderUid) === String(currentUser.uid);
    const row = document.createElement("div");
    row.className = `message-row ${isSelf ? "self" : "other"}`;

    const avatar = document.createElement("img");
    avatar.className = "message-avatar";
    avatar.alt = msg.senderName || "User";
    avatar.src = msg.senderProfilePicture || selectedUser.profilePicture || "";
    if (!avatar.src) avatar.style.visibility = "hidden";

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";

    const body = document.createElement("div");
    body.textContent = msg.text || "";

    const meta = document.createElement("div");
    meta.className = "message-meta";
    meta.innerHTML = `<span>${isSelf ? "You" : selectedUser.fullName}</span><span>${formatTimestamp(
      msg.createdAt
    )}</span>`;

    bubble.appendChild(body);
    bubble.appendChild(meta);

    if (!isSelf) row.appendChild(avatar);
    row.appendChild(bubble);
    messageList.appendChild(row);
  }

  function formatTimestamp(ts) {
    try {
      const date = ts && ts.toDate ? ts.toDate() : new Date();
      return new Intl.DateTimeFormat("en-IN", {
        hour: "numeric",
        minute: "2-digit",
        day: "2-digit",
        month: "short",
      }).format(date);
    } catch (e) {
      return "";
    }
  }

  function scrollToBottom() {
    messageList.scrollTop = messageList.scrollHeight;
  }

  function isNearBottom() {
    const threshold = 80;
    return messageList.scrollHeight - messageList.scrollTop - messageList.clientHeight < threshold;
  }

  function showSystemMessage(text) {
    if (!messageList) return;
    const wrap = document.createElement("div");
    wrap.className = "empty-chat-main";
    wrap.innerHTML = `<p>${text}</p>`;
    messageList.innerHTML = "";
    messageList.appendChild(wrap);
  }
})();
