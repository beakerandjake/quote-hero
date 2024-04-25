import { Button } from "./Button";

/**
 * Controls that should appear when there is only one word
 */
const SingleWordControls = ({ onSubmit }) => (
  <Button onClick={() => onSubmit(false)}>Match</Button>
);

/**
 * Controls that should appear when there is multiple words.
 */
const MultipleWordsControls = ({ onSubmit }) => (
  <div className="flex flex-col items-center gap-4">
    <div className="flex items-center gap-4">
      <Button onClick={() => onSubmit(true)}>Match Fuzzy</Button>
      <span className="text-md font-bold dark:text-white">OR</span>
      <Button onClick={() => onSubmit(false)}>Match Exact</Button>
    </div>
  </div>
);

/**
 * The controls used to submit the search. Allows fuzzy or exact matching.
 */
export const SubmitControls = ({ wordCount, onSubmit }) => {
  // If there is only one word, there isn't a difference
  // between fuzzy or exact searching so just show one control.
  if (wordCount < 2) {
    return <SingleWordControls onSubmit={onSubmit} />;
  }
  // If there are multiple words, make the user choose between fuzzy or exact search
  return <MultipleWordsControls onSubmit={onSubmit} />;
};
