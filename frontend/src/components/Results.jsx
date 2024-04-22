export const Results = ({ results }) => (
  <div>
    <h3 className="text-lg font-bold">Got {results.total} results</h3>
    <ul className="mt-2 list-disc">
      {results.top.map((r, i) => (
        <li key={i}>
          <a>{r.title}</a>
        </li>
      ))}
    </ul>
  </div>
);
