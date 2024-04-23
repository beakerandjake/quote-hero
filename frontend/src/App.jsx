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
  const [highScores, setHighScores] = useState({
    easy: {
      wordCount: 0,
      matchCount: 0,
    },
    hard: {
      wordCount: 0,
      matchCount: 0,
    },
  });

  // gets a random word from the api and adds it to our word collection
  const onAddWord = async () => {
    const word = await getWord();
    setWords((prev) => [...prev, word]);
  };

  // clears the current words and results.
  const onReset = () => {
    setWords([]);
    setResults(null);
  };

  // update the high scores if beat the records.
  const tryToUpdateHighScores = (matches, easy) => {
    const scoreKey = easy ? "easy" : "hard";
    const best = highScores[scoreKey];
    // bail if didn't have any matches or didn't beat word count.
    if (matches < 1 || words.length < best.wordCount) {
      return;
    }
    // bail if didn't beat match count.
    if (words.length === best.wordCount && matches <= best.matchCount) {
      return;
    }
    // beat the high score by either number of words or same words but better match count.
    setHighScores({
      ...highScores,
      ...{
        [scoreKey]: {
          wordCount: words.length,
          matchCount: matches,
        },
      },
    });
  };

  // searches with the current words
  const onSubmit = async (easy) => {
    if (!words.length) {
      return;
    }
    const results = await search(words, easy);
    setResults(results);
    tryToUpdateHighScores(results.total, easy);
  };

  return (
    <div className="min-h-full">
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6">
        {/* Title */}
        <PageHeader />
        {/* Content */}
        <div className="mt-4 flex flex-col items-center gap-5">
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
          {(!!highScores.easy.wordCount || !!highScores.hard.wordCount) && (
            <HighScores highScores={highScores} />
          )}
        </div>
      </main>
    </div>
  );
};

export default App;
