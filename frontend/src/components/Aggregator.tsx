import React, { useState, useEffect } from "react";
import Navbar from "./Navbar";

function getTruncatedText(html: string, maxLength: number) {
  const div = document.createElement("div");
  div.innerHTML = html;
  const text = div.textContent || div.innerText || "";
  return text.length > maxLength ? text.slice(0, maxLength) + "..." : text;
}

interface Article {
  title: string;
  content: string;
  source: string;
  published_at: string;
  category: string;
  author: string;
  url: string;
  image?: string;
}

const Aggregator = () => {
  const [articles, setArticles] = useState<Article[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const endpoint = selectedCategory === 'all' 
          ? '/api/news' 
          : `/api/news/filter?category=${selectedCategory}`;
        
        const response = await fetch(endpoint, { signal: controller.signal });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        setArticles(data);
      } catch (err) {
        if (!controller.signal.aborted) {
          setError(err instanceof Error ? err.message : "Failed to fetch news");
        }
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    };

    fetchData();
    return () => controller.abort();
  }, [selectedCategory]);

  const CategoryFilter = ({ selected, onChange }: { 
    selected: string; 
    onChange: (category: string) => void 
  }) => {
    const [categories, setCategories] = useState<string[]>([]);

    useEffect(() => {
      fetch('/api/categories')
        .then(res => res.ok ? res.json() : ['all', 'general', 'technology', 'politics', 'business', 'top'])
        .then(data => setCategories(['all', ...new Set(data.filter((c: string) => c !== 'all'))]))
        .catch(() => setCategories(['all', 'general', 'technology', 'politics', 'business', 'top']));
    }, []);

    return (
      <div className="category-filters mb-8 flex flex-wrap gap-4">
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => onChange(cat)}
            className={`px-4 py-2 rounded-lg transition-all ${
              selected === cat 
                ? 'bg-purple-600 text-white shadow-lg' 
                : 'bg-gray-800 hover:bg-gray-700 text-gray-300 hover:scale-105'
            }`}
          >
            {cat.charAt(0).toUpperCase() + cat.slice(1)}
          </button>
        ))}
      </div>
    );
  };

  const ArticleCard = ({ article }: { article: Article }) => (
    <div className="bg-white/10 backdrop-blur-sm p-6 rounded-xl shadow-lg hover:scale-[1.02] transition-transform">
      <div className="relative h-48 mb-4 rounded-xl overflow-hidden">
        {article.image ? (
          <img
            src={article.image}
            alt={article.title}
            className="w-full h-full object-cover"
            loading="lazy"
            onError={(e) => (e.currentTarget.style.display = 'none')}
          />
        ) : (
          <div className="absolute inset-0 bg-gradient-to-br from-purple-900 to-blue-900 flex items-center justify-center">
            <span className="text-gray-300 text-sm">No image available</span>
          </div>
        )}
      </div>
      
      <h2 className="text-2xl font-bold mb-2 text-white">{article.title}</h2>
      
      <div className="text-gray-300 mb-4">
        <p className="line-clamp-3">
          {getTruncatedText(article.content, 220)}
          {article.content.length > 220 && (
            <a href={article.url} className="text-purple-400 ml-1 underline">Read more</a>
          )}
        </p>
      </div>

      <div className="text-sm space-y-2 text-gray-400">
        <p><span className="font-semibold">Source:</span> {article.source}</p>
        <p><span className="font-semibold">Category:</span> {article.category}</p>
        <p><span className="font-semibold">Author:</span> {article.author}</p>
        <p><span className="font-semibold">Published:</span> {new Date(article.published_at).toLocaleDateString()}</p>
      </div>

      <a
        href={article.url}
        target="_blank"
        rel="noopener noreferrer"
        className="mt-4 inline-block w-full text-center px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors"
      >
        Read Full Article
      </a>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-black to-blue-900 text-white">
      <Navbar />
      <div className="pt-32 px-4 max-w-7xl mx-auto">
        <CategoryFilter
          selected={selectedCategory}
          onChange={setSelectedCategory}
        />

        {loading && (
          <div className="text-center py-10 space-y-4">
            <div className="animate-pulse bg-purple-900/50 h-12 w-48 mx-auto rounded-lg" />
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="h-96 bg-gray-800/50 rounded-xl animate-pulse" />
              ))}
            </div>
          </div>
        )}

        {error && (
          <div className="text-center py-10 text-red-400">
            <p className="text-xl mb-4">⚠️ Error loading articles</p>
            <p className="text-sm font-mono bg-black/50 p-4 rounded-lg">{error}</p>
          </div>
        )}

        {!loading && !error && (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {articles.map((article, index) => (
              <ArticleCard key={`${article.url}-${index}`} article={article} />
            ))}
            {articles.length === 0 && (
              <div className="col-span-full text-center py-20">
                <p className="text-2xl text-gray-400">No articles found in this category</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Aggregator;
