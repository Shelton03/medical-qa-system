import type { Variants, Transition } from 'framer-motion';

/**
 * Mirage Design System — Animation Tokens
 *
 * Default spring: stiffness 380, damping 32
 * Timing: instant 100ms, fast 200ms, standard 300ms, slow 450ms
 */

export const springTransition: Transition = {
  type: 'spring',
  stiffness: 380,
  damping: 32,
};

export const fadeIn: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: 0.3, ease: 'easeOut' },
  },
  exit: {
    opacity: 0,
    transition: { duration: 0.2, ease: 'easeIn' },
  },
};

export const slideIn: Variants = {
  hidden: { x: 24, opacity: 0 },
  visible: {
    x: 0,
    opacity: 1,
    transition: springTransition,
  },
  exit: {
    x: -24,
    opacity: 0,
    transition: { duration: 0.2, ease: 'easeIn' },
  },
};

export const slideUp: Variants = {
  hidden: { y: 24, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: springTransition,
  },
  exit: {
    y: 24,
    opacity: 0,
    transition: { duration: 0.2, ease: 'easeIn' },
  },
};

export const scaleIn: Variants = {
  hidden: { scale: 0.96, opacity: 0 },
  visible: {
    scale: 1,
    opacity: 1,
    transition: springTransition,
  },
  exit: {
    scale: 0.96,
    opacity: 0,
    transition: { duration: 0.2, ease: 'easeIn' },
  },
};

export const staggerContainer: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.06,
      delayChildren: 0.05,
    },
  },
  exit: {
    opacity: 0,
    transition: { staggerChildren: 0.04, staggerDirection: -1 },
  },
};

export const staggerItem: Variants = {
  hidden: { y: 12, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: springTransition,
  },
  exit: {
    y: 8,
    opacity: 0,
    transition: { duration: 0.15 },
  },
};

export const pageTransition: Variants = {
  hidden: { opacity: 0, x: 16 },
  visible: {
    opacity: 1,
    x: 0,
    transition: springTransition,
  },
  exit: {
    opacity: 0,
    x: -16,
    transition: { duration: 0.2, ease: 'easeIn' },
  },
};

export const bottomSheet: Variants = {
  hidden: { y: '100%', opacity: 0.8 },
  visible: {
    y: 0,
    opacity: 1,
    transition: { type: 'spring', stiffness: 300, damping: 30 },
  },
  exit: {
    y: '100%',
    opacity: 0.8,
    transition: { duration: 0.25, ease: 'easeIn' },
  },
};

export const notificationSlide: Variants = {
  hidden: { y: -24, opacity: 0, scale: 0.98 },
  visible: {
    y: 0,
    opacity: 1,
    scale: 1,
    transition: springTransition,
  },
  exit: {
    y: -16,
    opacity: 0,
    scale: 0.98,
    transition: { duration: 0.2, ease: 'easeIn' },
  },
};
