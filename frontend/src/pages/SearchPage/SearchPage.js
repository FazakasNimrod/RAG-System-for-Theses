import React, { useState } from "react";
import SearchBar from "../../components/SearchBar/SearchBar";
import Sidebar from "../../components/SideBar/SideBar";
import ResultsList from "../../components/ResultList/ResultsList";
import { searchElasticsearch } from "../../services/elasticsearchService";
import "./SearchPage.css";

const SearchPage = () => {
  const [results, setResults] = useState([]);
  const [query, setQuery] = useState("");
  const [year, setYear] = useState("");
  const [sort, setSort] = useState("desc");

  const handleSearch = async () => {
    const data = await searchElasticsearch({ query, year, sort });
    setResults(data);
  };

  return (
    <div className="search-page">
      <Sidebar
        year={year}
        setYear={setYear}
        sort={sort}
        setSort={setSort}
        onFilter={handleSearch}
      />

      <div className="main-content">
        <h1>Search Theses</h1>
        <SearchBar onSearch={handleSearch} query={query} setQuery={setQuery} />
        <ResultsList results={results} />
      </div>
    </div>
  );
};

export default SearchPage;
