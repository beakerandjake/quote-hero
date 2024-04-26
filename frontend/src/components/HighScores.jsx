import { Card } from "./Card";

// adds 's' to end of string if necessary
const pluralize = (str, count) => (count > 1 ? `${str}s` : str);

/**
 * Displays information about a high score.
 */
const HighScore = ({ name, wordCount, matchCount }) => {
  const score = `Used ${wordCount.toLocaleString()} ${pluralize("word", wordCount)}, matched ${matchCount.toLocaleString()} ${pluralize("page", matchCount)}.`;
  return (
    <div className="text-gray-500 dark:text-slate-400">
      <span className="md:text-lg font-semibold">{name}</span>: {score}
    </div>
  );
};

/**
 * Displays the high scores
 */
export const HighScores = ({ highScores }) => {
  return (
    <Card>
      <div className="flex flex-col gap-2">
        <h3 className="text-center text-xl md:text-2xl font-medium leading-6 text-gray-900 dark:text-white">
          High Scores
        </h3>
        <div>
          {highScores.easy.wordCount > 0 && (
            <HighScore name="Forgiving" {...highScores.easy} />
          )}
          {highScores.hard.wordCount > 0 && (
            <HighScore name="Exact" {...highScores.hard} />
          )}
        </div>
      </div>
    </Card>
  );
};
