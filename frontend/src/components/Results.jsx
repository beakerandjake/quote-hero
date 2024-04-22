export const Results = ({ results }) => (
  <div className="flex flex-col items-center gap-5">
    <h3 className="text-lg font-bold">
      You matched {results.total} results!!!
    </h3>
    <h4 className="text-md font-bold">Top Results:</h4>
    <ul className="list-disc">
      {results.top.map((r, i) => (
        <li key={i}>
          <a
            className="font-medium text-blue-600 hover:underline dark:text-blue-500"
            href={`https://en.wikiquote.org/?curid=${r.pageId}`}
          >
            {r.title}
          </a>
        </li>
      ))}
    </ul>
  </div>
);
