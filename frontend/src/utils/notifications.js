const STORAGE_KEY = "nyayaai_notifications";

export const getNotifications = () => {
  return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
};

export const saveNotifications = (notifications) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(notifications));
};

export const unreadCount = () => {
  return getNotifications().filter((n) => !n.read).length;
};

// ✅ FIX: prevent spam duplicates
export const addNotification = (title, message, icon) => {
  const notifications = getNotifications();

  const last = notifications[0];

  // 🔥 prevent duplicate back-to-back notifications
  if (
    last &&
    last.title === title &&
    last.message === message &&
    Date.now() - last.id < 5000
  ) {
    return;
  }

  const newNotification = {
    id: Date.now(),
    title,
    message,
    icon,
    read: false,
    time: new Date().toLocaleString(),
  };

  const updated = [newNotification, ...notifications].slice(0, 50); // limit size

  saveNotifications(updated);

  window.dispatchEvent(new Event("notification-update"));
};

export const markAllAsRead = () => {
  const notifications = getNotifications().map((n) => ({
    ...n,
    read: true,
  }));

  saveNotifications(notifications);
  window.dispatchEvent(new Event("notification-update"));
};

export const clearNotifications = () => {
  saveNotifications([]);
  window.dispatchEvent(new Event("notification-update"));
};