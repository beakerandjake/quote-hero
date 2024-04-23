import { Word } from "./Word";
import { Card } from "./Card";

/**
 * Component rendered when no words have been selected.
 */
const NoWords = () => (
  <div className="min-w-64">
    <Card>
      <div className="text-center dark:text-white">
        <p>Add a word to get started.</p>
      </div>
    </Card>
  </div>
);

/**
 * Displays the words
 */
export const Words = ({ words }) => {
  if (!words.length) {
    return <NoWords />;
  }
  return (
    <Card className="inline-flex min-w-64 flex-wrap justify-center gap-3">
      {words.map((word, i) => (
        <Word word={word} key={i} />
      ))}
    </Card>
  );
};
