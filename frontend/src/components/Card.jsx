/**
 * Container used to display different components.
 */
export const Card = ({ children }) => (
  <div className="rounded-lg border border-slate-300 px-8 py-5 shadow dark:border-gray-700">
    {children}
  </div>
);
