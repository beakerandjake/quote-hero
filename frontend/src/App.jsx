import { useState } from "react";
import { Button } from "./components/Button";
import { getWord } from "./services/api.js";

export const App = () => {
  const [words, setWords] = useState([]);

  const addWord = async () => {
    const word = await getWord();
    setWords((prev) => [...prev, word]);
  };

  return (
    <div className="min-h-full">
      <main className="mx-auto max-w-7xl px-4 py-20 sm:px-6 md:py-24 lg:px-8">
        {/* Title */}
        <div className="text-center">
          <h1 className="text-4xl font-bold lg:text-6xl">
            QuoteMaster <span className="pl-1">💬</span>
          </h1>
          <div className="text-md mt-3 text-gray-500 md:text-xl  dark:text-slate-400">
            How many pages can you match?
          </div>
        </div>
        {/* Content */}
        <div className="mt-10 flex flex-col">
          <Button onClick={addWord}>Hello World</Button>
          <div>[{words.join(",")}]</div>
        </div>
      </main>
    </div>
  );
};

export default App;
