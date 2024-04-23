const Card = ({ children }) => (
  <div className="rounded-lg border border-gray-200 px-8 py-5 shadow dark:border-gray-700">
    {children}
  </div>
);

const NoMatches = () => (
  <Card>
    <h1 className="text-md font-medium leading-6 text-gray-900  dark:text-white">
      No Matches Found
    </h1>
  </Card>
);

export const Results = ({ results }) => {
  if (!results.total) {
    return <NoMatches />;
  }
  return (
    <Card>
      {/* Header */}
      <div className="flex flex-col gap-3">
        <h1 className="text-xl font-medium leading-6 text-gray-900  dark:text-white">
          {results.total === 1
            ? "Found One Match"
            : `Found ${results.total} Matches`}
        </h1>
      </div>
      <h3 className="mt-1 text-gray-500 dark:text-slate-400">Top Results:</h3>
      <ul role="list" className="divide-y divide-gray-100">
        {results.top.map(({ pageId, title }) => (
          <li
            className="list-decimal font-medium text-blue-600 hover:underline dark:text-blue-500"
            key={pageId}
          >
            <a href={`https://en.wikiquote.org/?curid=${pageId}`}>{title}</a>
          </li>
        ))}
      </ul>
    </Card>
  );
};
