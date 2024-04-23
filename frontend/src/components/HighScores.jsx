/**
 * Displays the high scores
 */
export const HighScores = ({ highScores }) => {
  return <span className="dark:text-white">{JSON.stringify(highScores)}</span>;
};
