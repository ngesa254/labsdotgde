/* Offline additions to the recovered original React application. */
(() => {
  'use strict';
  const draftKey = 'labsdotgde.local.original-draft.v1';
  const historyKey = 'labsdotgde.local.requests.v1';
  const fields = ['name', 'email', 'phone', 'location', 'country', 'building', 'contribute'];
  function read(key, fallback) {
    try { return JSON.parse(localStorage.getItem(key)) ?? fallback; }
    catch { return fallback; }
  }
  function write(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); return true; }
    catch { return false; }
  }
  function cleanDraft(value) {
    return Object.fromEntries(fields.filter(key => typeof value?.[key] === 'string').map(key => [key, value[key]]));
  }
  window.LabsOffline = {
    draft() { return cleanDraft(read(draftKey, {})); },
    saveDraft(value) { write(draftKey, cleanDraft(value)); },
    remember(file) {
      try {
        const data = JSON.parse(file.json);
        const saved = read(historyKey, []);
        const requests = Array.isArray(saved) ? saved : [];
        if (!requests.some(item => item.submitted_at === data.submitted_at && item.email === data.email)) {
          write(historyKey, [...requests, data]);
        }
      } catch { /* The original JSON download still works if storage is unavailable. */ }
    },
  };
  // The saved files contain no recipient age public key. Do not invent one.
  window.LABS_LOCAL_CONFIG = Object.freeze({ inviteEmail: '', publicKeyUrl: '' });
  // Keep the original interface and copy, with an explicit offline handoff note.
  const observer = new MutationObserver(() => {
    const intro = document.querySelector('#invite .invite-intro');
    if (intro && !document.getElementById('offline-handoff-note')) {
      const note = document.createElement('p');
      note.id = 'offline-handoff-note';
      note.className = 'offline-note mono';
      note.append('Your request stays on this device until you choose to share it. ');
      const link = document.createElement('a');
      link.href = './offline.html#invites';
      link.textContent = 'How to share a lab request →';
      note.append(link);
      intro.after(note);
    }
  });
  document.addEventListener('DOMContentLoaded', () => observer.observe(document.getElementById('root'), { childList: true, subtree: true }));
})();
