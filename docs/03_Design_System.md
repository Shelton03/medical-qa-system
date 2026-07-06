# Mirage
# Design System Specification

Version: 1.0

---

# 1. Design Philosophy

Mirage is a healthcare application.

Healthcare software must inspire confidence before it communicates information.

The interface should therefore feel:

- Calm
- Clean
- Trustworthy
- Modern
- Fast
- Predictable
- Accessible

The visual language should avoid unnecessary decoration while remaining polished enough for public demonstrations.

Animations should support understanding rather than entertain.

Every interaction should reinforce clarity.

---

# 2. Core Design Principles

The UI follows six principles.

## Clinical First

Important information should always be visible.

Critical allergies.

Warnings.

Consent status.

Current consultation.

These must never become hidden beneath secondary content.

---

## Mobile Native Feel

Although implemented in Next.js, the patient application should feel indistinguishable from a native mobile application.

Users should forget they are using a browser.

Scrolling.

Spacing.

Touch targets.

Animations.

Typography.

Everything should resemble iOS and modern Android applications.

---

## Progressive Disclosure

Do not overwhelm users.

Show summaries first.

Expand into detail only when requested.

Example:

Timeline

↓

Visit Card

↓

Expanded Visit

↓

Diagnosis

↓

Medication

↓

Clinical Notes

---

## Consistency

Every card.

Every button.

Every sheet.

Every dialog.

Every navigation pattern.

Should follow identical rules.

Consistency reduces cognitive load.

---

## Immediate Feedback

Every user interaction should provide feedback.

Button

↓

Pressed

↓

Loading

↓

Completed

↓

Success

Never leave users wondering whether something happened.

---

## Motion With Purpose

Animations communicate:

Hierarchy

State

Navigation

Context

Never animate simply because animation is possible.

---

# 3. Visual Identity

The visual identity should communicate modern digital healthcare.

Suggested keywords:

Minimal

Premium

Professional

Human

Trustworthy

Accessible

Soft

Lightweight

---

# 4. Color System

The application should define semantic colors rather than feature-specific colors.

## Primary

Primary brand color.

Used for:

Primary buttons

Links

Highlights

Selected navigation

Progress

---

## Secondary

Surface accents.

Cards.

Inputs.

Backgrounds.

---

## Accent

Used sparingly.

AI highlights.

Interactive elements.

Illustrations.

---

## Success

Clinical confirmation.

Approved consent.

Completed consultation.

Successful updates.

---

## Warning

Expiring consent.

Medication warnings.

Potential risks.

---

## Destructive

Denied consent.

Errors.

Delete actions.

Critical failures.

---

## Information

General informational banners.

Help.

Guidance.

---

## Neutral

Text.

Borders.

Backgrounds.

Dividers.

Cards.

---

Never hardcode colors.

Everything should reference design tokens.

---

# 5. Typography

Typography should prioritize readability.

Suggested hierarchy:

Display

32–36px

Page Title

28px

Section Title

22px

Card Title

18px

Body

14–16px

Caption

12px

Micro Labels

10–11px

Line heights should prioritize readability.

Avoid dense paragraphs.

---

# 6. Iconography

Use Lucide icons consistently.

Icons should communicate meaning rather than decoration.

Examples:

Patient

Doctor

Hospital

Medication

Timeline

AI

Notification

Settings

Security

Search

Consent

Laboratory

Diagnosis

Documentation

Avoid mixing icon libraries.

---

# 7. Spacing Scale

Spacing should use a fixed scale.

4

8

12

16

20

24

32

40

48

64

Avoid arbitrary spacing values.

---

# 8. Radius Scale

Consistent rounded corners improve familiarity.

Buttons

Full

Cards

16px

Sheets

32px

Inputs

16px

Dialogs

24px

Phone Frame

44px+

---

# 9. Elevation

Use elevation sparingly.

Level 0

Background

Level 1

Cards

Level 2

Floating buttons

Level 3

Bottom sheets

Level 4

Dialogs

Level 5

Notifications

Shadow intensity should remain subtle.

---

# 10. Glass Morphism

Glass surfaces are a defining characteristic of Mirage.

Used for:

Bottom Navigation

Floating Panels

Bottom Sheets

Dialogs

Status Cards

Floating Actions

Properties:

Translucent background

Backdrop blur

Soft border

Subtle shadow

Never reduce readability.

Glass should support content rather than obscure it.

---

# 11. Motion System

All animations should use Framer Motion.

Default spring:

```

stiffness: 380

damping: 32

```

These values should be reused throughout the application.

Consistency is more important than novelty.

---

# 12. Animation Categories

Navigation

Fade + slight slide.

Bottom Sheets

Slide upward.

Dialogs

Fade + scale.

Cards

Fade.

Buttons

Scale on press.

Notifications

Slide from top.

Timeline

Progressive reveal.

Never animate large layout shifts.

---

# 13. Timing

Instant

100ms

Fast

200ms

Standard

300ms

Slow

450ms

Background

800ms+

Users should never wait on animations.

---

# 14. Accessibility

Minimum touch target:

44 × 44

Minimum contrast:

WCAG AA

Focus indicators:

Always visible.

Reduced motion:

Supported.

Animations should disable gracefully.

---

# 15. Component Design Rules

Every component should expose:

Variant

Size

Disabled

Loading

Icon

Accessibility label

Class overrides

Avoid creating one-off components.

Everything should be reusable.

# 16. PhoneFrame Component

The PhoneFrame is the foundation of the patient application.

It is not decorative.

It defines the rendering environment for every patient screen.

Every patient page must render inside PhoneFrame.

---

## Responsibilities

The PhoneFrame should:

- Simulate a modern smartphone.
- Maintain a fixed viewport.
- Prevent browser resizing from affecting layouts.
- Provide realistic safe areas.
- Render the decorative device frame.
- Provide an authentic mobile experience inside the browser.

---

## Dimensions

Large screens

```
370px × 800px
```

Smaller laptops

```
350px × 760px
```

These dimensions remain fixed.

The application scales around the frame rather than resizing its internal layout.

---

## Physical Device Elements

The frame should include:

Rounded bezel

Side buttons

Speaker notch

Camera cut-out

Glass reflection

Soft shadow

Optional home indicator

These elements are decorative and should not interfere with interaction.

---

## Screen Container

The screen container is the only scrollable region.

```
PhoneFrame

├── Device Frame

├── Status Bar

├── Safe Area

├── Application

└── Bottom Navigation
```

Content must never overflow beyond the rounded screen boundaries.

---

# 17. Status Bar

The patient application always displays a simulated status bar.

Contents:

Time

Signal

5G

Battery

Camera notch

Values remain static during the demo.

The goal is realism rather than device integration.

---

# 18. Bottom Navigation

The bottom navigation remains persistent.

Recommended tabs:

Home

Timeline

Symptoms

Notifications

Profile

---

Requirements

Glassmorphism background.

Blur.

Rounded edges.

Animated active indicator.

Touch-friendly spacing.

Safe area padding.

Navigation transitions should feel native.

---

# 19. Header Pattern

Each screen begins with a consistent header.

Header includes:

Title

Optional subtitle

Back button

Optional action

Search (where applicable)

Headers should never exceed two lines.

---

# 20. Card Component

Cards are the primary information container.

Every card should support:

Variant

Size

Leading icon

Trailing action

Loading state

Selected state

Disabled state

Hover state (desktop)

Cards should animate subtly when entering the screen.

---

Card variants:

Information

Medical Record

Timeline

Notification

Consent

AI Suggestion

Alert

Statistic

---

# 21. Button Component

Supported variants:

Primary

Secondary

Ghost

Outline

Danger

Success

Text

Sizes:

Small

Medium

Large

Buttons should support:

Loading

Disabled

Icons

Full width

Rounded

Accessibility labels

Loading buttons replace the label with a spinner.

---

# 22. Input Components

Supported inputs:

Text

Password

Search

Email

Phone

Date

Select

Multi-select

Textarea

Medical Notes

Every input includes:

Label

Placeholder

Validation

Helper text

Error state

Success state

Disabled state

---

Search inputs should debounce requests.

---

# 23. Search Experience

Patient search should feel instantaneous.

Features:

Debounced typing

Keyboard navigation

Highlight matches

Empty state

Loading indicator

Recent searches

Duplicate patient differentiation

---

# 24. Timeline Component

The medical timeline is central to Mirage.

Each entry displays:

Date

Facility

Doctor

Diagnosis

Medication

Summary

Expandable indicator

---

Expanding a visit reveals:

Clinical notes

Medications

Investigations

Attachments

AI summary

Timeline animations should preserve orientation.

The user should never lose their place.

---

# 25. Consent Card

Displays:

Doctor

Facility

Registration Number

Purpose

Requested Scope

Expiration

Buttons:

Approve

Deny

Animation:

Card slides into view.

Approval immediately updates UI.

---

# 26. Notification Card

Supports:

Unread indicator

Category icon

Timestamp

Title

Body

Quick actions

Notification categories:

Consent

Medical Record

Reminder

System

AI

---

# 27. AI Conversation

The AI consultation resembles modern messaging applications.

Messages include:

Speaker

Timestamp

Avatar

Markdown support

Code blocks disabled

Medical references highlighted

Doctor messages align right.

AI aligns left.

Typing indicators supported.

Streaming responses supported.

---

Suggested actions appear beneath AI responses.

Examples:

Ask Follow-up

Explain

Accept

Ignore

Generate Summary

---

# 28. Differential Diagnosis Card

Displays:

Diagnosis

Confidence

Evidence

Contradictory Findings

Suggested Tests

Medication Risks

Expandable reasoning

Doctors can:

Accept

Ignore

Edit

Compare

Nothing is committed automatically.

---

# 29. Clinical Summary Editor

The generated summary appears inside editable sections.

Recommended layout:

SOAP

Subjective

Objective

Assessment

Plan

Rich text editing is unnecessary for MVP.

Plain structured inputs are preferred.

---

# 30. Bottom Sheets

Bottom sheets should be used instead of full-screen dialogs where practical.

Characteristics:

Rounded top corners

Blurred background

Drag handle

Spring animation

Dismiss gesture

Tap outside to close (where safe)

Examples:

Patient Details

Notifications

Consent

Visit Preview

Medication

---

# 31. Dialogs

Dialogs should interrupt only high-risk actions.

Examples:

Delete

Logout

Cancel Consultation

Discard Changes

Permission Errors

Dialogs should never exceed the width of the phone frame.

---

# 32. Floating Action Button

Used sparingly.

Examples:

Start Assessment

New Consultation

Quick Search

Scroll to Top

Should remain above scrolling content.

---

# 33. Loading Components

Avoid blank screens.

Use:

Skeleton cards

Skeleton timeline

Skeleton profile

Animated shimmer

Progress indicators

Loading indicators should resemble the final layout.

---

# 34. Empty States

Every feature defines an empty state.

Examples:

No notifications.

No visits.

No consent requests.

No AI sessions.

Each empty state should include:

Illustration or icon

Explanation

Primary action

---

# 35. Error States

Every feature defines a recoverable error state.

Display:

Friendly message

Retry button

Support text (optional)

Avoid technical language.

Never expose stack traces.

---

# 36. Success States

Success feedback should be immediate.

Examples:

Consent approved

Record updated

Assessment submitted

Consultation completed

Success indicators should combine:

Icon

Color

Short confirmation message

Optional animation

---

# 37. Toast Notifications

Transient events should appear as toast notifications.

Examples:

Saved

Updated

Connected

Disconnected

New notification

Consent approved

Position:

Top of patient frame

Top-right of doctor portal

Duration:

3–5 seconds

User-dismissible.

---

# 38. Doctor Dashboard Components

The dashboard is composed of reusable widgets.

Examples:

Today's Queue

Recent Patients

Pending Consent

AI Activity

System Status

Quick Actions

Statistics

Each widget should be independently reusable and independently loadable.

---

# 39. Split-Screen Demonstration Layout

The preferred demonstration mode is split-screen.

```
--------------------------------------------------------------

Patient Phone         Doctor Dashboard

┌──────────────┐      ┌────────────────────────────────────┐
│              │      │                                    │
│              │      │                                    │
│              │      │                                    │
│              │      │                                    │
│              │      │                                    │
└──────────────┘      └────────────────────────────────────┘

--------------------------------------------------------------
```

Real-time updates should be visible on both sides simultaneously.

This mode should be optimized for presentations, recordings, judging sessions, and stakeholder demonstrations.

---

# 40. Component Definition of Done

Every reusable component should satisfy the following criteria:

- Fully typed with TypeScript.
- Accessible (ARIA, keyboard navigation, focus management).
- Responsive where appropriate.
- Supports loading, error, and disabled states.
- Exposes composable props instead of feature-specific logic.
- Includes documentation/examples for future contributors.
- Avoids embedding business logic.
- Is visually consistent with the design tokens and motion guidelines.

Reusable components should favor composition over inheritance and remain framework-agnostic wherever practical.