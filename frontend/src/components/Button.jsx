/**
 * Basic button component
 */
export const Button = ({ children, ...props }) => {
  return (
    <button
      {...props}
      className="bg-wikimedia hover:bg-wikimedia-light rounded px-3 py-2 text-sm font-semibold text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#36c] disabled:bg-gray-400 dark:disabled:border disabled:dark:border-gray-700 disabled:dark:bg-gray-900"
    >
      {children}
    </button>
  );
};
