import React, { useState } from "react";
import SearchBar from "../../components/SearchBar/SearchBar";
import Sidebar from "../../components/SideBar/SideBar";
import ResultsList from "../../components/ResultList/ResultsList";
import { searchElasticsearchSemantic } from "../../services/elasticsearchService";
import "../SearchPage/SearchPage.css";

const SemanticSearchPage = () => {
  const [results, setResults] = useState([]);
  const [query, setQuery] = useState("");
  const [year, setYear] = useState("");
  const [sort, setSort] = useState("desc");
  const [limit, setLimit] = useState(10);
  const [loading, setLoading] = useState(false);
  const [department, setDepartment] = useState(null);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const data = await searchElasticsearchSemantic({
        query,
        year,
        sort,
        limit,
        department,
      });
      setResults(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-page">
      <Sidebar
        year={year}
        setYear={setYear}
        sort={sort}
        setSort={setSort}
        limit={limit}
        setLimit={setLimit}
        department={department}
        setDepartment={setDepartment}
        onFilter={handleSearch}
        hidePhraseOption={true}
        hideSortOption={true}
        showLimitOption={true}
      />

      <div className="main-content">
        <h1>Semantic Search</h1>
        <SearchBar onSearch={handleSearch} query={query} setQuery={setQuery} />
        {loading ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Processing semantic search...</p>
          </div>
        ) : (
          <ResultsList results={results} showScores={true} />
        )}
      </div>
    </div>
  );
};

export default SemanticSearchPage;
