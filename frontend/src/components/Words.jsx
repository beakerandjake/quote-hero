import { Word } from "./Word";

/**
 * Displays the words
 */
export const Words = ({ words }) => (
  <div className="flex flex-wrap justify-center gap-3">
    {words.map((word, i) => (
      <Word word={word} key={i} />
    ))}
  </div>
);
