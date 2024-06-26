import { Card } from "./Card";

/**
 * Indicates that no results were found.
 */
const NoMatches = () => (
  <Card>
    <h1 className="text-md font-medium leading-6 text-gray-900  dark:text-white">
      No Matches Found
    </h1>
  </Card>
);

/**
 * Displays the results of the search
 */
export const Results = ({ results }) => {
  if (!results.total) {
    return <NoMatches />;
  }
  const matchType = results.forgiving ? "Forgiving" : "Exact";
  return (
    <Card>
      {/* Header */}
      <div className="mb-2">
        <h1 className="text-xl font-medium leading-6 text-gray-900 md:text-2xl dark:text-white">
          {results.total === 1
            ? `Found One ${matchType} Match`
            : `Found ${results.total.toLocaleString()} ${matchType} Matches`}
        </h1>
      </div>
      {/* Content */}
      <h3 className="mb-1 text-lg text-gray-500 dark:text-slate-400">
        Top Results
      </h3>
      {/* Links to the top pages */}
      <ul role="list">
        {results.top.map(({ pageId, title }) => (
          <li
            className="list-inside list-disc text-blue-600 hover:underline dark:text-blue-500"
            key={pageId}
          >
            <a href={`https://en.wikiquote.org/?curid=${pageId}`}>{title}</a>
          </li>
        ))}
      </ul>
    </Card>
  );
};
