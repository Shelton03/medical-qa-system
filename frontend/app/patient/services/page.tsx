"use client";

import React from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { CalendarPlus, ClipboardList, Stethoscope } from "lucide-react";

const services = [
  {
    href: "/patient/book-appointment",
    title: "Book Appointment",
    description: "Schedule a visit at your preferred healthcare facility",
    icon: CalendarPlus,
    color: "bg-celestialBlue text-white",
  },
  {
    href: "/patient/appointments",
    title: "My Appointments",
    description: "View upcoming and past appointments",
    icon: ClipboardList,
    color: "bg-mirageBlack text-white",
  },
];

export default function ServicesHubPage(): React.ReactElement {
  return (
    <div className="p-4 space-y-5 pb-20">
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div className="flex items-center gap-2 mb-1">
          <div className="w-8 h-8 rounded-lg bg-celestialBlue/10 flex items-center justify-center">
            <Stethoscope className="w-4 h-4 text-celestialBlue" />
          </div>
          <h1 className="text-page-title font-heading text-mirageBlack">
            Services
          </h1>
        </div>
        <p className="text-caption text-clinicalGrey">
          Manage your healthcare appointments
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1, duration: 0.3 }}
        className="space-y-6"
      >
        {services.map((service, index) => (
          <React.Fragment key={service.href}>
            <Link href={service.href}>
              <div className="group bg-white border border-border rounded-card p-5 flex items-center gap-4 hover:shadow-elevation-2 transition-all active:scale-[0.99]">
                <div
                  className={`w-12 h-12 rounded-xl flex items-center justify-center shrink-0 ${service.color}`}
                >
                  <service.icon className="w-6 h-6" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-body font-semibold text-mirageBlack">
                    {service.title}
                  </p>
                  <p className="text-caption text-clinicalGrey">
                    {service.description}
                  </p>
                </div>
              </div>
            </Link>
            {index < services.length - 1 && (
              <div className="border-t border-border" />
            )}
          </React.Fragment>
        ))}
      </motion.div>
    </div>
  );
}
