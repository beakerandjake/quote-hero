/**
 * Basic button component
 */
export const Button = ({ children, ...props }) => {
  // default: border-gray-300 text-gray-900 bg-white
  // default disabled:
  // dark: dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:focus:ring-gray-700
  // dark hover: dark:hover:bg-gray-700 dark:hover:border-gray-600
  // dark disabled: dark:disabled:bg-gray-900 dark:disabled:text-gray-400 dark:disabled:border-gray-600
  return (
    <button
      {...props}
      className="bg-wikimedia hover:bg-wikimedia-light rounded px-3 py-2 text-sm font-semibold text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#36c] disabled:bg-gray-400"
    >
      {children}
    </button>
  );
};
