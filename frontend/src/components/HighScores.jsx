import { Card } from "./Card";

/**
 * Displays information about a high score.
 */
const HighScore = ({ name, wordCount, matchCount }) => {
  return (
    <span className="dark:text-white">
      {name} - words: {wordCount}, matches: {matchCount}
    </span>
  );
};

/**
 * Displays the high scores
 */
export const HighScores = ({ highScores }) => {
  return (
    <Card>
      <div className="flex gap-3">
        <HighScore name="Fuzzy" {...highScores.easy} />
        <HighScore name="Exact" {...highScores.hard} />
      </div>
    </Card>
  );
};
