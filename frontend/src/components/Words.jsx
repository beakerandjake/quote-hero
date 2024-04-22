import { Word } from "./Word";

/**
 * Container for words display
 */
const Card = ({ children }) => (
  <div className="relative inline-flex min-w-64 flex-wrap justify-center gap-3 rounded-lg border border-slate-300 p-5 shadow dark:border-gray-700">
    {children}
  </div>
);

/**
 * Component rendered when no words have been selected.
 */
const NoWords = () => (
  <Card>
    <div className="text-center dark:text-white">
      <p>Add a word to get started.</p>
    </div>
  </Card>
);

/**
 * Displays the words
 */
export const Words = ({ words }) => {
  if (!words.length) {
    return <NoWords />;
  }
  return (
    <Card>
      {words.map((word, i) => (
        <Word word={word} key={i} />
      ))}
    </Card>
  );
};
