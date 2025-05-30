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
  const [sort, setSort] = useState("relevance");
  const [isPhrase, setIsPhrase] = useState(false);
  const [department, setDepartment] = useState(null);
  const [searchSupervisors, setSearchSupervisors] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const data = await searchElasticsearch({
        query,
        year,
        sort,
        isPhrase,
        department,
        searchSupervisors,
      });
      setResults(data);
    } catch (error) {
      console.error("Error performing search:", error);
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
        isPhrase={isPhrase}
        setIsPhrase={setIsPhrase}
        department={department}
        setDepartment={setDepartment}
        searchSupervisors={searchSupervisors}
        setSearchSupervisors={setSearchSupervisors}
        onFilter={handleSearch}
        showSupervisorOption={true}
      />

      <div className="main-content">
        <h1>Search Theses</h1>
        <SearchBar onSearch={handleSearch} query={query} setQuery={setQuery} />

        {loading ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Searching...</p>
          </div>
        ) : (
          <ResultsList results={results} />
        )}
      </div>
    </div>
  );
};

export default SearchPage;
