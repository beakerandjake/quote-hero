import { useState } from "react";
import { Button } from "./components/Button";
import { getWord, search } from "./services/api.js";
import { Results } from "./components/Results.jsx";
import { Words } from "./components/Words.jsx";
import { PageHeader } from "./components/PageHeader.jsx";
import { SubmitControls } from "./components/SubmitControls.jsx";
import { HighScores } from "./components/HighScores.jsx";

export const App = () => {
  const [words, setWords] = useState([]);
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [highScores, setHighScores] = useState({
    forgiving: {
      wordCount: 0,
      matchCount: 0,
    },
    exact: {
      wordCount: 0,
      matchCount: 0,
    },
  });

  // gets a random word from the api and adds it to our word collection
  const onAddWord = async () => {
    if (isLoading) {
      return;
    }
    setIsLoading(true);
    const word = await getWord();
    setWords((prev) => [...prev, word]);
    setIsLoading(false);
  };

  // clears the current words and results.
  const onReset = () => {
    setWords([]);
    setResults(null);
  };

  // update the high scores if beat the records.
  const tryToUpdateHighScores = (matchCount, forgiving) => {
    const scoreKey = forgiving ? "forgiving" : "exact";
    const best = highScores[scoreKey];
    // bail if didn't have any matches or didn't beat word count.
    if (matchCount < 1 || words.length < best.wordCount) {
      return;
    }
    // bail if didn't beat match count.
    if (words.length === best.wordCount && matchCount <= best.matchCount) {
      return;
    }
    // beat the high score by either number of words or same words but better match count.
    setHighScores({
      ...highScores,
      ...{
        [scoreKey]: {
          wordCount: words.length,
          matchCount: matchCount,
        },
      },
    });
  };

  // searches with the current words
  const onSubmit = async (forgiving) => {
    if (!words.length || isLoading) {
      return;
    }
    setIsLoading(true);
    const results = await search(words, forgiving);
    setResults({ ...results, forgiving });
    tryToUpdateHighScores(results.total, forgiving);
    setIsLoading(false);
  };

  return (
    <div className="min-h-full">
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6">
        {/* Title */}
        <PageHeader />
        {/* Content */}
        <div className="mt-4 flex flex-col items-center gap-3 md:gap-5">
          {/* Words controls */}
          <div className="flex gap-4">
            <Button disabled={!!results} onClick={onAddWord}>
              Add Word
            </Button>
            <Button disabled={!words.length} onClick={onReset}>
              Reset
            </Button>
          </div>
          {/* Word List */}
          <div className="flex w-full justify-center">
            <Words words={words} />
          </div>
          {/* Submit Buttons */}
          {!!words.length && !results && (
            <SubmitControls wordCount={words.length} onSubmit={onSubmit} />
          )}
          {/* Results */}
          {!!results && <Results results={results} />}
          {/* High Scores */}
          {(!!highScores.forgiving.wordCount || !!highScores.exact.wordCount) && (
            <HighScores highScores={highScores} />
          )}
        </div>
      </main>
    </div>
  );
};

export default App;
