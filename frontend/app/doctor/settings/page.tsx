"use client";

import React from "react";
import { motion } from "framer-motion";
import { User, LogOut, Bell, Moon, Sun, Shield } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";

export default function DoctorSettingsPage(): React.ReactElement {
  const { user, logout } = useAuth();
  const [darkMode, setDarkMode] = React.useState(false);
  const [emailNotifications, setEmailNotifications] = React.useState(true);
  const [pushNotifications, setPushNotifications] = React.useState(true);

  return (
    <div className="space-y-6">
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-2xl font-bold text-mirageBlack">Settings</h1>
        <p className="text-clinicalGrey">Manage your account and preferences</p>
      </motion.div>

      {/* Profile Card */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.05 }}
        className="bg-white rounded-card border border-border p-6"
      >
        <h2 className="text-section-title font-semibold text-mirageBlack mb-4">Profile</h2>
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 rounded-full bg-mirageBlack-100 flex items-center justify-center">
            <User className="w-7 h-7 text-mirageBlack" />
          </div>
          <div>
            <p className="text-card-title font-semibold text-mirageBlack">
              {user ? `${user.first_name} ${user.last_name}` : "Dr. Mirage"}
            </p>
            <p className="text-sm text-clinicalGrey">{user?.email || "doctor@mirage.health"}</p>
            <span className="inline-flex items-center gap-1 mt-1 px-2 py-0.5 rounded-full text-[10px] font-medium bg-healthGreen/10 text-healthGreen">
              <Shield className="w-2.5 h-2.5" />
              Verified Doctor
            </span>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-4 mt-5 pt-4 border-t border-border">
          <div>
            <p className="text-micro text-clinicalGrey uppercase tracking-wider">Role</p>
            <p className="text-sm text-mirageBlack mt-0.5 capitalize">{user?.role || "Doctor"}</p>
          </div>
          <div>
            <p className="text-micro text-clinicalGrey uppercase tracking-wider">User ID</p>
            <p className="text-sm text-mirageBlack mt-0.5 font-mono">{user?.id?.slice(0, 12) || "—"}...</p>
          </div>
        </div>
      </motion.div>

      {/* Notification Preferences */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white rounded-card border border-border p-6"
      >
        <h2 className="text-section-title font-semibold text-mirageBlack mb-4">Notification Preferences</h2>
        <div className="space-y-4">
          <ToggleRow
            icon={<Bell className="w-4 h-4 text-celestialBlue" />}
            label="Email Notifications"
            description="Receive email alerts for consent requests and updates"
            checked={emailNotifications}
            onChange={setEmailNotifications}
          />
          <ToggleRow
            icon={<Bell className="w-4 h-4 text-healthGreen" />}
            label="Push Notifications"
            description="Real-time browser notifications for urgent events"
            checked={pushNotifications}
            onChange={setPushNotifications}
          />
        </div>
      </motion.div>

      {/* Appearance */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.15 }}
        className="bg-white rounded-card border border-border p-6"
      >
        <h2 className="text-section-title font-semibold text-mirageBlack mb-4">Appearance</h2>
        <div className="space-y-4">
          <ToggleRow
            icon={darkMode ? <Moon className="w-4 h-4 text-mirageBlack" /> : <Sun className="w-4 h-4 text-alertOrange" />}
            label="Dark Mode"
            description="Switch between light and dark themes"
            checked={darkMode}
            onChange={setDarkMode}
          />
        </div>
      </motion.div>

      {/* Danger Zone */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-alertOrange/5 border border-alertOrange/15 rounded-card p-6"
      >
        <h2 className="text-section-title font-semibold text-alertOrange mb-4">Session</h2>
        <button
          onClick={logout}
          className="inline-flex items-center gap-2 px-4 py-2 bg-alertOrange text-white rounded-lg text-sm font-medium hover:bg-alertOrange/90 transition-colors"
        >
          <LogOut className="w-4 h-4" />
          Log Out
        </button>
      </motion.div>
    </div>
  );
}

function ToggleRow({
  icon,
  label,
  description,
  checked,
  onChange,
}: {
  icon: React.ReactNode;
  label: string;
  description: string;
  checked: boolean;
  onChange: (v: boolean) => void;
}): React.ReactElement {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center shrink-0">
          {icon}
        </div>
        <div>
          <p className="text-sm font-medium text-mirageBlack">{label}</p>
          <p className="text-caption text-clinicalGrey">{description}</p>
        </div>
      </div>
      <button
        onClick={() => onChange(!checked)}
        className={`relative w-11 h-6 rounded-full transition-colors ${
          checked ? "bg-celestialBlue" : "bg-clinicalGrey/30"
        }`}
        aria-label={label}
      >
        <span
          className={`absolute top-1 left-1 w-4 h-4 rounded-full bg-white shadow-sm transition-transform ${
            checked ? "translate-x-5" : "translate-x-0"
          }`}
        />
      </button>
    </div>
  );
}
