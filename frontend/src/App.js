import { useState } from "react";
import Welcome from "./pages/Welcome";
import Diagnose from "./pages/Diagnose";
import Results from "./pages/Results";

export default function App() {
  const [page, setPage]       = useState("welcome");
  const [results, setResults] = useState(null);
  const [input, setInput]     = useState(null);

  function goToDiagnose() { setPage("diagnose"); }

  function goToResults(data, inputData) {
    setResults(data);
    setInput(inputData);
    setPage("results");
  }

  function goBack() {
    setResults(null);
    setInput(null);
    setPage("diagnose");
  }

  return (
    <div>
      {page === "welcome"  && <Welcome  onStart={goToDiagnose} />}
      {page === "diagnose" && <Diagnose onResults={goToResults} />}
      {page === "results"  && <Results  data={results} input={input} onBack={goBack} />}
    </div>
  );
}