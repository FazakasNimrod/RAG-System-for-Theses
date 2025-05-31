import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./components/Header/Header";
import SearchPage from "./pages/SearchPage/SearchPage";
import SemanticSearchPage from "./pages/SemanticSearchPage/SemanticSearchPage";
import RagPage from "./pages/RagPage/RagPage";
import StatisticsPage from "./pages/StatisticsPage/StatisticsPage";
import SignUpPage from "./pages/SignUpPage/SignUpPage";
import SignInPage from "./pages/SignInPage/SignInPage";
import "./App.css";

const App = () => {
  return (
    <Router>
      <Header />
      <div className="app-container">
        <Routes>
          <Route path="/" element={<SearchPage />} />
          <Route path="/semantic" element={<SemanticSearchPage />} />
          <Route path="/rag" element={<RagPage />} />
          <Route path="/statistics" element={<StatisticsPage />} />
          <Route path="/signup" element={<SignUpPage />} />
          <Route path="/signin" element={<SignInPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
