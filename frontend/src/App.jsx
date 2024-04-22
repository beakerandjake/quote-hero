import { useState } from "react";
import { Button } from "./components/Button";
import { getWord, search } from "./services/api.js";
import { Results } from "./components/Results.jsx";
import { Words } from "./components/Words.jsx";
import { PageHeader } from "./components/PageHeader.jsx";

export const App = () => {
  const [words, setWords] = useState([]);
  const [results, setResults] = useState(null);

  const onAddWord = async () => {
    const word = await getWord();
    setWords((prev) => [...prev, word]);
  };

  const onReset = () => {
    setWords([]);
    setResults(null);
  };

  const onSubmit = async (easy) => {
    if (!words.length) {
      return;
    }
    setResults(await search(words, easy));
  };

  return (
    <div className="min-h-full">
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 md:py-10">
        {/* Title */}
        <PageHeader />
        {/* Content */}
        <div className="mt-4 flex flex-col items-center gap-5">
          {/* Add New Word */}
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
          <div className="flex gap-4">
            <Button disabled={!words.length} onClick={() => onSubmit(true)}>
              Go (easy)
            </Button>
            <Button disabled={words.length < 2} onClick={() => onSubmit(false)}>
              Go (hard)
            </Button>
          </div>
          {/* Results */}
          {!!results && <Results results={results} />}
        </div>
      </main>
    </div>
  );
};

export default App;
