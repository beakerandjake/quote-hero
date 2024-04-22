import { Button } from "./Button";

const SingleWordControls = ({ onSubmit }) => (
  <Button onClick={() => onSubmit(false)}>Match</Button>
);

const MultipleWordsControls = ({ onSubmit }) => (
  <div className="flex flex-col items-center gap-4">
    <div className="flex items-center gap-4">
      <Button onClick={() => onSubmit(true)}>Match Fuzzy</Button>
      <span className="text-md font-bold dark:text-white">OR</span>
      <Button onClick={() => onSubmit(false)}>Match Exact</Button>
    </div>
  </div>
);

export const SubmitControls = ({ wordCount, onSubmit }) => {
  return wordCount < 2 ? (
    <SingleWordControls onSubmit={onSubmit} />
  ) : (
    <MultipleWordsControls onSubmit={onSubmit} />
  );
};
