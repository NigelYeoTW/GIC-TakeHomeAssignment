import { useEffect } from "react";
import { useBlocker } from "react-router-dom";
import { Modal } from "antd";

/**
 * Blocks navigation away from a form page when there are unsaved changes.
 * Uses React Router v6's useBlocker to intercept navigation attempts.
 *
 * @param {boolean} isDirty - From React Hook Form's formState.isDirty
 */
export default function UnsavedChangesGuard({ isDirty, isSubmitting }) {
  const blocker = useBlocker(
    ({ currentLocation, nextLocation }) =>
      isDirty && !isSubmitting && currentLocation.pathname !== nextLocation.pathname
  );

  useEffect(() => {
    if (blocker.state === "blocked") {
      Modal.confirm({
        title: "Unsaved Changes",
        content: "You have unsaved changes. Are you sure you want to leave?",
        okText: "Leave",
        cancelText: "Stay",
        onOk: () => blocker.proceed(),
        onCancel: () => blocker.reset(),
      });
    }
  }, [blocker]);

  return null;
}
