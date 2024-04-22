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
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 md:py-10 lg:px-8 lg:py-24">
        {/* Title */}
        <PageHeader />
        {/* Content */}
        <div className="mt-4 flex flex-col items-center gap-5">
          {/* Add New Word */}
          <Button onClick={onAddWord}>Add Word</Button>
          {/* Word List */}
          <div className="flex w-full justify-center">
            <Words words={words} />
          </div>
          {/* Submit Buttons */}
          {!!words.length && (
            <div className="flex gap-4">
              <Button onClick={() => onSubmit(true)}>Go (easy)</Button>
              <Button onClick={() => onSubmit(false)}>Go (hard)</Button>
              <Button onClick={onReset}>Reset</Button>
            </div>
          )}
          {/* Results */}
          {!!results && <Results results={results} />}
        </div>
      </main>
    </div>
  );
};

export default App;
