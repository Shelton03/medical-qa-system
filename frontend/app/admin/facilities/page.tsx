"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Building2,
  Pencil,
  Trash2,
  Plus,
  X,
  MapPin,
  Globe,
  Clock,
  Stethoscope,
} from "lucide-react";
import { adminApi } from "@/lib/api";
import type { AdminFacilityItem, CreateFacilityPayload, UpdateFacilityPayload } from "@/lib/types";
import { cn } from "@/lib/utils";
import { useToast } from "@/hooks/useToast";

const spring = { type: "spring", stiffness: 380, damping: 32 };

const initialForm: CreateFacilityPayload = {
  name: "",
  address: "",
  phone: "",
  email: "",
  city: "",
  country: "",
  timezone: "",
};

export default function AdminFacilitiesPage(): React.ReactElement {
  const { showToast } = useToast();
  const queryClient = useQueryClient();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingFacility, setEditingFacility] = useState<AdminFacilityItem | null>(null);
  const [form, setForm] = useState<CreateFacilityPayload>(initialForm);
  const [confirmDelete, setConfirmDelete] = useState<string | null>(null);

  const { data: facilities, isLoading } = useQuery({
    queryKey: ["admin", "facilities"],
    queryFn: () => adminApi.listFacilities(),
  });

  const createMutation = useMutation({
    mutationFn: (data: CreateFacilityPayload) => adminApi.createFacility(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "facilities"] });
      showToast({ title: "Facility created successfully.", message: "", type: "success" });
      closeModal();
    },
    onError: (err: unknown) => {
      const message = err instanceof Error ? err.message : "Failed to create facility.";
      showToast({ title: message, message: "", type: "error" });
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: UpdateFacilityPayload }) =>
      adminApi.updateFacility(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "facilities"] });
      showToast({ title: "Facility updated successfully.", message: "", type: "success" });
      closeModal();
    },
    onError: (err: unknown) => {
      const message = err instanceof Error ? err.message : "Failed to update facility.";
      showToast({ title: message, message: "", type: "error" });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => adminApi.deleteFacility(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "facilities"] });
      showToast({ title: "Facility deleted successfully.", message: "", type: "success" });
      setConfirmDelete(null);
    },
    onError: (err: unknown) => {
      const message = err instanceof Error ? err.message : "Failed to delete facility.";
      showToast({ title: message, message: "", type: "error" });
      setConfirmDelete(null);
    },
  });

  function openAddModal() {
    setEditingFacility(null);
    setForm(initialForm);
    setIsModalOpen(true);
  }

  function openEditModal(facility: AdminFacilityItem) {
    setEditingFacility(facility);
    setForm({
      name: facility.name,
      address: facility.address ?? "",
      phone: facility.phone ?? "",
      email: facility.email ?? "",
      city: facility.city ?? "",
      country: facility.country ?? "",
      timezone: facility.timezone ?? "",
    });
    setIsModalOpen(true);
  }

  function closeModal() {
    setIsModalOpen(false);
    setEditingFacility(null);
    setForm(initialForm);
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.name.trim()) {
      showToast({ title: "Facility name is required.", message: "", type: "error" });
      return;
    }
    if (editingFacility) {
      const payload: UpdateFacilityPayload = {};
      if (form.name !== undefined) payload.name = form.name;
      if (form.address !== undefined) payload.address = form.address || null;
      if (form.phone !== undefined) payload.phone = form.phone || null;
      if (form.email !== undefined) payload.email = form.email || null;
      if (form.city !== undefined) payload.city = form.city || null;
      if (form.country !== undefined) payload.country = form.country || null;
      if (form.timezone !== undefined) payload.timezone = form.timezone || null;
      updateMutation.mutate({ id: editingFacility.id, data: payload });
    } else {
      createMutation.mutate(form);
    }
  }

  return (
    <div className="space-y-6">
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={spring}>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-mirageBlack">Facilities</h1>
            <p className="text-clinicalGrey">Manage healthcare facilities and locations</p>
          </div>
          <button
            onClick={openAddModal}
            className="inline-flex items-center gap-2 px-4 py-2 bg-celestialBlue text-white rounded-lg text-sm font-medium hover:bg-celestialBlue/90 transition-colors"
          >
            <Plus className="w-4 h-4" />
            Add Facility
          </button>
        </div>
      </motion.div>

      {/* Table */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ ...spring, delay: 0.1 }}
        className="bg-white rounded-xl border border-border overflow-hidden"
      >
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-clinicalGrey uppercase bg-stellarWhite border-b border-border">
              <tr>
                <th className="px-6 py-3">Name</th>
                <th className="px-6 py-3">City</th>
                <th className="px-6 py-3">Country</th>
                <th className="px-6 py-3">Timezone</th>
                <th className="px-6 py-3">Doctors</th>
                <th className="px-6 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {isLoading ? (
                Array.from({ length: 5 }).map((_, i) => (
                  <tr key={i} className="border-b border-border animate-shimmer">
                    <td className="px-6 py-4"><div className="h-4 w-32 bg-clinicalGrey/20 rounded" /></td>
                    <td className="px-6 py-4"><div className="h-4 w-20 bg-clinicalGrey/20 rounded" /></td>
                    <td className="px-6 py-4"><div className="h-4 w-20 bg-clinicalGrey/20 rounded" /></td>
                    <td className="px-6 py-4"><div className="h-4 w-24 bg-clinicalGrey/20 rounded" /></td>
                    <td className="px-6 py-4"><div className="h-4 w-10 bg-clinicalGrey/20 rounded" /></td>
                    <td className="px-6 py-4 text-right"><div className="h-4 w-16 bg-clinicalGrey/20 rounded ml-auto" /></td>
                  </tr>
                ))
              ) : facilities && facilities.length > 0 ? (
                facilities.map((facility) => (
                  <tr key={facility.id} className="border-b border-border hover:bg-stellarWhite/50 transition-colors">
                    <td className="px-6 py-4 font-medium text-mirageBlack whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <Building2 className="w-4 h-4 text-celestialBlue" />
                        {facility.name}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-clinicalGrey">
                      <div className="flex items-center gap-1.5">
                        <MapPin className="w-3.5 h-3.5" />
                        {facility.city ?? "—"}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-clinicalGrey">
                      <div className="flex items-center gap-1.5">
                        <Globe className="w-3.5 h-3.5" />
                        {facility.country ?? "—"}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-clinicalGrey">
                      <div className="flex items-center gap-1.5">
                        <Clock className="w-3.5 h-3.5" />
                        {facility.timezone ?? "—"}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-clinicalGrey">
                      <div className="flex items-center gap-1.5">
                        <Stethoscope className="w-3.5 h-3.5" />
                        {facility.doctor_count ?? 0}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="inline-flex items-center gap-2">
                        <button
                          onClick={() => openEditModal(facility)}
                          className="inline-flex items-center gap-1 text-xs text-celestialBlue hover:underline font-medium"
                        >
                          <Pencil className="w-3.5 h-3.5" />
                          Edit
                        </button>
                        <button
                          onClick={() => setConfirmDelete(facility.id)}
                          className="inline-flex items-center gap-1 text-xs text-alertOrange hover:underline font-medium"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-clinicalGrey">
                    No facilities found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </motion.div>

      {/* Modal */}
      <AnimatePresence>
        {isModalOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4"
            onClick={(e) => {
              if (e.target === e.currentTarget) closeModal();
            }}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.96, y: 8 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.96, y: 8 }}
              transition={{ type: "spring", stiffness: 400, damping: 30 }}
              className="bg-white rounded-xl border border-border shadow-lg w-full max-w-lg max-h-[90vh] overflow-y-auto"
            >
              <div className="flex items-center justify-between px-6 py-4 border-b border-border">
                <h2 className="text-lg font-bold text-mirageBlack">
                  {editingFacility ? "Edit Facility" : "Add Facility"}
                </h2>
                <button
                  onClick={closeModal}
                  className="text-clinicalGrey hover:text-mirageBlack transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <form onSubmit={handleSubmit} className="px-6 py-4 space-y-4">
                <div>
                  <label className="text-xs text-clinicalGrey font-medium block mb-1">Name *</label>
                  <input
                    type="text"
                    value={form.name}
                    onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                    className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30"
                    placeholder="Facility name"
                    required
                  />
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="text-xs text-clinicalGrey font-medium block mb-1">City</label>
                    <input
                      type="text"
                      value={form.city ?? ""}
                      onChange={(e) => setForm((f) => ({ ...f, city: e.target.value }))}
                      className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30"
                      placeholder="City"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-clinicalGrey font-medium block mb-1">Country</label>
                    <input
                      type="text"
                      value={form.country ?? ""}
                      onChange={(e) => setForm((f) => ({ ...f, country: e.target.value }))}
                      className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30"
                      placeholder="Country"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-xs text-clinicalGrey font-medium block mb-1">Address</label>
                  <input
                    type="text"
                    value={form.address ?? ""}
                    onChange={(e) => setForm((f) => ({ ...f, address: e.target.value }))}
                    className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30"
                    placeholder="Street address"
                  />
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="text-xs text-clinicalGrey font-medium block mb-1">Phone</label>
                    <input
                      type="text"
                      value={form.phone ?? ""}
                      onChange={(e) => setForm((f) => ({ ...f, phone: e.target.value }))}
                      className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30"
                      placeholder="Phone number"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-clinicalGrey font-medium block mb-1">Email</label>
                    <input
                      type="email"
                      value={form.email ?? ""}
                      onChange={(e) => setForm((f) => ({ ...f, email: e.target.value }))}
                      className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30"
                      placeholder="Email address"
                    />
                  </div>
                </div>
                <div>
                  <label className="text-xs text-clinicalGrey font-medium block mb-1">Timezone</label>
                  <input
                    type="text"
                    value={form.timezone ?? ""}
                    onChange={(e) => setForm((f) => ({ ...f, timezone: e.target.value }))}
                    className="w-full px-3 py-2 rounded-lg border border-border text-sm text-mirageBlack focus:outline-none focus:ring-2 focus:ring-celestialBlue/30"
                    placeholder="e.g. UTC, Africa/Harare"
                  />
                </div>
                <div className="flex items-center justify-end gap-3 pt-2">
                  <button
                    type="button"
                    onClick={closeModal}
                    className="px-4 py-2 text-sm text-clinicalGrey hover:text-mirageBlack transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={createMutation.isPending || updateMutation.isPending}
                    className={cn(
                      "px-4 py-2 bg-celestialBlue text-white rounded-lg text-sm font-medium transition-colors",
                      (createMutation.isPending || updateMutation.isPending) && "opacity-60 cursor-not-allowed"
                    )}
                  >
                    {editingFacility
                      ? updateMutation.isPending
                        ? "Saving..."
                        : "Save Changes"
                      : createMutation.isPending
                      ? "Creating..."
                      : "Create Facility"}
                  </button>
                </div>
              </form>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Delete Confirmation */}
      <AnimatePresence>
        {confirmDelete && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4"
            onClick={(e) => {
              if (e.target === e.currentTarget) setConfirmDelete(null);
            }}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.96, y: 8 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.96, y: 8 }}
              transition={{ type: "spring", stiffness: 400, damping: 30 }}
              className="bg-white rounded-xl border border-border shadow-lg w-full max-w-sm px-6 py-5"
            >
              <h3 className="text-lg font-bold text-mirageBlack mb-1">Delete Facility</h3>
              <p className="text-sm text-clinicalGrey mb-4">
                Are you sure you want to delete this facility? Facilities with assigned doctors cannot be deleted.
              </p>
              <div className="flex items-center justify-end gap-3">
                <button
                  onClick={() => setConfirmDelete(null)}
                  className="px-4 py-2 text-sm text-clinicalGrey hover:text-mirageBlack transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={() => deleteMutation.mutate(confirmDelete)}
                  disabled={deleteMutation.isPending}
                  className={cn(
                    "px-4 py-2 bg-alertOrange text-white rounded-lg text-sm font-medium transition-colors",
                    deleteMutation.isPending && "opacity-60 cursor-not-allowed"
                  )}
                >
                  {deleteMutation.isPending ? "Deleting..." : "Delete"}
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
