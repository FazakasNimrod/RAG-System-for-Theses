import React, { useState } from "react";
import SearchBar from "../components/SearchBar";
import ResultsList from "../components/ResultsList";
import { searchElasticsearch } from "../services/elasticsearchService";


const SearchPage = () => {
  const [results, setResults] = useState([]);

  const handleSearch = async (searchParams) => {
    const data = await searchElasticsearch(searchParams);
    setResults(data);
  };

  return (
    <div className="search-page">
      <h1>Search Theses</h1>
      <SearchBar onSearch={handleSearch} />
      <ResultsList results={results} />
    </div>
  );
};

export default SearchPage;
