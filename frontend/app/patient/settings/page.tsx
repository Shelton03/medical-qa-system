"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  User,
  Bell,
  Moon,
  Info,
  LogOut,
  ChevronRight,
  Lock,
  Palette,
  ShieldCheck,
} from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import { useToast } from "@/hooks/useToast";

interface SettingsSection {
  id: string;
  title: string;
  icon: React.ElementType;
  iconColor: string;
  items: SettingsItem[];
}

interface SettingsItem {
  id: string;
  label: string;
  description?: string;
  action?: () => void;
  toggle?: boolean;
  initialValue?: boolean;
  href?: string;
  destructive?: boolean;
}

export default function PatientSettingsPage(): React.ReactElement {
  const { logout } = useAuth();
  const { showToast } = useToast();

  const [toggles, setToggles] = useState<Record<string, boolean>>({
    "notifications-push": true,
    "notifications-email": false,
    "notifications-sms": true,
    "appearance-dark": false,
  });

  const handleToggle = (id: string) => {
    setToggles((prev) => {
      const next = { ...prev, [id]: !prev[id] };
      showToast({
        title: next[id] ? "Enabled" : "Disabled",
        message: `${id.split("-").slice(1).join(" ")} ${next[id] ? "enabled" : "disabled"}.`,
        type: "info",
      });
      return next;
    });
  };

  const sections: SettingsSection[] = [
    {
      id: "account",
      title: "Account",
      icon: User,
      iconColor: "bg-celestialBlue/10 text-celestialBlue",
      items: [
        {
          id: "change-password",
          label: "Change Password",
          description: "Update your account password",
          action: () => showToast({ title: "Coming soon", message: "Password change will be available soon.", type: "info" }),
        },
        {
          id: "privacy",
          label: "Privacy Settings",
          description: "Manage data visibility",
          action: () => showToast({ title: "Coming soon", message: "Privacy settings will be available soon.", type: "info" }),
        },
      ],
    },
    {
      id: "notifications",
      title: "Notifications",
      icon: Bell,
      iconColor: "bg-alertOrange/10 text-alertOrange",
      items: [
        {
          id: "notifications-push",
          label: "Push Notifications",
          description: "Receive alerts on your device",
          toggle: true,
          initialValue: toggles["notifications-push"],
        },
        {
          id: "notifications-email",
          label: "Email Notifications",
          description: "Get updates via email",
          toggle: true,
          initialValue: toggles["notifications-email"],
        },
        {
          id: "notifications-sms",
          label: "SMS Alerts",
          description: "Critical alerts via text",
          toggle: true,
          initialValue: toggles["notifications-sms"],
        },
      ],
    },
    {
      id: "appearance",
      title: "Appearance",
      icon: Moon,
      iconColor: "bg-mirageBlack/10 text-mirageBlack",
      items: [
        {
          id: "appearance-dark",
          label: "Dark Mode",
          description: "Switch to dark theme",
          toggle: true,
          initialValue: toggles["appearance-dark"],
        },
      ],
    },
    {
      id: "about",
      title: "About Mirage",
      icon: Info,
      iconColor: "bg-healthGreen/10 text-healthGreen",
      items: [
        {
          id: "version",
          label: "Version",
          description: "Mirage Health v1.0.0",
        },
        {
          id: "terms",
          label: "Terms of Service",
          action: () => showToast({ title: "Coming soon", message: "Terms of Service will be available soon.", type: "info" }),
        },
        {
          id: "privacy-policy",
          label: "Privacy Policy",
          action: () => showToast({ title: "Coming soon", message: "Privacy Policy will be available soon.", type: "info" }),
        },
      ],
    },
  ];

  return (
    <div className="p-4 space-y-6 pb-20">
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <h1 className="text-page-title font-heading text-mirageBlack">Settings</h1>
        <p className="text-caption text-clinicalGrey">Manage your preferences</p>
      </motion.div>

      {sections.map((section, sectionIndex) => (
        <motion.div
          key={section.id}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 * sectionIndex, duration: 0.3 }}
        >
          <div className="flex items-center gap-2 mb-2">
            <div className={`w-6 h-6 rounded-md flex items-center justify-center ${section.iconColor}`}>
              <section.icon className="w-3.5 h-3.5" />
            </div>
            <h2 className="text-body font-semibold text-mirageBlack">{section.title}</h2>
          </div>
          <div className="bg-white border border-border rounded-card overflow-hidden divide-y divide-border">
            {section.items.map((item) => (
              <div
                key={item.id}
                className="flex items-center justify-between p-3 hover:bg-mirageBlack-50 transition-colors"
              >
                <div className="flex-1 min-w-0">
                  <p className={`text-body ${item.destructive ? "text-errorRed" : "text-mirageBlack"}`}>
                    {item.label}
                  </p>
                  {item.description && (
                    <p className="text-caption text-clinicalGrey">{item.description}</p>
                  )}
                </div>
                {item.toggle ? (
                  <button
                    onClick={() => handleToggle(item.id)}
                    className={`relative w-11 h-6 rounded-full transition-colors ${
                      toggles[item.id] ? "bg-celestialBlue" : "bg-mirageBlack-200"
                    }`}
                  >
                    <span
                      className={`absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform ${
                        toggles[item.id] ? "translate-x-5" : "translate-x-0"
                      }`}
                    />
                  </button>
                ) : item.action ? (
                  <button
                    onClick={item.action}
                    className="p-1.5 rounded-full hover:bg-mirageBlack-100 transition-colors"
                  >
                    <ChevronRight className="w-4 h-4 text-clinicalGrey" />
                  </button>
                ) : null}
              </div>
            ))}
          </div>
        </motion.div>
      ))}

      {/* Logout */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5, duration: 0.3 }}
      >
        <button
          onClick={() => logout()}
          className="w-full flex items-center justify-center gap-2 py-3 border border-errorRed/20 text-errorRed rounded-card text-body font-medium hover:bg-errorRed-50 transition-colors"
        >
          <LogOut className="w-4 h-4" />
          Sign Out
        </button>
      </motion.div>

      <div className="text-center pt-2">
        <p className="text-micro text-clinicalGrey">Mirage Health v1.0.0</p>
      </div>
    </div>
  );
}
