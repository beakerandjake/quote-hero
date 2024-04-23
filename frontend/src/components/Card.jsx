/**
 * Container used to display different components.
 */
export const Card = ({ className, children }) => (
  <div
    className={`rounded-lg border border-slate-300 px-8 py-5 shadow dark:border-gray-700 ${className}`}
  >
    {children}
  </div>
);
